# encoding=utf-8

"""
爬取豆瓣电影TOP250 - 完整示例代码
"""

import codecs

import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250/'


def download_page(url):
	# 获取爬虫网页
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content


def parse_html(html):
	# 解析网页
    soup = BeautifulSoup(html,'html.parser')
    # 寻找ol标签内容，包含了所有电影列表
    movie_list_soup = soup.find('ol', class_ = 'grid_view')

    movie_name_list = []

    # 寻找li标签内容，包含单个电影内容
    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', class_ = 'hd')
        movie_name = detail.find('span', class_ = 'title').get_text()

        movie_name_list.append(movie_name)

    # 翻页
    next_page = soup.find('span', class_ = 'next').find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']

    return movie_name_list, None # 程序运行到所遇到的第一个return即返回（退出def块），不会再运行第二个return。
    # 或用else


def main():
    url = DOWNLOAD_URL
    
    # 使用codecs这个包是为了更方便处理中文编码
    with codecs.open('moviess', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            # u表示该段字符用unicode编码
            fp.write('{0}\n'.format('\n'.join(movies)))


if __name__ == '__main__':
    main()