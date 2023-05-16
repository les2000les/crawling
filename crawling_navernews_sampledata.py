##########
#crawling_navernews.py를 함수로 정의하고 키워드로 샘플데이터를 추출하는 코드 
##########


def crawling(keyword, pagenum, daycount):
  ##########크롤링 라이브러리 호출##########
  from bs4 import BeautifulSoup
  import requests
  import re
  import sys
  import pandas as pd
  from datetime import datetime, timedelta
  from tqdm import tqdm

  #뉴스 크롤링 결과를 담을 리스트
  news_df_list = [] #크롤링 결과인 데이터프레임을 담을 리스트
  news_titles = []  #뉴스 제목
  news_url =[]  #뉴스 링크
  news_contents =[]  #뉴스 본문
  news_dates = []  #뉴스 날짜
  news_url_final = []  #네이버뉴스 필터링 후 제목, 링크, 내용 담을 리스트
  news_df_list = []

  ##########
  ##########함수정의##########
  #페이지 형식 변경 함수
  ##네이버 뉴스의 1, 2, 3, 4, ... 페이지 => 1, 11, 21, 31, ...
  def ChangePageNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num+1
    else:
        return num+9*(num-1)

  #크롤링할 네이버의 url 생성하는 함수
  ##검색어와 최대 페이지 수를 입력받음
  def makeUrl(search, maxpage, s_date, e_date):
  #def makeUrl(search, sort, maxpage, s_date, e_date): #검색옵션을 가지는 경우
        urls = []
        page = 1
        s_from = s_date.replace(".","") #시작일의 형식 변경
        e_to = e_date.replace(".","") #종료일의 형식 변경
        for i in range(page, maxpage + 1):
            page = ChangePageNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "&start=" + str(page)
            #url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&sort="+sort + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "&start=" + str(page) #검색옵션을 가지는 경우
            urls.append(url)
        print("생성url: ",urls)

        return urls

  # html에서 원하는 속성 추출하는 함수(기사, 추출할 속성값)
  def news_attrs_crawler(articles,attrs):
    attrs_content=[]
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content

  #html생성해서 기사크롤링하는 함수(url): 링크를 반환
  def articles_crawler(url):
    #requests.get()함수를 사용해서 'url'에 해당하는 웹페이지의 html을 추출함
    original_html = requests.get(i,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"})  #connection error 해결 #requests.get()함수를 사용해서 'url'에 해당하는 웹페이지의 html을 추출함
    html = BeautifulSoup(original_html.text, "html.parser") #추출한 html을 beautifulsoup 라이브러리를 사용해 파싱

    url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info") #필요부분 선택
    url = news_attrs_crawler(url_naver,'href') #추출한 링크의 속성을 가져옴

    return url

  #제목, 링크, 내용 1차원 리스트로 꺼내는 함수 생성
  def makeList(newlist, content):
    for i in content:
        for j in i:
            newlist.append(j)
    return newlist


  ##########
  ##########크롤링 시작##########

  ##########[1] 사용자로부터 입력을 받음 ##########
  #검색어 입력
  search = keyword#input("검색할 키워드를 입력하시오: ")
  maxpage = pagenum
  datenum = daycount
  ##검색옵션
  ##검색옵션의 디폴트는 관련도순
  ##본 프로젝트는 관련도 순으로 기사를 추출할 것이기 때문에 검색옵션 제외
  #sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")    #관련도순=0  최신순=1  오래된순=2

  
  #뉴스 페이지 수 입력
  #maxpage = 10 #int(input("\n크롤링할 기사의 페이지 수를 입력하시오(페이지당 최소 1개, 최대 10개): "))

  """시작일과 종료일을 지정할 경우
  #시작일 입력
  s_date = input("시작날짜 입력(YYYY.MM.DD):")  #2023.05.02
  #종료일 입력
  e_date = input("종료날짜 입력(YYYY.MM.DD):")   #2023.05.16"""

  """현재날짜를 기준으로 추출할 경우"""
  #추출할 날짜 수 입력
  #datenum = 7#int(input("\n추출할 날짜의 수를 입력하시오: "))
  
  #종료일 현재날짜
  e_date = datetime.today().strftime("%Y.%m.%d")
  #시작일 현재날짜
  s_date = (datetime.today() - timedelta(datenum)).strftime("%Y.%m.%d")

  print("\n")
  print("========================================")
  print("키워드: ", keyword)
  print("시작일: ", s_date)
  print("종료일: ", e_date)
  print("날짜 수: ", datenum)


  ##########[2] 네이버 뉴스 페이지의 url 생성 ##########
  # naver url 생성 (페이지 단위)
  url = makeUrl(search, maxpage, s_date, e_date)
  #url = makeUrl(search, sort, maxpage, s_date, e_date) #검색옵션이 있는 경우


  ##########[3] 추출한 페이지의 html에서 속성 추출 ########## 
  #각각의 뉴스 크롤러 실행해서 속성 추출
  for i in url:
    url = articles_crawler(url)
    news_url.append(url)

  #1차원 리스트로 만들기(내용 제외)
  makeList(news_url_final,news_url)


  ##########[4] 네이버 뉴스만 추출 ##########
  #네이버 뉴스만 추출
  #네이버 뉴스만 추출한 이유는 네이버뉴스의 형식에 맞는 크롤러만 사용했기 때문
  #네이버 뉴스가 아니라 각각의 신문사로 들어가는 링크일 경우 크롤러를 다 정의해야함
  final_urls = []
  for i in tqdm(range(len(news_url_final))):
    if "news.naver.com" in news_url_final[i]:
        final_urls.append(news_url_final[i])
    else:
        pass


  ##########[5] 뉴스 크롤링 ##########
  # 뉴스 내용 크롤링(제목, 본문)
  for i in tqdm(final_urls):
    #각 기사 html get하기
    news = requests.get(i,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}) #connection error 해결
    news_html = BeautifulSoup(news.text,"html.parser")

    # 뉴스 제목 크롤링
    title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
    if title == None:
        title = news_html.select_one("#content > div.end_ct > div > h2")
    
    # 뉴스 본문 크롤링
    content = news_html.select("div#dic_area")
    if content == []:
        content = news_html.select("#articeBody")

    # 기사 텍스트 추출 및 list 합치기
    content = ''.join(str(content))

    # 텍스트 전처리(html태그제거 및 텍스트 처리)
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1, repl='', string=str(title))
    content = re.sub(pattern=pattern1, repl='', string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    content = content.replace(pattern2, '')

    news_titles.append(title)
    news_contents.append(content)

    
    try:
        html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
        news_date = html_date.attrs['data-date-time']
    except AttributeError:
        news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
        news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
    
    # 날짜 추출
    news_dates.append(news_date)


  print("\n네이버 뉴스 필터링 후 기사 개수 :",len(final_urls))

  print("\n")
  print('news_title: ',len(news_titles))
  print('news_url: ',len(final_urls))
  print('news_contents: ',len(news_contents))
  print('news_dates: ',len(news_dates))
  print("\n")

  ##########
  ##########추출 결과 변환##########
  #딕셔너리 -> 데이터프레임
  news_df = pd.DataFrame({'date':news_dates,'title':news_titles,'link':final_urls,'content':news_contents})
  print("중복 제거 전 행 개수: ",len(news_df))
  #중복 행 제거
  news_df = news_df.drop_duplicates(keep='first',ignore_index=True)
  print("중복 제거 후 행 개수: ",len(news_df))

  #데이터프레임 ->csv
  #now = datetime.now() 
  #news_df.to_csv('{}_{}.csv'.format(search,datetime.now().strftime('%Y%m%d_%H시%M분%S초')),encoding='utf-8-sig',index=False)

  #unbuntu에서 데이터프레임 -> csv
  #news_df.to_csv('{}.csv'.format(search),encoding='utf-8-sig',index=False)
  return news_df
  
  
  
"""""""
##########
##########샘플데이터 키워드 지정##########
# https://msg.soledot.com/finance/fo/sisemarketsumlist.sd
#위의 사이트 참고해서 2023-05-16 기준으로 상위 20개 키워드 추출
StockList = ['삼성전자', 'lg에너지솔루션', 'sk하이닉스', '삼성바이오로직스', 'lg화학',
           '삼성sdi', '삼성전자우', '현대차', '기아', 'naver',
           'posco홀딩스', '카카오', '셀트리온','포스코퓨처엠', '현대모비스',
           '삼성물산', 'kb금융', 'lg전자', '신한지주', 'sk이노베이션']

""""""
##########
##########키워드 기준으로 샘플데이터 추출##########
maxpage = int(input("\n크롤링할 기사의 페이지 수를 입력하시오(페이지당 최소 1개, 최대 10개): "))
datenum = int(input("\n추출할 날짜의 수를 입력하시오: ")) 
news_keyword_list = []
news_df_list = []
for i in StockList:
  news_df = crawling(i, maxpage, datenum)
  for j in range(len(news_df)):
    news_keyword_list.append(i)
  news_df_list.append(news_df)
  
""""""
##########데이터프레임 결합##########
import pandas as pd
df_all = pd.concat(news_df_list, ignore_index=True)
df_all.insert(0,'keyword',news_keyword_list)

#데이터프레임 ->csv
#now = datetime.now() 
df_all.to_csv('sample_{}.csv'.format(search,datetime.now().strftime('%Y%m%d_%H시%M분%S초')),encoding='utf-8-sig',index=False)

#unbuntu에서 데이터프레임 -> csv
#news_df.to_csv('sample_{}.csv'.format(search),encoding='utf-8-sig',index=False)


