import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10) #用法哦比较多所以赋值

def search():
	try:
		browser.get('https://www.taobao.com')
		input = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))#选中主页的输入框
			)
		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))#选中首页的按钮
			)
		input.send_keys('美食') #输入搜索关键字
		submit.click() #点击按钮
		total = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))) #获取页数
#		get_product()
		return total.text
	except TimeoutException:
		return search()



def next_page(page_number):
	try:
		input = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))#选中页码的输入框
			)
		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))#选中确定的按钮
			)
		input.clear()#清除当中的内容
		input.send_keys(page_number)
		submit.click()
		# 判断是否跳转成功
		wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_number)))
		get_product()
	except TimeoutException:
		next_page(page_number)

def  get_product():  # 该函数无法正确爬取，待修改
	wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "mainsrp-itemlist .items .item")))
	html = browser.page_source #获取网页源代码
	doc = BeautifulSoup(html, 'lxml')
	items = doc.select("mainsrp-itemlist .items .item").items() #items()方法调用所有选择的内容
	for item in items:
		product = {
			'image':item.select('.pic .img').attrs('src'),
			'price':item.select('.price').text(),
			'deal':item.select('.deal-cnt').text()[:-3],
			'title':item.select('.title').text(),
			'shop':item.select('.shop').text(),
			'location':item.select('.location').text()
		}
#		print(product)
#	doc = pq(html)
#	items = doc("mainsrp-itemlist .items .item").items() #items()方法调用所有选择的内容
#	for item in items:
#		product = {
#			'image':item.find('.pic .img').attrs('src'),
#			'price':item.find('.price').text(),
#			'deal':item.find('.deal-cnt').text()[:-3],
#			'title':item.find('.title').text(),
#			'shop':item.find('.shop').text(),
#			'location':item.find('.location').text()
#		}
#		print(product)

def main():
	total = search()
	total = int(re.compile('(\d+)').search(total).group(1))
	for i in range(2, total + 1):
		next_page(i)
	browser.close()

if __name__ == '__main__':
	main()