from flask import Flask, render_template, request
import camera
import cv2
# 자바스크립트 코드나 이미지 파일 등에 대해
# 브라우저에게 캐시에 저장한 파일을 사용하지 않도록 지시
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
def index():
	return render_template('11-4.html')
@app.route('/cctv')
def cctv():
    image = camera.take_picture(most_recent=True)
    if image is not None:
        cv2.imwrite('/data/cctv.jpg', image)
        return render_template('11-4.html',fname='/data/cctv.jpg')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
