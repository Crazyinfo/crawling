import requests
import re
import random
from selenium import webdriver
import time
import json
import math


# 使用selenium获取cookies
post = {}

driver = webdriver.Chrome()
driver.get('https://mp.weixin.qq.com/')
time.sleep(2)
driver.find_element_by_xpath("./*//input[@name='account']").clear()
driver.find_element_by_xpath("./*//input[@name='account']").send_keys('viasource@163.com')
driver.find_element_by_xpath("./*//input[@name='password']").clear()
time.sleep(5)
driver.find_element_by_xpath("./*//a[@class='btn_login']").click()
# 拿手机扫二维码！
time.sleep(15)
cookie_items = driver.get_cookies()
for cookie_item in cookie_items:
    post[cookie_item['name']] = cookie_item['value'] # 构造cookie字典
cookie_str = json.dumps(post)
with open('cookie.txt', 'w+', encoding='utf-8') as f:
    f.write(cookie_str)
driver.close()



# 开始爬取公众号文章
url = 'https://mp.weixin.qq.com'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}
with open('cookie.txt', 'r', encoding='utf-8') as f:
    cookie = f.read()
cookies = json.loads(cookie)
response = requests.get(url=url, cookies=cookies)
print(response.url)
token = re.findall(r'token=(\d+)', str(response.url))[0]
#print(token)
search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
search_dict = {
    'action': 'search_biz',
    'token': token,
    'lang': 'zh_CN',
    'f': 'json',
    'ajax': '1',
    'random': '0.3720570352633761',#random.random(),
    'query': 'hustxyzh',
    'begin': '0',
    'count': '5',
    }
search_response = requests.get(search_url, cookies=cookies, headers=header, params=search_dict)
#print(search_response.json())
lists = search_response.json().get('list')[0]
fakeid = lists.get('fakeid')
#print(lists)

appmsg_dict = {
    'token': token,
    'lang': 'zh_CN',
    'f': 'json',
    'ajax': '1',
    'random': '0.9868543781213128',
    'action': 'list_ex',
    'begin': '0',
    'count': '5',
    'query': '',
    'fakeid': fakeid,
    'type': '9'
}
appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=appmsg_dict)
#print(appmsg_response.json())
max_num = appmsg_response.json().get('app_msg_cnt')

begin = 0
while begin <= max_num:
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '{}'.format(str(begin)),
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }
    print('翻页###################', begin)
    query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    fakeid_list = query_fakeid_response.json().get('app_msg_list')
    for item in fakeid_list:
        print(item.get('title') + ':' + item.get('link'))
    #begin = int(begin)
    begin += 5
    time.sleep(2)