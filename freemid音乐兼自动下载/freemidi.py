import re
import requests
import json
from requests.exceptions import RequestException



def get_page(url):#获取不同的首页
	try:
		headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
		}
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None


def get_pages(html):#进入不同首页中的下载页面获取每个下载链接
	list_page = []
	pattern = re.compile(
		'<div class=song-list-container>.*?href="(.*?)".*?<a href=genre-></a></div>', re.S)#下载链接、歌曲名字、文件大小
	items = re.findall(pattern, html)
	for item in items:
		list_page.append(item)
	return list_page



def download_midi(list_link):#下载
	for raw_link in list_link:
		link = 'https://freemidi.org/getter-' + raw_link.split('-')[1]
		file_name = raw_link.split('-')[-1] + '.mid'
		print("Downloading file:%s" % file_name)
		r = requests.get(link, stream=True)
		with open(file_name, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024 * 1024):
				if chunk:
					f.write(chunk)

		print("%s downloaded!\n" % file_name)




def main():
	urls = 'https://freemidi.org/songtitle-0-{}'
	for i in range(0,9):
		print(i)
		url = urls.format(i)
		html = get_page(url)
		list_link = get_pages(html)
		#print(h)
		download_midi(list_link)

		
if __name__ == '__main__':
	main()