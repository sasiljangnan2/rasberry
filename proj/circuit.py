import time
import RPi.GPIO as GPIO
import io

global red_on 
red_on = 0

global blue_on
blue_on = 0
# LED를 켜고 끄는 함수
def controlAlert(on_off): # led 번호의 핀에 on_off(0/1) 값 출력하는 함수
	
	if (on_off == 0):
		repert_led()
	else :
		led_off()
# pin에 연결된 LED에 value(0/1) 값을 출력하여 LED를 켜거나 끄는 함수
def ledred_on():
	global red_on, blue_on
	GPIO.output(ledred, 1)
	GPIO.output(ledblue, 0)
	red_on = 1
	blue_on = 0
def ledblue_on():
	global red_on, blue_on
	GPIO.output(ledred, 0)
	GPIO.output(ledblue, 1)
	red_on = 0
	blue_on = 1
def led_off():
	global red_on, blue_on
	GPIO.output(ledred, 0)
	GPIO.output(ledblue, 0)
	red_on = 0
	blue_on = 0
# 초음파 센서를 제어하여 물체와의 거리를 측정하여 거리 값 리턴하는 함수

def measure_distance():
    global trig, echo
    time.sleep(0.2) # 초음파 센서의 준비 시간을 위해 200밀리초 지연
    GPIO.output(trig, 1) # trig 핀에 1(High) 출력
    GPIO.output(trig, 0) # trig 핀에 0(Low) 출력. High->Low. 초음파 발사 지시
    while(GPIO.input(echo) == 0): # echo 핀 값이 0->1로 바뀔 때까지 루프
        pass
    # echo 핀 값이 1이면 초음파가 발사되었음
    pulse_start = time.time() # 초음파 발사 시간 기록
    while(GPIO.input(echo) == 1): # echo 핀 값이 1->0으로 바뀔 때까지 루프
        pass
    pulse_end = time.time() # 초음파가 되돌아 온 시간 기록
    pulse_duration = pulse_end - pulse_start # 경과 시간 계산
    return pulse_duration*340*100/2 # 거리 계산하여 리턴(단위 cm)

def repert_led():
	global red_on, blue_on
	if (red_on == 0):
		ledred_on()
	elif (blue_on == 0):
		ledblue_on()

# LED 상태를 확인하는 편의 함수들
def is_red_on():
	try:
		return bool(GPIO.input(ledred))
	except Exception:
		return bool(red_on)

def is_blue_on():
	try:
		return bool(GPIO.input(ledblue))
	except Exception:
		return bool(blue_on)

def get_led_states():
	"""Return dict with current LED states: {'red': bool, 'blue': bool}."""
	return {'red': is_red_on(), 'blue': is_blue_on()}


# 초음파 센서를 다루기 위한 전역 변수 선언 및 초기화
trig = 20 # GPIO20
echo = 16 # GPIO16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT) # GPIO20 핀을 출력으로 지정
GPIO.setup(echo, GPIO.IN) # GPIO16 핀을 입력으로 지정

# LED를 다루기 위한 전역 변수 선언 및 초기화
ledred = 6 # GPIO6
ledblue =13
GPIO.setup(ledred, GPIO.OUT) # GPIO6 핀을 출력으로 지정
GPIO.setup(ledblue, GPIO.OUT) # GPIO13 핀을 출력으로 지정

