import sys, time, signal, os
import alg_denoise

def sigint_handler(signum, frame):
    global objDenoise, exit
    exit = True
    objDenoise.close()
    print("exit sigint handle")
    #sys.exit(0)

if __name__ == '__main__':
    global objDenoise, exit
    exit = False

    signal.signal(signal.SIGINT, sigint_handler)

    objDenoise = alg_denoise.espDenoise()
    objDenoise.initWiener()
    '''
    objDenoise.denoiseWiener(os.path.join(os.path.dirname(__file__),"cmu_arctic_us_aew_a0001.wav"), 
            os.path.join(os.path.dirname(__file__),"doing_the_dishes.wav"), 
            os.path.join(os.path.dirname(__file__),"output_wiener.wav"))
    '''
    objDenoise.denoiseWiener("output.wav", "doing_the_dishes.wav",  "output_wiener.wav") #加噪

    #objDenoise.denoiseWienerOneInput("2.wav",  "denoise.wav") #减噪

    '''
    objDenoise.initSpectralSubtraction()
    objDenoise.denoiseSpectralSubtraction("cmu_arctic_us_aew_a0001.wav", "doing_the_dishes.wav",  "output_spetral.wav")
    objDenoise.denoiseSpectralSubtractionOneInput("denoise_input_SpectralSubtraction.wav", "output_spetral_2.wav")

    objDenoise.initSubspace(mu=500)
    objDenoise.denoiseSubspace("cmu_arctic_us_aew_a0001.wav", "doing_the_dishes.wav", "output_subspace.wav")
    objDenoise.denoiseSubspaceOneInput("denoise_input_Subspace.wav", "output_subspace_2.wav")
    '''
    #m = input("press <ENTER> to exit: \n")

    while exit is False:
        if objDenoise.getState() == -1:
            time.sleep(0.5)
            print("state runing, wait")
            continue
        else:
            break

    print("going to exit")
    objDenoise.close()

    print("exit main program")
