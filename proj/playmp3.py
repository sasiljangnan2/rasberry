#import speech_recognition as sr
from gtts import gTTS
import vlc
global p
p = None
def playspeak(text):
     tts = gTTS(text=text, lang='ko')
     filename='alerttext'
     tts.save('./data/%s.mp3' % filename) # 변환된 tts를 mp3으로 저장 
     t = vlc.MediaPlayer('./data/%s.mp3' % filename) 
     t.play() # mp3 실행
def initsound(mp3): # 실행할 mp3 초기화 함수
     global p
     p = vlc.MediaPlayer(mp3) 
def playsound(): # mp3을 실행하는 함수
     global p
     p.play()
def stopsound(): # 실행되는 mp3를 멈추는 함수
     global p
     p.stop()
