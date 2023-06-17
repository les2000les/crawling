import datetime
from bs4 import BeautifulSoup
import requests
import re
import sys
import pandas as pd
from tqdm import tqdm


def crawling(keyword, day, page):
    # 뉴스 크롤링 결과를 담을 리스트
    news_titles = []  # 뉴스 제목
    news_url = []  # 뉴스 링크
    news_contents = []  # 뉴스 본문
    news_dates = []  # 뉴스 날짜
    news_url_final = []  # 네이버뉴스 필터링 후 제목, 링크, 내용 담을 리스트

    # 페이지 형식 변경 함수
    def ChangePageNum(num):
        if num == 1:
            return num
        elif num == 0:
            return num + 1
        else:
            return num + 9 * (num - 1)

    # 크롤링할 네이버의 url 생성하는 함수
    def makeUrl(search, maxpage, s_date, e_date):
        urls = []
        page = 1
        s_from = s_date.replace(".", "")  # 시작일의 형식 변경
        e_to = e_date.replace(".", "")  # 종료일의 형식 변경
        for i in range(page, maxpage + 1):
            page = ChangePageNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "&start=" + str(page)
            urls.append(url)
        print("생성url: ", urls)
        return urls

    # html에서 원하는 속성 추출하는 함수(기사, 추출할 속성값)
    def news_attrs_crawler(articles, attrs):
        attrs_content = []
        for i in articles:
            attrs_content.append(i.attrs[attrs])
        return attrs_content

    # html생성해서 기사크롤링하는 함수(url): 링크를 반환
    def articles_crawler(url):
        original_html = requests.get(i, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"})
        html = BeautifulSoup(original_html.text, "html.parser")
        url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
        url = news_attrs_crawler(url_naver, 'href')
        return url

    # 제목, 링크, 내용 1차원 리스트로 꺼내는 함수 생성
    def makeList(newlist, content):
        for i in content:
            for j in i:
                newlist.append(j)
        return newlist

    ##########
    ##########크롤링 시작##########

    # 검색어 입력
    search = keyword
    # 뉴스 페이지 수 입력
    maxpage = int(input("\n크롤링할 기사의 페이지 수를 입력하시오(페이지당 최소 1개, 최대 10개): "))

    """시작일과 종료일을 직접 입력할 경우"""
    # s_date = input("시작일을 입력하세요(예: 2021.01.01):")
    # e_date = input("종료일을 입력하세요(예: 2021.12.31):")

    """현재날짜를 기준으로 추출할 경우"""
    # 추출할 날짜 수 입력
    datenum = int(input("\n추출할 날짜의 수를 입력하시오: "))
    # 종료일 현재날짜
    e_date = datetime.datetime.today().strftime("%Y.%m.%d")
    # 시작일 현재날짜
    s_date = (datetime.datetime.today() - datetime.timedelta(datenum)).strftime("%Y.%m.%d")

    urls = makeUrl(search, maxpage, s_date, e_date)

    print("\n크롤링 중...")

    for i in tqdm(urls):
        html = requests.get(i, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"})
        soup = BeautifulSoup(html.text, 'html.parser')
        articles = soup.select('.group_news > ul.list_news > li')
        # 뉴스 날짜
        dates = news_attrs_crawler(articles, 'data-date')
        # 뉴스 제목
        titles = news_attrs_crawler(articles, 'title')
        # 뉴스 링크
        links = articles_crawler(articles)
        # 뉴스 내용
        contents = []

        for link in links:
            try:
                content_html = requests.get(link, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"})
                soup = BeautifulSoup(content_html.text, "html.parser")

                # 뉴스 본문 추출
                content = soup.select_one("#articleBodyContents").text.replace("\n", " ").replace("\t", " ").strip()
                contents.append(content)

            except Exception as e:
                contents.append("본문을 가져오지 못했습니다.")

        # 리스트에 추가
        news_dates = makeList(news_dates, dates)
        news_titles = makeList(news_titles, titles)
        news_url = makeList(news_url, links)
        news_contents = makeList(news_contents, contents)

    # 네이버 뉴스 필터링
    for title, url, content in zip(news_titles, news_url, news_contents):
        if "네이버뉴스" in title:
            news_url_final.append([title, url, content])

    # 데이터프레임 생성
    news_df = pd.DataFrame(news_url_final, columns=["제목", "링크", "본문"])

    return news_df
