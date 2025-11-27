from flask import Flask, render_template, request

# 자바스크립트 코드나 이미지 파일 등에 대해
# 브라우저에게 캐시에 저장한 파일을 사용하지 않도록 지시.
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
def index():
	return render_template('alert.html')
@app.route('/cctv')
def cctv():
    return render_template('cctv.html')
@app.route('/view', methods=['GET']) # 전화번호 전체 보기
def view():
    alertdata = {} # 빈 딕셔너리 생성
    file = open('./data/alert.txt', 'r') # 읽기 모드로 열기
    for line in file.readlines(): # 한 줄씩 읽기
        data = line.strip().split(',') # , 기준으로 나누어서 data[0], data[1]에 저장
        alertdata[data[0]] = data[1] # 딕셔너리에 이름, 전화번호 저장
    file.close()
    return render_template('view.html', alertdata=alertdata)
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
