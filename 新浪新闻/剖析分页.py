import requests
import json

url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=3'
res = requests.get(url)
# res.encoding = 'utf-8'
# jd = json.loads(res.text)
jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');')) 
# 将json格式转换为python中的字典，而获取的res.text多了一个JavaScript功能函数字符，需去掉才能使用
# print(jd)
for ent in jd['result']['data']:
	print(ent['url'])