#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2016-2099 Ailemon.net
#
# This file is part of ASRT Speech Recognition Tool.
#
# ASRT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# ASRT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ASRT.  If not, see <https://www.gnu.org/licenses/>.
# ============================================================================

"""
@author: nl8590687
用于通过ASRT语音识别系统预测一次语音文件的程序
"""

import os

from speech_model import ModelSpeech
from speech_model_zoo import SpeechModel251
from speech_features import Spectrogram
from LanguageModel2 import ModelLanguage

def predict():

    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    AUDIO_LENGTH = 1600
    AUDIO_FEATURE_LENGTH = 200
    CHANNELS = 1
    # 默认输出的拼音的表示大小是1428，即1427个拼音+1个空白块
    OUTPUT_SIZE = 1428
    sm251 = SpeechModel251(
        input_shape=(AUDIO_LENGTH, AUDIO_FEATURE_LENGTH, CHANNELS),
        output_size=OUTPUT_SIZE
        )
    feat = Spectrogram()
    ms = ModelSpeech(sm251, feat, max_label_length=64)

    ms.load_model('save_models/' + sm251.get_model_name() + '.model.h5')
    print('save_models/' + sm251.get_model_name() + '.model.h5')
    #res = ms.recognize_speech_from_file('C:\\Users\\凉意\\Desktop\\lab3\\RecordedVoice-RealTime\\recordedVoice_before.wav')
    res = ms.recognize_speech_from_file('C:\\Users\\凉意\\Desktop\\lab3\\RecordedVoice\\1-3.wav')
    #print('*[提示] 声学模型语音识别结果：\n', res)

    ml = ModelLanguage('model_language')
    ml.LoadModel()
    str_pinyin = res
    #res = ml.SpeechToText(str_pinyin)
    #print('语音识别最终结果：\n',res)
    return res
print(predict())