import signal
import time
import tkinter
import wave
from tkinter import *
import tkinter.messagebox
import pyaudio
import winsound
from tqdm import tqdm

import alg_denoise
import simpleaudio as sa
import alg_tts
from denoise import sigint_handler


class denoWindow:
    def __init__(self, win, ww, wh):
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.title("语音降噪模块")
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))
        self.img_src_path = None

        self.textlabe = Label(text="语音降噪模块", fg="white", bg='black', font=("微软雅黑", 21))
        self.textlabe.place(x=420, y=35)

        self.button = Button(self.win, text='开始录音', width=10, height=2, command=self.start)
        self.button.place(x=183, y=450)

        self.button1 = Button(self.win, text='加噪处理', width=10, height=2, command=self.noise)
        self.button1.place(x=300, y=450)

        self.button2 = Button(self.win, text='降噪处理', width=10, height=2, command=self.denoise)
        self.button2.place(x=417, y=450)

        self.button3 = Button(self.win, text='播放原音频', width=10, height=2, command=self.play)
        self.button3.place(x=534, y=450)


        self.button4 = Button(self.win, text='播放降噪音频', width=10, height=2, command=self.playdeno)
        self.button4.place(x=650, y=450)

        self.button5 = Button(self.win, text='播放加噪音频', width=10, height=2, command=self.playno)
        self.button5.place(x=763, y=450)

    def noise(self):
        global objDenoise, exit
        exit = False
        signal.signal(signal.SIGINT, sigint_handler)
        objDenoise = alg_denoise.espDenoise()
        objDenoise.initWiener()
        objDenoise.denoiseWiener("E:/audio/pyaudio.wav", "E:/audio/doing_the_dishes.wav",  "E:/audio/noise.wav") #加噪
        while exit is False:
            if objDenoise.getState() == -1:
                time.sleep(0.5)
                print("state runing, wait")
                continue
            else:
                break
        #print("going to exit")
        objDenoise.close()
        tkinter.messagebox.showinfo('提示', '存储成功')

    def start(self):
        wave_out_path = "E:/audio/pyaudio.wav"
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
        tkinter.messagebox.showinfo('提示', '处理成功')

    def denoise(self):
        global objDenoise, exit
        exit = False
        signal.signal(signal.SIGINT, sigint_handler)
        objDenoise = alg_denoise.espDenoise()
        objDenoise.initWiener()
        objDenoise.denoiseWienerOneInput("E:/audio/pyaudio.wav", "E:/audio/denoise.wav")  # 减噪


        while exit is False:
            if objDenoise.getState() == -1:
                time.sleep(0.5)
                print("state runing, wait")
                continue
            else:
                break

        #print("going to exit")
        objDenoise.close()
        #print("exit main program")
        tkinter.messagebox.showinfo('提示', '处理成功')

    def playdeno(self):
        filename = 'E:/audio/denoise.wav'
        winsound.PlaySound(filename, winsound.SND_FILENAME)

    def play(self):
        filename = 'E:/audio/pyaudio.wav'
        winsound.PlaySound(filename, winsound.SND_FILENAME)

    def playno(self):
        filename = 'E:/audio/noise.wav'
        winsound.PlaySound(filename, winsound.SND_FILENAME)

if __name__ == '__main__':
    win = Tk()
    ww = 1000
    wh = 600
    img_gif = tkinter.PhotoImage(file="2.gif")
    label_img = tkinter.Label(win, image=img_gif, width="998", height="600")
    label_img.place(x=0, y=0)
    denoWindow(win, ww, wh)
    screenWidth, screenHeight = win.maxsize()
    geometryParam = '%dx%d+%d+%d' % (
        ww, wh, (screenWidth - ww) / 2, (screenHeight - wh) / 2)
    win.geometry(geometryParam)
    win.mainloop()
