import time
import paho.mqtt.client as mqtt
import circuit 
import RPi.GPIO as GPIO
import camera
import playmp3 as playmp3
import cv2

camera.init(width=640, height=480)
playmp3.initsound('./data/alertsound.mp3')
def on_connect(client, userdata, flag, rc, prop=None):
	client.subscribe("doAlert") # "doalert" 토픽으로 구독 신청

def on_message(client, userdata, msg) :
    on_off = int(msg.payload); # on_off는 0 또는 1의 정수
    circuit.controlAlert(on_off)
ip = "localhost" # 현재 브로커는 이 컴퓨터에 설치되어 있음
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(ip, 1883) # 브로커에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

# 도착하는 메시지는 on_message() 함수에 의해 처리되어 경보상태를 켜거나 끄는 작업과
# 병렬적으로 1초 단위로 초음파 센서로부터 거리를 읽어 전송하는 무한 루프 실행
try:
	while True:
		image = camera.take_picture(most_recent=True)
		if image is not None:
			cv2.imwrite('./static/cctv.jpg', image) # 사진을 0.5초마다 찍어 실시간 cctv 구현을 위해 사용
		distance = circuit.measure_distance() # 초음파 센서로부터 거리 읽기
		client.publish("ultrasonic", distance) # “ultrasonic” 토픽으로 거리 전송
		time.sleep(0.5) # 1초 동안 잠자기
		if distance < 20: # 물체와의 거리가 50cm 이내이면
			nowtime = time.strftime('%Y-%m-%d%H:%M:%S') # 현재 시간 저장
			file = open('./data/alert.txt', 'a') # 추가 모드로 열기
			data = "%s,%s\n" % (nowtime, distance) # data에 date,dis 형식으로 저장
			cv2.imwrite('./static/image_%s.jpg'% nowtime, image) # camera에 image+날짜 이름으로 저장 
			file.write(data) # 파일에 저장
			file.close()
			if circuit.doAlert() == 1: # 경보 상태라면 led 반복 점등과 경보 소리 실행
				circuit.repert_led()
				playmp3.playsound()
		if circuit.doAlert() == 0 : # 경보 상태가 아니라면 
			circuit.led_off()
			playmp3.stopsound()
except KeyboardInterrupt:
    print("종료")
finally:
	print("cleanup")
	GPIO.cleanup()
client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
