import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas

# {}表示待填入的数据，该处为新闻的id
commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
newsurl = 'http://news.sina.com.cn/c/gat/2018-08-10/doc-ihhnunsq4646089.shtml'
url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=1'
urls = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}'

# 获取总评论数
def getCommentCounts(newsurl):
	m = re.search('doc-i(.*).shtml', newsurl)
	newsid = m.group(1)
	comments = requests.get(commentURL.format(newsid))
	jd = json.loads(comments.text.strip('var data='))
	return jd['result']['count']['total']

#print(getCommentCounts(newsurl))

# 抓取新闻内文信息
def getNewsDetail(newsurl):
	result = {}
	res = requests.get(newsurl)
	res.encoding = 'utf-8'
	soup = BeautifulSoup(res.text, 'html.parser')
	result['title'] = soup.select('.main-title')[0].get_text()
	#result['source'] = soup.select('.date-source a')[0].get_text()
	timesource = soup.select('.date-source span')[0].contents[0].strip().replace(' ', '')
	result['time'] = datetime.strptime(timesource, '%Y年%m月%d日%H:%M') 
	result['article'] = '\n'.join([p.get_text().strip() for p in soup.select('#article p')[:-1]]) # [:-1]切片，去掉编辑
	result['editor'] = soup.select('.show_author')[0].get_text().strip('责任编辑：')
	result['comments'] = getCommentCounts(newsurl)
	return result

#print(getNewsDetail(newsurl))


# 建立剖析清单链接,将每一则链接中的新闻内文集合放在列表中
def parseListLinks(url):
	newsdetail = []
	res = requests.get(url)
	res.encoding = 'utf-8'
	jd = json.loads(res.text) 
	for ent in jd['result']['data']:
		newsdetail.append(getNewsDetail(ent['url']))
	return newsdetail


# print(len(parseListLinks(url))) # 22
'''
print(parseListLinks(urls.format(1)))
print(parseListLinks(urls.format(2)))
print(parseListLinks(urls.format(3)))
'''


# 抓取多页的新闻内容
def morePageNews():
	news_total = []
	for i in range(1, 3):
		newsurl = urls.format(i)
		newsary = parseListLinks(newsurl)
		news_total.extend(newsary) # 在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
	return news_total


# print(len(morePageNews()))# 44

def PandasData():
	df = pandas.DataFrame(morePageNews())
	return df.head(20) # head()只显示数据列表的前五个,或者在括号中填入需要显示的数目


print(PandasData())
PandasData().to_excel('new.xlsx')
