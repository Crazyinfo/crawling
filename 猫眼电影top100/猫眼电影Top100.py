import requests
import re
import json
import time
from requests.exceptions import RequestException
# from multpocessing import Pool

def get_one_page(url):
	try:
		headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
		}
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None



def parse_one_page(html):
	pattern = re.compile(
		'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
	items = re.findall(pattern, html)
	for item in items:
		yield {
		'index': item[0],
		'image': item[1],
		'title': item[2].strip(),
		'actor': item[3].strip()[3:], # 字符串切片
		'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
		'score': item[5].strip() + item[6].strip()
		}



def write_to_file(content):
	with open('result5.txt', 'a', encoding = 'utf-8') as f:
		f.write(json.dumps(content, ensure_ascii = False) + '\n') # json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False


def main(offset):
	url = 'http://maoyan.com/board/4?offset=' + str(offset)
	html = get_one_page(url)
	for x in parse_one_page(html):
		print(x)
		write_to_file(x)


if __name__ == '__main__':
	for i in range(10):
		main(offset = i*10)
		time.sleep(1) # 猫眼多了反爬虫，速度过快则会无响应，故增加了一个延时等待。

#	pool = Pool()
#	pool.map(main, [i*10 for in range(10)]) 多进程，进程池


# 正则提取
 # 筛选排名、电影图片、电影名称、主演、上映时间地点、评分
