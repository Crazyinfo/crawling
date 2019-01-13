import re
import requests
import json
from requests.exceptions import RequestException

def get_page(url):
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


def parse_page(url_text):
	music = []
	pattern = re.compile(
		'<li><a href="(.*?)">(.*?)</a>.*?<br/>.*?</li>', re.S)#下载链接、歌曲名字、文件大小
	items = re.findall(pattern, url_text)
	for item in items:
		yield {
		'name': item[1],
		'link': item[0],
		}


def write_to_file(content):
	with open('music.txt', 'a', encoding = 'utf-8') as f:
		f.write(json.dumps(content, ensure_ascii = False) + '\n') # json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False


def download_link(list):
	for music in list:

		file_name = music.split('/')[-1]
		print("Downloading file:%s" % file_name)
		r = requests.get(music, stream=True)
		with open(file_name, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024 * 1024):
				if chunk:
					f.write(chunk)

		print("%s downloaded!\n" % file_name)




def main():
	url = 'http://midi.midicn.com/2000/06/06/%E6%AC%A7%E7%BE%8E%E6%B5%81%E8%A1%8C%E9%9F%B3%E4%B9%90MIDI'
	html = get_page(url)
#	print(html)
	music_list = []
	music_list.append('http://file.midicn.com/midi/euro_usa_pop/feeling.mid')
	for item in parse_page(html):
		if item['link'].strip('/'):
			print(item['link'].strip('/'))
			music_list.append(item['link'].strip('/'))
#	print(music_list)
			write_to_file(item)
	download_link(music_list)


if __name__ == '__main__':
	main()