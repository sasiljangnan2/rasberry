import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import circuit

def on_connect(client, userdata, flag, rc, prop=None):
	client.subscribe("textAlert") # "textalert" 토픽으로 구독 신청

def on_message(client, userdata, msg) : # 받은 메시지 txt
	file = open('./data/text.txt', 'w') # 추가 모드로 열기
	file.write(str(msg.payload,'utf-8'))
	file.close()
ip = "localhost" 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(ip, 1883) # 브로커에 연결
client.loop_forever()
client.disconnect()
