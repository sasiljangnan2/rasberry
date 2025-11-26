import cv2
camera = None
def init(camera_id = -1, width=640, height=480,buffer_size=1):
	global camera
	# 카메라 객체를 생성하고 촬영한 사진 크기를 640x480으로 설정
	camera = cv2.VideoCapture(camera_id, cv2.CAP_V4L)
	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	# 프레임을 임시 저장할 버퍼 개수를 1로 설정
	buffer_size = 1
	camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
def take_picture(most_recent=False):
	global camera
	len = 0 if most_recent == False else camera.get(cv2.CAP_PROP_BUFFERSIZE)
	while len > 0: # 버퍼 내에 저장된 모든 프레임을 버린다
		camera.read( ) 
		len -= 1
	ret, frame = camera.read( ) # 버퍼에 있는 현재 프레임을 읽는다.
	return frame if ret == True else None

def final():
	if camera != None:
		camera.release()
camera = None