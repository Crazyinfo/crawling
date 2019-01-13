import requests
from bs4 import BeautifulSoup
from datetime import datetime
'''
res = requests.get('http://news.sina.com.cn/c/nd/2016-08-20/doc-ifxvctcc8121090.shtml')
res.encoding = 'utf-8' # 申明编码方式，否则会乱码
print(res.text) # 可以显示html代码
soup = BeautifulSoup(res.text, 'html.parser')
print(soup.select('#artibodyTitle')[0].get_text())
'''

res = requests.get('http://news.sina.com.cn/c/gat/2018-08-10/doc-ihhnunsq4646089.shtml')
res.encoding = 'utf-8' # 申明编码方式，否则会乱码
soup = BeautifulSoup(res.text, 'html.parser')


title = soup.select('.main-title')[0].get_text()

# 以下方式得到的是str类型的时间
dt = soup.select('.date-source span')[0].contents[0].strip().replace(' ', '') # 去除首位的空格
# parent方法用于向上遍历树节点，contents方法用于向下遍历树节点，即向下访问某节点的子节点。 
# tag的.contents 属性可以将tag的子节点以列表的方式输出。  


source = soup.select('.date-source a')[0].get_text()

# 字符串时间 - strptime  
time = datetime.strptime(dt, '%Y年%m月%d日%H:%M') 
# print(time.strftime('%Y-%m')) 字符串时间中特定的年或月等
print(time, source)

article = []
for p in soup.select('#article p')[:-1]: # 去掉最后一个列表里的责任编辑
	article.append(p.get_text().strip())

h = '\n'.join(article)

# print('\n'.join([p.text.strip() for p in soup.select('#article p')[:-1]])) 另外一种写法

print(h)


# 取得编辑名称
editor = soup.select('.show_author')[0].get_text().strip() # strip('责任编辑：') 表示去掉'责任编辑：'
print(editor)



# 抓取新闻评论数
# print(soup.select('#commentCount1'))该方法显示不出评论数,可猜测使用了JavaScript
comments = requests.get('http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-fxvctcc8121090&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20')
import json
jd = json.loads(comments.text.strip('var data='))
#　　(1)json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）
#　　(2)json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）
# jd是一个字典，从里面获取想要的数据需要层层获取，如下获取评论数
print(jd['result']['count']['total'])



# 获取新闻编号
newsurl = 'http://news.sina.com.cn/c/nd/2016-08-20/doc-ifxvctcc8121090.shtml'
# split以/切割成一个list
# print(newsurl.split('/'))
newsid = newsurl.split('/')[-1].rstrip('.shtml').lstrip('doc-i') # 通过[-1]取得最后一层资料

print(newsid)

# 获取新闻编号（使用正则表达式）
import re
m = re.search('doc-i(.*).shtml', newsurl) #()括号里面是需要match的部分
print(m)
print(m.group(0)) # 打印所有比对到的部分
print(m.group(1)) # 打印第一个小括号比对的部分