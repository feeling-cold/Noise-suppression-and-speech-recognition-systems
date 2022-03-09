import tkinter
from tkinter import *
import tkinter.messagebox

import winsound

import alg_tts


class ttsWindow:
    def __init__(self, win, ww, wh):
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.title("语音合成模块")
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))
        self.img_src_path = None

        self.textlabe = Label(text="语音合成模块", fg="white", bg='black', font=("微软雅黑", 21))
        self.textlabe.place(x=420, y=35)

        self.text = Text(height=15, width=50)
        self.text.place(x=120, y=200)

        self.text2 = Text(height=15, width=50)
        self.text2.place(x=520, y=200)

        self.button1 = Button(self.win, text='合成语音', width=10, height=2, command=self.tts)
        self.button1.place(x=210, y=450)

        self.button2 = Button(self.win, text='存取合成音频', width=10, height=2, command=self.load)
        self.button2.place(x=335, y=450)

        self.button2 = Button(self.win, text='存取1号音频', width=10, height=2, command=self.loadone)
        self.button2.place(x=460, y=450)

        self.button2 = Button(self.win, text='存取2号音频', width=10, height=2, command=self.loadtwo)
        self.button2.place(x=585, y=450)

        self.button2 = Button(self.win, text='播放合成音频', width=10, height=2, command=self.play)
        self.button2.place(x=710, y=450)

    def tts(self):
        alg_tts.init()
        self.string1 = self.text.get('0.0', 'end')
        self.string2 = self.text2.get('0.0', 'end')
        alg_tts.ttsSpeak(self.string1)
        alg_tts.ttsSpeak(self.string2)

    def loadone(self):
        alg_tts.init()
        self.string1 = self.text.get('0.0', 'end')
        alg_tts.ttsSaveToFile(self.string1, "E:/audio/tts.wav")
        tkinter.messagebox.showinfo('提示','存储成功')

    def loadtwo(self):
        alg_tts.init()
        self.string1 = self.text2.get('0.0', 'end')
        alg_tts.ttsSaveToFile(self.string1, "E:/audio/tts2.wav")
        tkinter.messagebox.showinfo('提示','存储成功')

    def load(self):
        alg_tts.init()
        self.string1 = self.text.get('0.0', 'end')
        self.string2 = self.text2.get('0.0', 'end')
        alg_tts.ttsSaveToFile(self.string1+self.string2, "E:/audio/tts3.wav")
        tkinter.messagebox.showinfo('提示','存储成功')

    def play(self):
        int = self.text.get('0.0', 'end')
        if int == "1\n":
            #print("ok")
            filename = 'E:/audio/tts.wav'
            winsound.PlaySound(filename, winsound.SND_FILENAME)
        if int == "2\n":
            #print("ok")
            filename = 'E:/audio/tts2.wav'
            winsound.PlaySound(filename, winsound.SND_FILENAME)
        if int == "3\n":
            #print("ok")
            filename = 'E:/audio/tts3.wav'
            winsound.PlaySound(filename, winsound.SND_FILENAME)



if __name__ == '__main__':
    win = Tk()
    ww = 1000
    wh = 600
    img_gif = tkinter.PhotoImage(file="4.gif")
    label_img = tkinter.Label(win, image=img_gif, width="1000", height="600")
    label_img.place(x=0, y=0)
    ttsWindow(win, ww, wh)
    screenWidth, screenHeight = win.maxsize()
    geometryParam = '%dx%d+%d+%d' % (
        ww, wh, (screenWidth - ww) / 2, (screenHeight - wh) / 2)
    win.geometry(geometryParam)
    win.mainloop()
