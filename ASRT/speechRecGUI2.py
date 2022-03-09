import os
import tkinter
import wave
from tkinter import *
import tkinter.messagebox
import pyaudio
import winsound
from tqdm import tqdm
import ASRT
from ASRT import speech_model

from ASRT.predict_speech_file import predict


class srWindow:
    def __init__(self, win, ww, wh):
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.title("语音识别模块")
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))
        self.img_src_path = None

        self.textlabe = Label(text="语音识别模块", fg="white", bg='black', font=("微软雅黑", 21))
        self.textlabe.place(x=420, y=35)

        self.text = Text(height=15, width=50)
        self.text.place(x=325, y=180)

        self.button1 = Button(self.win, text='开始录音', width=10, height=2, command=self.pyaudio)
        self.button1.place(x=325, y=450)

        self.button3 = Button(self.win, text='播放录音', width=10, height=2, command=self.play)
        self.button3.place(x=465, y=450)

        self.button2 = Button(self.win, text='开始识别', width=10, height=2, command=self.speechrec)
        self.button2.place(x=605, y=450)

    def play(self):
        filename = 'E:/audio/speech.wav'
        winsound.PlaySound(filename, winsound.SND_FILENAME)

    def pyaudio(self):
        wave_out_path = "E:/audio/speech.wav"
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
        tkinter.messagebox.showinfo('提示', '存储成功')


    def speechrec(self):
        res = predict()
        self.text.insert('end',res)

if __name__ == '__main__':
    win = Tk()
    ww = 1000
    wh = 600
    img_gif = tkinter.PhotoImage(file="3.gif")
    label_img = tkinter.Label(win, image=img_gif, width="1000", height="600")
    label_img.place(x=0, y=0)
    srWindow(win, ww, wh)
    screenWidth, screenHeight = win.maxsize()
    geometryParam = '%dx%d+%d+%d' % (
        ww, wh, (screenWidth - ww) / 2, (screenHeight - wh) / 2)
    win.geometry(geometryParam)
    win.mainloop()
