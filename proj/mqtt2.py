import paho.mqtt.client as mqtt
import playmp3 as playmp3

def on_connect(client, userdata, flag, rc, prop=None):
	client.subscribe("textAlert") # "textalert" 토픽으로 구독 신청

def on_message(client, userdata, msg) : # 받은 메시지를 txt로 저장하고 메시지를 tts화해 mp3로 변환 후 실행
	string = str(msg.payload,'utf-8') # 받은 메시지 문자열로 변환
	file = open('./data/text.txt', 'w') # 쓰기 모드로 열기
	file.write(string)
	playmp3.speak(string) # 메시지를 tts화해 mp3로 변환 후 실행
	file.close()
ip = "localhost" 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(ip, 1883) # 브로커에 연결
client.loop_forever()
client.disconnect()
