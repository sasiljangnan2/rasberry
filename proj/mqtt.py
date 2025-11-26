import time
import paho.mqtt.client as mqtt
import circuit 
import RPi.GPIO as GPIO
import cv2
import camera
camera = cv2.VideoCapture(0, cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# 프레임을 임시 저장할 버퍼 개수를 1로 설정
buffer_size = 1
camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
red_on = 0
blue_on = 0
def on_connect(client, userdata, flag, rc, prop=None):
	client.subscribe("led") # "led" 토픽으로 구독 신청

def on_message(client, userdata, msg) :
	on_off = int(msg.payload); # on_off는 0 또는 1의 정수
	circuit.controlLED(on_off) # LED를 켜거나 끔

ip = "localhost" # 현재 브로커는 이 컴퓨터에 설치되어 있음

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(ip, 1883) # 브로커에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

# 도착하는 메시지는 on_message() 함수에 의해 처리되어 LED를 켜거나 끄는 작업과
# 병렬적으로 1초 단위로 초음파 센서로부터 거리를 읽어 전송하는 무한 루프 실행
try:
	while True:
		distance = circuit.measure_distance() # 초음파 센서로부터 거리 읽기
		client.publish("ultrasonic", distance) # “ultrasonic” 토픽으로 거리 전송
		time.sleep(1) # 1초 동안 잠자기
		if distance < 20 : # 물체와의 거리가 10cm 이내이면
			#image = camera.take_picture()
			for i in range(buffer_size+1): 
				ret, frame = camera.read()
			if ret is not None:
				cv2.imwrite('./data/cctv.jpg', frame)
			if (red_on == 0) :
				circuit.ledred_on()
				red_on = 1
				blue_on = 0
			elif (blue_on == 0):
				circuit.ledblue_on()
				red_on = 0
				blue_on = 1
		else:
			circuit.led_off()
except KeyboardInterrupt:
	print("Ctrl+C 종료")
finally:
	print("cleanup")
	GPIO.cleanup()
client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
