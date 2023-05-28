import base64

def encode_image_to_url(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        url_encoded_data = 'data:image/jpeg;base64,' + base64_data  # 이미지 형식에 맞게 수정
        
    return url_encoded_data
  
  image_path = 'path/to/your/image.jpg'  # 인코딩할 이미지 파일 경로
  url = encode_image_to_url(image_path)
  print(url)
