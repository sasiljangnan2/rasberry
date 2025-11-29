import speech_recognition as sr

from gtts import gTTS

import os

import time

import playsound


def speak(text):

     tts = gTTS(text=text, lang='ko')

     filename='alerttext.mp3'

     tts.save('/data/%s.mp3' % filename)

     playsound.playsound('/data/%s.mp3' % filename)