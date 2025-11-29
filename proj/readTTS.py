import speech_recognition as sr

from gtts import gTTS

import os

import time

import vlc


def speak(text):

     tts = gTTS(text=text, lang='ko')

     filename='alerttext'

     tts.save('./data/%s.mp3' % filename)

     p = vlc.MediaPlayer('./data/%s.mp3' % filename)
     
     p.play()