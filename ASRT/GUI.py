import tkinter

from ASRT.speechRecGUI2 import srWindow
from FFTGUI import FFTWindow
from denoGUI import denoWindow
from ttsGUI import ttsWindow

def FFTGUI():
    root.destroy()
    win = tkinter.Tk()
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

def speechrecGUI():
    root.destroy()
    win = tkinter.Tk()
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


def ttsGUI():
    root.destroy()
    win = tkinter.Tk()
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

def denoiseGUI():
    root.destroy()
    win = tkinter.Tk()
    ww = 1000
    wh = 600
    img_gif = tkinter.PhotoImage(file="2.gif")
    label_img = tkinter.Label(win, image=img_gif, width="1000", height="600")
    label_img.place(x=0, y=0)
    denoWindow(win, ww, wh)
    screenWidth, screenHeight = win.maxsize()
    geometryParam = '%dx%d+%d+%d' % (
        ww, wh, (screenWidth - ww) / 2, (screenHeight - wh) / 2)
    win.geometry(geometryParam)
    win.mainloop()

root = tkinter.Tk()
root.title('语音识别系统')
root.resizable(False, False)
windowWidth = 1000
windowHeight = 600
screenWidth, screenHeight = root.maxsize()
geometryParam = '%dx%d+%d+%d' % (
    windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
root.geometry(geometryParam)
root.wm_attributes('-topmost', 1)  # 窗口置顶

img_gif = tkinter.PhotoImage(file="1.gif")
label_img = tkinter.Label(root, image=img_gif, width="1000", height="600")
label_img.place(x=0, y=0)

textlabe = tkinter.Label(text="语音识别系统", fg="white", bg='midnightblue',
                         font=("微软雅黑", 28))
textlabe.place(x=400, y=40)

button1 = tkinter.Button(text="语音识别", width="10", height="2", bg="DimGray",command = speechrecGUI)
button1.place(x=210, y=500)
button3 = tkinter.Button(text="FFT降噪", width="10", height="2", bg="DimGray",command = FFTGUI)
button3.place(x=383,y = 500)
button = tkinter.Button(text="语音降噪", width="10", height="2", bg="DimGray",command = denoiseGUI)
button.place(x=556, y=500)
button2 = tkinter.Button(text="语音合成", width="10", height="2", bg="DimGray",command = ttsGUI)
button2.place(x=730, y=500)

root.mainloop()
