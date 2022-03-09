import signal
import time
import tkinter
import wave
from tkinter import *
import tkinter.messagebox

import librosa
import numpy as np
import pyaudio
import winsound
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import wavfile
from tqdm import tqdm
import soundfile as sf


import alg_denoise
import alg_tts
from denoise import sigint_handler


class FFTWindow:
    def __init__(self, win, ww, wh):
        self.fig = fig = Figure(figsize=(4, 3), dpi=80)
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.title("FFT降噪模块")
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))
        self.img_src_path = None

        self.textlabe = Label(text="FFT降噪模块", fg="white", bg='black', font=("微软雅黑", 21))
        self.textlabe.place(x=420, y=35)

        self.canvas = FigureCanvasTkAgg(fig, win)
        self.canvas.get_tk_widget().place(x=140, y=130)

        self.canvas2 = FigureCanvasTkAgg(fig, win)
        self.canvas2.get_tk_widget().place(x=560, y=130)

        self.button = Button(self.win, text='开始录音', width=10, height=2, command=self.start)
        self.button.place(x=183, y=450)

        self.button1 = Button(self.win, text='添加白噪', width=10, height=2, command=self.noise)
        self.button1.place(x=300, y=450)

        self.button2 = Button(self.win, text='FFT降噪', width=10, height=2, command=self.denoise)
        self.button2.place(x=417, y=450)

        self.button3 = Button(self.win, text='播放原音频', width=10, height=2, command=self.play)
        self.button3.place(x=534, y=450)

        self.button4 = Button(self.win, text='播放降噪音频', width=10, height=2, command=self.playdeno)
        self.button4.place(x=650, y=450)

        self.button5 = Button(self.win, text='播放加噪音频', width=10, height=2, command=self.playno)
        self.button5.place(x=763, y=450)


    def noise(self):
        rate, data = wavfile.read(r'E:/audio/FFTpyaudio.wav')
        noise = np.random.normal(0, 500, data.shape)
        newaudio = data + noise
        wavfile.write("E:/audio/FFTnoise.wav", rate, newaudio.astype(np.int16))
        tkinter.messagebox.showinfo('提示', '存储成功')
        #self.clear2()
        axc = self.fig.add_subplot(111)
        axc.set_xticks([])
        axc.set_yticks([])
        axc.plot(newaudio, 'g')
        self.canvas2.draw()

    def start(self):
        wave_out_path = "E:/audio/FFTpyaudio.wav"
        record_second = 5
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        wf = wave.open(wave_out_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        print("* recording")
        for i in tqdm(range(0, int(RATE / CHUNK * record_second))):
            data = stream.read(CHUNK)
            wf.writeframes(data)
        print("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()
        tkinter.messagebox.showinfo('提示', '录制成功')
        #self.clear1()
        rate, data = wavfile.read(r'E:/audio/FFTpyaudio.wav')
        axc = self.fig.add_subplot(111)
        axc.set_xticks([])
        axc.set_yticks([])
        axc.plot(data)
        self.canvas.draw()

    def denoise(self):
        file = r'E:/audio/FFTnoise.wav'
        sig, fs = librosa.load(file, sr=50000)

        # Filtering
        dt = 1 / fs
        t = np.arange(0, 6, dt)
        n = len(t)

        fhat = np.fft.fft(sig, n)  # Compute the FFT
        PSD = fhat * np.conj(fhat) / n  # Power spectrum (power per freq)
        freq = (1 / (dt * n)) * np.arange(n)  # Create x-axis of frequencies in Hz
        L = np.arange(1, np.floor(n / 20), dtype='int')
        indices = PSD > 0.1  # Find all freqs with large power
        PSDclean = PSD * indices  # Zero out all others
        fhat = indices * fhat  # Zero out small Fourier coeffs.
        ffilt = np.fft.ifft(fhat)

        nsig = ffilt.real
        abs_spectrogram = np.abs(librosa.stft(nsig))
        audio_signal = librosa.griffinlim(abs_spectrogram)
        sf.write('E:/audio/FFTdenoise.wav', audio_signal, fs)
        tkinter.messagebox.showinfo('提示', '存储成功')

        rate, data = wavfile.read(r'E:/audio/FFTdenoise.wav')
        axc = self.fig.add_subplot(111)
        axc.set_xticks([])
        axc.set_yticks([])
        axc.plot(data)
        self.canvas.draw()


    def playdeno(self):
        filename = 'E:/audio/FFTdenoise.wav'
        winsound.PlaySound(filename, winsound.SND_FILENAME)

    def play(self):
        filename = 'E:/audio/FFTpyaudio.wav'
        winsound.PlaySound(filename, winsound.SND_FILENAME)

    def playno(self):
        filename = 'E:/audio/FFTnoise.wav'
        winsound.PlaySound(filename, winsound.SND_FILENAME)

    def clear1(self):
        self.canvas.get_tk_widget().delete(tkinter.ALL)

    def clear2(self):
        self.canvas2.get_tk_widget().delete(tkinter.ALL)


if __name__ == '__main__':
    win = Tk()
    ww = 1000
    wh = 600
    img_gif = tkinter.PhotoImage(file="5.gif")
    label_img = tkinter.Label(win, image=img_gif, width="1000", height="600")
    label_img.place(x=0, y=0)
    FFTWindow(win, ww, wh)
    screenWidth, screenHeight = win.maxsize()
    geometryParam = '%dx%d+%d+%d' % (
        ww, wh, (screenWidth - ww) / 2, (screenHeight - wh) / 2)
    win.geometry(geometryParam)
    win.mainloop()