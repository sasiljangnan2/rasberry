import time
import paho.mqtt.client as mqtt
import circuit 
import RPi.GPIO as GPIO
import cv2
import camera
'''
camera = cv2.VideoCapture(0, cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# 프레임을 임시 저장할 버퍼 개수를 1로 설정
buffer_size = 1
camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)'''
camera.init(width=640, height=480)
red_on = 0
blue_on = 0
def on_connect(client, userdata, flag, rc, prop=None):
	client.subscribe("alert") # "alert" 토픽으로 구독 신청

def on_message(client, userdata, msg) :
	on_off = int(msg.payload); # on_off는 0 또는 1의 정수
	circuit.controlAlert(on_off) # LED를 켜거나 끔

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
		image = camera.take_picture(most_recent=True)
		if image is not None:
			cv2.imwrite('./static/cctv.jpg', image)
		distance = circuit.measure_distance() # 초음파 센서로부터 거리 읽기
		client.publish("ultrasonic", distance) # “ultrasonic” 토픽으로 거리 전송
		time.sleep(0.5) # 1초 동안 잠자기
		if distance < 20 : # 물체와의 거리가 10cm 이내이면
			nowtime = time.strftime('%Y-%m-%d%H:%M:%S') # 현재 시간 저장
			file = open('./data/alert.txt', 'a') # 추가 모드로 열기
			data = "%s,%s\n" % (nowtime, distance) # data에 date,dis 형식으로 저장
			cv2.imwrite('./static/image_%s.jpg'% nowtime, image) # data에 image+날짜 이름으로 저장 
			file.write(data) # 파일에 저장
			file.close()
			circuit.repert_led()
		else:
			circuit.led_off()
		if (circuit.controlAlert() == 1):
			circuit.repert_led()
		else :
			circuit.led_off()
except KeyboardInterrupt:
    print("종료")
finally:
	print("cleanup")
	GPIO.cleanup()
client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
