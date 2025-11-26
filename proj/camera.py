import cv2
def init():
	global camera
	# 카메라 객체를 생성하고 촬영한 사진 크기를 640x480으로 설정
	camera = cv2.VideoCapture(0, cv2.CAP_V4L)
	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	# 프레임을 임시 저장할 버퍼 개수를 1로 설정
	buffer_size = 1
	camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
def take_picture(most_recent=False):
	global camera
	len = 0
	while(len > 0):
		camera.grab()
		len -=1
		success, image = camera.read()
		if not success:
			return None
		return image
def final():
	if camera != None:
		camera.release()
camera = None