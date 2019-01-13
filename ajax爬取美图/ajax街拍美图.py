import requests
import re
import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def get_page_index(offset, keyword):
	# data从headers里末尾复制有
	data = {
		'offset': offset,
		'format': 'json',
		'keyword': keyword,
		'autoload': 'true',
		'count': '20',
		'cur_tab': 3,
		'from': 'gallery'
	}
	url = 'https://www.toutiao.com/search_content/?'+ urlencode(data)#urlencode将字典形式的数据合成url上的参数
	try:
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
		}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		print('请求索引页出错')
		return None


def parse_page_index(html):
	data = json.loads(html)
	#print(data,'\n\n\n')
	if data and 'data' in data.keys():
		#print(data.keys()) # 将json转化为python的字典数据类型，键值里面的data里的数据是我们需要的
		for item in data.get('data'):
			yield [
				item.get('article_url'),
				item.get('source'),
				item.get('title'),
				item.get('datetime')
				]

def get_page_detail(url):
	try:
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
		}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		print('请求详情页出错', url)
		return None


def parse_page_detail(content):
	soup = BeautifulSoup(content, 'lxml')
	title = soup.select('title')[0].get_text()
	print(title)
	image_pattern = re.compile('gallery: JSON.parse((.*?)),', re.S) #解析详情页面无法成功，待修改
#	image_pattern = re.compile('BASE_DATA.galleryInfo = (.*?)</script><script>var', re.S)
	result = re.findall(image_pattern, content)
	print(result)



def main():
	html = get_page_index(0, '街拍')
	for url in parse_page_index(html):
		content = get_page_detail(url[0])
		parse_page_detail(content)
		print(url[0],'\n\n')
#		print(content)

if __name__ == '__main__':
	main()