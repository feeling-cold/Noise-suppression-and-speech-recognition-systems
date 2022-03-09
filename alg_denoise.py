import numpy as np
from scipy.io import wavfile
import os
import pyroomacoustics as pra
import time
from pyroomacoustics.denoise import IterativeWiener, SpectralSub, Subspace
from concurrent.futures import ThreadPoolExecutor

class espDenoise(object):
    def __init__(self):
        self.pool_list = []
        self.threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="audio_denoise")
        self.exit = False

    def initWiener(self, snr=5, lpc_order=15, iterations=2, frame_len=512, alpha=0.1, threshold=0.003):
        """
        Test and algorithm parameters
        """
        self.snr_wiener = snr  # SNR of input signal

        # the number of LPC coefficients to consider
        self.lpc_order = lpc_order
        # the number of iterations to update wiener filter
        self.iterations = iterations
        # FFT length
        self.frame_len = frame_len
        # parameter update of the sigma in sigma tracking
        self.alpha = alpha #0.1  # smaller value allows noise floor to change faster
        self.threshold = threshold#0.003

    def wienerDenoiseThread(self, noisy_signal, fs, output_path):
        """
        Apply approach
        """
        print("entered wiener thread")
        if self.exit is True:
            return "finished"
        scnr = IterativeWiener(self.frame_len, self.lpc_order, self.iterations, self.alpha, self.threshold)

        # derived parameters
        hop = self.frame_len // 2
        window_a = pra.hann(self.frame_len)
        window_s = pra.transform.stft.compute_synthesis_window(window_a, hop)
        stft = pra.transform.STFT(
            self.frame_len,
            hop=hop,
            analysis_window=window_a,
            synthesis_window=window_s,
            streaming=True,
        )
        speech_psd = np.ones(hop + 1)  # initialize PSD
        noise_psd = 0

        start_time = time.time()
        processed_audio = np.zeros(noisy_signal.shape)
        n = 0
        while noisy_signal.shape[0] - n >= hop:

            # to frequency domain, 50% overlap
            stft.analysis(
                noisy_signal[n : (n + hop)]
            )

            # compute Wiener output
            X = scnr.compute_filtered_output(current_frame=stft.fft_in_buffer, frame_dft=stft.X)

            # back to time domain
            processed_audio[n : n + hop] = stft.synthesis(X)

            # update step
            n += hop

        proc_time = time.time() - start_time
        print("Processing time: {} minutes".format(proc_time / 60))

        """
        Save and plot spectrogram
        """
        wavfile.write(
            output_path,
            fs,
            pra.normalize(processed_audio).astype(np.float32),
        )
        print("Noisy and denoised file written to: ", output_path)

        return 'finished'

    def denoiseWiener(self, sigpath="speaker.wav", noisepath="doing_the_dishes.wav",
                      outpath="denoise_output_IterativeWiener.wav"):
        if os.path.exists(sigpath) and os.path.exists(noisepath):
            """
                    Prepare input file
            """
            signal_fp = sigpath
            noise_fp = noisepath
            noisy_signal, signal, noise, fs = pra.create_noisy_signal(
                signal_fp, snr=self.snr_wiener, noise_fp=noise_fp
            )
            wavfile.write(
                "denoise_input_IterativeWiener.wav",
                fs,
                noisy_signal.astype(np.float32),
            )
            f = self.threadPool.submit(self.wienerDenoiseThread, noisy_signal, fs, outpath)
            self.pool_list.append(f)
        else:
            print("bad luck, filepaths is invalid: %s AND %s" %(sigpath, noisepath))

    def denoiseWienerOneInput(self, inpath="denoise_input_IterativeWiener.wav",
                      outpath="denoise_output_IterativeWiener.wav"):
        if os.path.exists(inpath):
            """
                    Prepare input file
            """
            fs, org_signal = wavfile.read(inpath)
            f = self.threadPool.submit(self.wienerDenoiseThread, org_signal, fs, outpath)
            self.pool_list.append(f)
        else:
            print("bad luck, filepaths is invalid: %s " %(inpath))

    def initSpectralSubtraction(self, snr=5, db_reduc=50, nfft=512, lookback=20, beta=3, alpha=39):
        """
        Test and algorithm parameters
        """
        self.snrSpectral = snr  # 5  # SNR of input signal.
        self.db_reduc = db_reduc  # 10  # Maximum suppression per frequency bin. Large suppresion can result in more musical noise.
        self.nfft = nfft  # Frame length will be nfft/2 as we will use an STFT with 50% overlap.
        self.lookback = lookback  # 12  # How many frames to look back for the noise floor estimate.
        self.beta = beta  # An overestimation factor to "push" the suppression towards db_reduc.
        self.alpha_spe = alpha  # 1.2  # An exponential factor to tune the suppresion (see doc. of 'SpectralSub').

    def SpectralThread(self, noisy_signal, fs, output_path):
        print("enter spetral substraction thread")
        if self.exit is True:
            return "finished"
        """
        Create STFT and SCNR objects
        """
        hop = self.nfft // 2
        window_a = pra.hann(self.nfft)
        window_s = pra.transform.stft.compute_synthesis_window(window_a, hop)
        stft = pra.transform.STFT(
            self.nfft, hop=hop, analysis_window=window_a, synthesis_window=window_s, streaming=True
        )

        scnr = SpectralSub(self.nfft, self.db_reduc, self.lookback, self.beta, self.alpha_spe)
        lookback_time = hop / fs * self.lookback
        print("Lookback : %f seconds" % (lookback_time))

        """
        Process as in real-time
        """
        # collect the processed blocks
        processed_audio = np.zeros(noisy_signal.shape)
        n = 0
        while noisy_signal.shape[0] - n >= hop:
            # SCNR in frequency domain
            stft.analysis(noisy_signal[n: (n + hop)])
            gain_filt = scnr.compute_gain_filter(stft.X)

            # back to time domain
            processed_audio[n: n + hop] = stft.synthesis(gain_filt * stft.X)

            # update step
            n += hop
        print("start writing output file")
        """
        Save and plot spectrogram
        """
        wavfile.write(
            output_path,
            fs,
            pra.normalize(processed_audio).astype(np.float32),
        )
        print("Noisy and denoised file written to: %s" %(output_path))
        return "finished"

    def denoiseSpectralSubtraction(self, sigpath="speaker.wav", noisepath="doing_the_dishes.wav",
                      outpath="denoise_output_SpectralSubtraction.wav"):
        if os.path.exists(sigpath) and os.path.exists(noisepath):
            """
                    Prepare input file
            """
            signal_fp = sigpath
            noise_fp = noisepath
            noisy_signal, signal, noise, fs = pra.create_noisy_signal(
                signal_fp, snr=self.snrSpectral, noise_fp=noise_fp
            )
            wavfile.write(
                "denoise_input_SpectralSubtraction.wav",
                fs,
                noisy_signal.astype(np.float32),
            )
            f = self.threadPool.submit(self.SpectralThread, noisy_signal, fs, outpath)
            self.pool_list.append(f)
        else:
            print("bad luck, filepaths is invalid: %s AND %s" %(sigpath, noisepath))

    def denoiseSpectralSubtractionOneInput(self, inpath="denoise_input_SpectralSubtraction.wav",
                      outpath="denoise_output_SpectralSubtraction.wav"):
        if os.path.exists(inpath):
            """
                    Prepare input file
            """
            fs, org_signal = wavfile.read(inpath)
            f = self.threadPool.submit(self.SpectralThread, org_signal, fs, outpath)
            self.pool_list.append(f)
        else:
            print("bad luck, filepaths is invalid: %s " %(inpath))

    def initSubspace(self, snr=5, frame_len = 80, mu = 10, lookback = 10, skip = 1, threshold = 0.003):
        print("mu is: ",mu)
        self.snrSubspace = snr  # SNR of input signal.
        self.frame_len_sub = frame_len
        self.mu = mu  # 10         # higher value can give more suppression but more distortion

        # parameters for covariance matrix estimation
        self.lookback_sub = lookback  # how many frames to look back
        self.skip = skip  # how many samples to skip when estimating
        self.threshold_sub = threshold  # 0.003    # threshold between (signal+noise) and noise

    def subspaceThread(self, noisy_signal, fs, output_path):
        print("enter subspace thread")
        if self.exit is True:
            return "finished"
        """ 
        Create noise reduction object and apply the method
        """
        scnr = Subspace(self.frame_len_sub, self.mu, self.lookback_sub, self.skip, self.threshold_sub)

        # parse signal as if streaming
        processed_audio = np.zeros(noisy_signal.shape)
        n = 0
        start_time = time.time()
        hop = self.frame_len_sub // 2
        while noisy_signal.shape[0] - n >= hop:
            processed_audio[n:n + hop, ] = scnr.apply(noisy_signal[n:n + hop])

            # update step
            n += hop

        proc_time = time.time() - start_time
        print("{} minutes".format((proc_time / 60)))
        # save to output file
        wavfile.write(output_path, fs,
                      pra.normalize(processed_audio).astype(np.float32))

        print("Noisy and denoised file written to: %s" % (output_path))
        return "finished"

    def denoiseSubspace(self, sigpath="speaker.wav", noisepath="doing_the_dishes.wav",
                      outpath="denoise_output_Subspace.wav"):
        if os.path.exists(sigpath) and os.path.exists(noisepath):
            """
                    Prepare input file
            """
            signal_fp = sigpath
            noise_fp = noisepath
            noisy_signal, signal, noise, fs = pra.create_noisy_signal(
                signal_fp, snr=self.snrSubspace, noise_fp=noise_fp
            )
            wavfile.write(
                "denoise_input_Subspace.wav",
                fs,
                noisy_signal.astype(np.float32),
            )
            f = self.threadPool.submit(self.subspaceThread, noisy_signal, fs, outpath)
            self.pool_list.append(f)
        else:
            print("bad luck, filepaths is invalid: %s AND %s" %(sigpath, noisepath))

    def denoiseSubspaceOneInput(self, inpath="denoise_input_Subspace.wav",
                      outpath="denoise_output_Subspace.wav"):
        if os.path.exists(inpath):
            """
                    Prepare input file
            """
            fs, org_signal = wavfile.read(inpath)
            f = self.threadPool.submit(self.subspaceThread, org_signal, fs, outpath)
            self.pool_list.append(f)
        else:
            print("bad luck, filepaths is invalid: %s " %(inpath))

    def getState(self):
        for item in self.pool_list:
            print("type: ", type(item))
            print("f result is: ", item.result());
            if item.result() is not 'finished':
                return -1
        return 0

    def close(self):
        self.threadPool.shutdown(wait=False)
        #self.exit = True
        for item in self.pool_list:
            print("cancel item")
            item.cancel()
            self.pool_list.remove(item)
