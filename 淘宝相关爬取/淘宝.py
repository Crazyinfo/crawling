from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re



def get_page():
	url = 'https://s.taobao.com/search?q=%E7%BE%8E%E9%A3%9F&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180927&ie=utf8'
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
	}
	html = requests.get(url, headers=headers)
	return html.text


def parse_page():
	doc = get_page()
	soup = BeautifulSoup(doc, 'lxml')
	items = re.compile('{"text":"(.*?)",', re.S).findall(doc)#soup.find_all('div', id='mainsrp-itemlist')#soup.select('#mainsrp-itemlist .items .item')#.items() #items()方法调用所有选择的内容
	print(items)
	#pattern = re.compile('{"text":"(.*?)",.*?"pic_url":"(.*?)",.*?"view_price":"(.*?)",.*?"item_loc":"(.*?)","view_sales":"(.*?)",.*?"nick":"(.*?)",', re.S)
	#result = re.findall(pattern, doc)
	#print(result)
	#for item in items:
	#	product = {
	#		'image':item.select('.pic .img').attrs('src'),
	#		'price':item.select('.price').text(),
	#		'deal':item.select('.deal-cnt').text()[:-3],
	#		'title':item.select('.title').text(),
	#		'shop':item.select('.shop').text(),
	#		'location':item.select('.location').text()
	#	}
	#	print(product)
	print(soup)

def main():
	parse_page()


if __name__ == '__main__':
	main()
