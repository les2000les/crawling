#top종목 추출
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import pandas as pd

URL = 'https://finance.naver.com/'
items = requests.get(URL)
html = BeautifulSoup(items.text,'lxml')
pattern = r'\d+' #정규표현식(숫자만 포함된 텍스트추출)

#거래상위
stockslist =  html.select('#_topItems1>tr') 
name_list = []
price_list = []
updown_list = []
percent_list = []
unit_list = []
unit = '거래상위'
for stocks in stockslist:
    unit_list.append(unit)
    name = stocks.select_one('#_topItems1 > tr> th > a').text
    name_list.append(name)
    price = stocks.select_one('#_topItems1 > tr> td')
    price = re.findall(pattern, str(price))
    price = ''.join(price)
    price_list.append(price)
    updown = stocks.select_one('#_topItems1 > tr > td:nth-child(3)').text
    updown_list.append(updown)
    percent = stocks.select_one('#_topItems1 > tr> td:nth-child(4)')
    percent = re.findall(pattern, str(percent))
    percent = ''.join(percent)
    percent_list.append(percent)

stocks_df1 = pd.DataFrame({'checkdate':datetime.now(),'unit': unit_list,'name':name_list,'price':price_list,'updown': updown_list, 'percent': percent_list})
stocks_df1



#상승
stockslist =  html.select('#_topItems2>tr') 
name_list = []
price_list = []
updown_list = []
percent_list = []
unit_list = []
unit = '상승'
for stocks in stockslist:
    unit_list.append(unit)
    name = stocks.select_one('#_topItems2 > tr> th > a').text
    name_list.append(name)
    price = stocks.select_one('#_topItems2 > tr> td')
    price = re.findall(pattern, str(price))
    price = ''.join(price)
    price_list.append(price)
    updown = stocks.select_one('#_topItems2 > tr > td:nth-child(3)').text
    updown_list.append(updown)
    percent = stocks.select_one('#_topItems2 > tr> td:nth-child(4)')
    percent = re.findall(pattern, str(percent))
    percent = ''.join(percent)
    percent_list.append(percent)

stocks_df2 = pd.DataFrame({'checkdate':datetime.now(),'unit': unit_list, 'name':name_list,'price':price_list,'updown': updown_list, 'percent': percent_list})
stocks_df2

#하락
stockslist =  html.select('#_topItems3>tr') 
name_list = []
price_list = []
updown_list = []
percent_list = []
unit_list = []
unit = '하락'
for stocks in stockslist:
    unit_list.append(unit)
    name = stocks.select_one('#_topItems3 > tr> th > a').text
    name_list.append(name)
    price = stocks.select_one('#_topItems3 > tr> td')
    price = re.findall(pattern, str(price))
    price = ''.join(price)
    price_list.append(price)
    updown = stocks.select_one('#_topItems3 > tr > td:nth-child(3)').text
    updown_list.append(updown)
    percent = stocks.select_one('#_topItems3 > tr> td:nth-child(4)')
    percent = re.findall(pattern, str(percent))
    percent = ''.join(percent)
    percent_list.append(percent)

stocks_df3 = pd.DataFrame({'checkdate':datetime.now(),'unit': unit_list, 'name':name_list,'price':price_list,'updown': updown_list, 'percent': percent_list})
stocks_df3

#시가총액 상위
stockslist =  html.select('#_topItems4>tr') 
name_list = []
price_list = []
updown_list = []
percent_list = []
unit_list = []
unit = '시각총액상위'
for stocks in stockslist:
    unit_list.append(unit)
    name = stocks.select_one('#_topItems4 > tr> th > a').text
    name_list.append(name)
    price = stocks.select_one('#_topItems4 > tr> td')
    price = re.findall(pattern, str(price))
    price = ''.join(price)
    price_list.append(price)
    updown = stocks.select_one('#_topItems4 > tr > td:nth-child(3)').text
    updown_list.append(updown)
    percent = stocks.select_one('#_topItems4 > tr> td:nth-child(4)')
    percent = re.findall(pattern, str(percent))
    percent = ''.join(percent)
    percent_list.append(percent)

stocks_df4 = pd.DataFrame({'checkdate':datetime.now(),'unit': unit_list, 'name':name_list,'price':price_list,'updown': updown_list, 'percent': percent_list})
stocks_df4

stocks_df = pd.concat([stocks_df1, stocks_df2, stocks_df3, stocks_df4])
stocks_df
