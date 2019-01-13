import requests
from bs4 import BeautifulSoup

douban_book = 'https://read.douban.com/columns/category/all'


def download_page(url):
	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}
	return requests.get(url, headers = headers).text


def souppage(html):
	soup = BeautifulSoup(html,'html.parser')
	books_list_soup = soup.find('ul', class_ = 'list-lined ebook-list column-list')

	book_lists = []

	for books_li in books_list_soup.find_all('li'):
		title = books_li.find('h4', class_ = 'title').find('a').get_text()
		author = books_li.find('div', class_ = 'author').find('a').get_text()
		book_lists.append(title + ' - ' + author)
		
	#设置抓数据停顿时间为1秒，防止过于频繁访问该网站，被封
	time.sleep(1)

	next_page = soup.find('li', class_ = 'next').find('a')

	if next_page:
		return book_lists, 'https://read.douban.com' + next_page['href']

	return book_lists, None

def main():
	url = douban_book
	with open('books', 'w', encoding='utf-8') as fp:

		while url:
			html = download_page(url)
			books, url = souppage(html)
			fp.write('{0}\n'.format('\n'.join(books)))

if __name__ == '__main__':
	main()

