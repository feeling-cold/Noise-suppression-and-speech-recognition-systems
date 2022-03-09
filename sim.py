import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


a = string_similar('jinjinbiaotiao', 'jinjinyoutiao')
print(a)
if  a >= 0.5:
    res = 1
    print (1)

'''
import librosa
import soundfile as sf
for i in range(1,101):
    #name = "LJ001-"+str( "%04d"%(i) )+".wav"
    name = "E:\\audio\\tts.wav"
    src_sig,sr = sf.read(name)  #name是要 输入的wav 返回 src_sig:音频数据  sr:原采样频率
    dst_sig = librosa.resample(src_sig,sr,16000)  #resample 入参三个 音频数据 原采样频率 和目标采样频率
    sf.write(name,dst_sig,16000) #写出数据  参数三个 ：  目标地址  更改后的音频数据  目标采样数据
'''