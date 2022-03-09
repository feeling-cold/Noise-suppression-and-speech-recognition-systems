import pyttsx3


def init(rate=125, volume=1.0, voice='zh'):
    global engine
    engine = pyttsx3.init() # object creation

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    print (rate)                        #printing current voice rate
    engine.setProperty('rate', rate)     # setting up new voice rate


    """VOLUME"""
    volume = engine.getProperty('volume')
    print (volume)
    engine.setProperty('volume',volume)

    """VOICE"""
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voice)

def ttsSpeak(text):
    global engine
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def ttsSaveToFile(text, filename):
    global engine
    """Saving Voice to a file"""
    engine.save_to_file(text, filename)
    engine.runAndWait()
    engine.stop()
