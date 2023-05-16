import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

summary = [] #요약된 본문을 담을 리스트
for i in news_df['content']:
  text = i.replace('\n', ' ') #개행문자 전처리: 개행
  raw_input_ids = tokenizer.encode(text) #text를 모델이 인식할 수 있는 토큰 형태로 바꿔줌
  #print(raw_input_ids) #텍스트가 토큰 단위로 나뉘고 모두 id 형태의 숫자로 바뀜, 0: 문자시작, 1: 문자종료
  input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id] # 시작 토큰(ID 0)과 종료 토큰(ID 1)을 추가하여 입력 토큰 시퀀스를 구성
  #num_beams: beam search 개수, max_length: 요약의 최대 길이, eos_token_id: 종료 토큰 id
  try: 
    summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=512,  eos_token_id=1) #generate 메소드를 이용해 요약문 생성
    summary.append(tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)) #토크나이저를 통해 id형태를 텍스트 형태로 바꿈
    #squeeze() : 1차원 텐서의 크기 변환, tolist(): 리스트로 변환
  except IndexError: #예외처리 : 인덱스 에러나는 부분
    summary.append('indexerror')
