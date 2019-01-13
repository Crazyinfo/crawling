import requests
from requests.exceptions import RequestException
import json
import re

def get_one_page(url):
	try:
		headers = {'Use-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None

def parse_one_page(html):
	pattern = re.compile('"showInfo":"(.*?)","boxRate":"(.*?)","avgShowView":"(.*?)","seatRate":"(.*?)","movieId":(.*?),"avgSeatView":"(.*?)",.*?"release.*?"boxInfo":"(.*?)","viewInfoV2":"(.*?)","splitAvgViewBox":"(.*?)","movieName":"(.*?)","splitSumBoxInfo":"(.*?)",".*?"releaseInfo":"(.*?)","sumBoxInfo":"(.*?)","splitBoxRate":"(.*?)","splitBoxInfo":"(.*?)","viewInfo":".*?showRate":"(.*?)","avgViewBox":"(.*?)"',re.S)
	items = re.findall(pattern, html)
	for item in items:
		yield{
		'movieName':item[9],#电影名
		'sumBoxInfo':item[12],#票房
		'showInfo':item[0],#排片场次
		'boxRate':item[1],#票房占比
		'avgShowView':item[2],#场均人数
		'seatRate':item[3],
		'movieId':item[4],
		'avgSeatView':item[5],#上座率
		'boxInfo':item[6],
		'viewInfoV2':item[7],
		'splitAvgViewBox':item[8],
		'splitSumBoxInfo':item[10],
		'releaseInfo':item[11],#上映天数
		'splitBoxRate':item[13],
		'splitBoxInfo':item[14],
		'showRate':item[15],
		'avgViewBox':item[16]
		}


def present_time(html):
	require = re.compile('"data":{"updateInfo":"(.*?)","',re.S)
	time = re.findall(require, html)
	return time


def write_to_file(content):
	with open('maoyanpiaofang.txt', 'a', encoding = 'utf-8') as f:
		f.write(json.dumps(content, ensure_ascii = False) + '\n')


def main():
	url = 'https://box.maoyan.com/promovie/api/box/second.json'
	html = get_one_page(url)
	time = present_time(html)
	print(time, '\n')
#	write_to_file(time,'\n')
	for x in parse_one_page(html):
		print(x)
		write_to_file(x)
#	print(get_one_page(url))


if __name__ == '__main__':
	main()





'''
	for item in items:
		yield{
		'showInfo':item[0],#排片场次
		'boxRate':item[1],#票房占比
		'avgShowView':item[2],#场均人数
		'seatRate':item[3],
		'movieId':item[4],
		'avgSeatView':item[5],#上座率
		'boxInfo':item[6],
		'viewInfoV2':item[7],
		'splitAvgViewBox':item[8],
		'movieName':item[9],#电影名
		'splitSumBoxInfo':item[10],
		'releaseInfo':item[11],#上映天数
		'sumBoxInfo':item[12],#票房
		'splitBoxRate':item[13],
		'splitBoxInfo':item[14],
		'showRate':item[15],
		'avgViewBox':item[16]
		}
'''