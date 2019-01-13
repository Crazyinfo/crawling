import requests
from bs4 import BeautifulSoup
import re
import json

html = 'http://news.sina.com.cn/china/'
headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}

reqhtml = requests.get(html,headers=headers).content # 若不设置编码方式，用.text会乱码，而用.content不会

souphtml = BeautifulSoup(reqhtml, 'html.parser') # 指定解析器,否则会有警告
#print(souphtml)





#h3 = souphtml.find_all('div')

zhuyenews = souphtml.find_all('div', class_ = 'right-content') # 首页显示的主要新闻

h1 = souphtml.find_all('div',  style='display:none;')

pattern = re.compile('<a href="(.*?)" target="_blank" title="(.*?)">')

hot_click = souphtml.find_all(pattern)

items = re.findall(pattern, requests.get(html,headers=headers).text)
print(items)
print(hot_click)

print(zhuyenews)

#print('\n\n\n\n\n', h1)

'''
for news in souphtml.select('.news-item'):
	if len(news.select('h2')) > 0:
		h2 = news.select('h2')[0].get_text() # 或者用h2 = news.select('h2')[0].text
		time = news.select('.time')[0].get_text()
		a = news.select('a')[0]['href']
		print(time, h2, a)
'''