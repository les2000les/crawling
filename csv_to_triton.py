import requests

# 트리톤 서버의 엔드포인트 URL
url = "http://<트리톤_서버_주소>/<추론_엔드포인트>"

# CSV 파일 경로
csv_file_path = "경로/파일명.csv"

# CSV 파일 열기
with open(csv_file_path, "rb") as file:
    # 파일을 요청 데이터에 첨부
    files = {"file": file}

    # POST 요청 보내기
    response = requests.post(url, files=files)

# 응답 확인
if response.status_code == 200:
    print("데이터 전송 성공")
else:
    print("데이터 전송 실패")
