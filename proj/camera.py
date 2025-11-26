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
def take_picture():
	global camera
	size = camera.get(cv2.CAP_PROP_BUFFERSIZE) # 버퍼 크기를 읽어온다
	while size > 0: # 버퍼 내에 저장된 모든 프레임을 버린다
		camera.grab( ) # camera.read( )로 해도 됨
		size -= 1
	ret, frame = camera.read( ) # 버퍼에 있는 현재 프레임을 읽는다.
	return frame if ret == True else None

def final():
	if camera != None:
		camera.release()
camera = None