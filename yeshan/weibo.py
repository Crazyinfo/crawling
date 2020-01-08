from selenium import webdriver
import requests
import time
import json
from bs4 import BeautifulSoup
import re
import pymysql

def get_cookies():
	post = {}

	driver = webdriver.Chrome()
	driver.get('https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=')
	time.sleep(2)
	driver.find_element_by_xpath("./*//input[@id='loginName']").clear()
	driver.find_element_by_xpath("./*//input[@id='loginName']").send_keys('')# 写自己账号
	time.sleep(5)
	driver.find_element_by_xpath("./*//input[@id='loginPassword']").clear()
	driver.find_element_by_xpath("./*//input[@id='loginPassword']").send_keys('')# 写自己密码
	time.sleep(5)
	driver.find_element_by_xpath("./*//a[@class='btn btnRed']").click()
	time.sleep(5)

	#自动化搜索
	#driver.find_element_by_xpath("/html/body/div[28]/form/div/input[1]").clear()
	#driver.find_element_by_xpath("/html/body/div[28]/form/div/input[1]").send_keys('卢浮宫')# 写自己密码
	#time.sleep(2)
	#driver.find_element_by_xpath("/html/body/div[28]/form/div/input[2]").click()


	time.sleep(2)
	cookie_items = driver.get_cookies()
	for cookie_item in cookie_items:
		post[cookie_item['name']] = cookie_item['value'] # 构造cookie字典
	cookie_str = json.dumps(post)
	with open('cookie.txt', 'w+', encoding='utf-8') as f:
		f.write(cookie_str)
	driver.close()


# 开始爬取
def get_result(keyword, page):
	header = {
	    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
	}
	with open('cookie.txt', 'r', encoding='utf-8') as f:
		cookie = f.read()
	cookies = json.loads(cookie)
	for i in range(1, page+1):
		url = 'https://weibo.cn/search/mblog?keyword={keyword}&page={page}'.format(keyword=keyword, page=page)
		response = requests.get(url=url, cookies=cookies, headers=header)

		content = response.text
		soup = BeautifulSoup(content,"lxml")
		items = soup.find_all(name="div", class_="c", id=re.compile(r'.*?'))


		for item in items:
			yield{
			'id': re.findall(re.compile('.*?id="(.*?)"'), str(item))[0],
			'user': item.a.get_text(),
			'behavior': is_relay(item),
			'content': get_content(item),
			'pic': re.findall(re.compile('src="(.*?)"'), str(item.find_all(name='img'))),
			'like': item.find_all(name='a', href=re.compile("attitude"))[0].get_text(),
			'relay': item.find_all(name='a', href=re.compile("repost"))[0].get_text(),
			'comment': item.find(name='a', class_='cc').get_text(),
			'time': item.find(name='span', class_='ct').get_text()
			}


# 判断是否属于转发内容
def is_relay(item):
	isor = item.find(name='span', class_='cmt')
	if isor != None:
		user = re.findall(re.compile('转发了 <a href=".*?">(.*?)</a>'), str(isor))[0]
		return '转发了'+ user + '的微博'
	else:
		return '原创'

# 以是否转发区分获取详情信息
def get_content(item):
	if is_relay(item) == '原创':
		content = item.find_all(name='span', class_='ctt')[0].get_text().lstrip(':')
		return content
		content_url = item.find(name='a', class_='cc')['href']
	else:
		reason = re.findall(re.compile('.*?转发理由:</span>(.*?)<',re.S), str(item))[0]
		return reason


def write_to_file(one):
	with open('weibo.txt', 'a', encoding = 'utf-8') as f:
		f.write(json.dumps(one, ensure_ascii = False) + '\n')




def write_to_database(one):
	conn = pymysql.connect(host='localhost', user='EV', password='161513', db='sys', port=3306, charset='utf8')# 声明一个mysql连接对象
	cursor = conn.cursor() #获得mysql的操作游标 利用游标来执行sql语句
	cursor.execute("SELECT VERSION()") #execute() 执行sql语句 查询当前mysql版本
	data = cursor.fetchone() #获得第一条数据
	print("连接成功！数据库版本号:",data)

	sql = "SELECT * FROM sys_config"

	try:
		cursor.execute(sql) # 执行SQL语句
		results = cursor.fetchall() # 获取所有记录列表
		for row in results:
			value = row[1] #获取第二个字段
			print("第二个值=", value)
	except:
		print("错误发生：获取数据失败") # 打印结果


def main():
	#get_cookies()
	for one in get_result('复联', 1):
		pass
		#write_to_file(one)
		#write_to_database(one)
		print(one)


if __name__ == '__main__':
	main()