#pip install flask
from flask import Flask, render_template  #html 파일 렌더링 메소드


app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello'

@app.route('/coder')
def coder():
    return 'I am AutoCoder.'

#.py가 실행되는 경로 안에 'templates' 폴더 생성 수 그 안에 test.html 파일 넣어두기
@app.route('/autocoder')
def autocoder():
    return render_template("test.html")


def main():
    app.run(host = '127.0.0.1', debug=True, port = 80)

if __name__ == '__main__':
    main()
