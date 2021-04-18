import re
import time
from selenium import webdriver
import datetime

def write_log(text):
	with open('log.txt', 'a') as log:
		log.write(text)

def update_stock_file(count, buy_price, now_buy_price, now_sell_price, money):
	write_file('stock.txt', 'count', count)
	write_file('stock.txt', 'buy_price', buy_price)
	write_file('stock.txt', 'last_buy_price', now_buy_price)
	write_file('stock.txt', 'last_sell_price', now_sell_price)
	write_file('stock.txt', 'money', money)

def convert_str_to_int(str):
	return int(re.sub(',','', str))

def write_file(file_name, field, value):
    with open(file_name, 'r') as file:
        data = file.read()
    
    with open(file_name, 'w') as file:
        data = re.sub('%s.*=\s*.+' %field, '{0} = {1}'.format(field,value), data)
        file.write(data)

def read_file(file_name, field):
	file = open(file_name, "r")
	result = re.findall("%s.*=\s*(.+)"%field, file.read())[0]
	file.close()
	return result

def enter_count_input(count):
	input_count = driver.find_element_by_id("send_order_txtCount")
	input_count.send_keys(count)

def enter_price_input(price):
	input_price = driver.find_element_by_id("send_order_txtPrice")
	input_price.send_keys(price)

def confirmtion():
	sell_btn =  driver.find_element_by_id("send_order_btnSendOrder")
	sell_btn.click()

	confirmـbtn = driver.find_element_by_id("sendorder_ModalConfirm_btnSendOrder")
	confirmـbtn.click()

def sell(count, price):
	sell_submit = driver.find_element_by_xpath("//div[2]/send-order/div/div[1]/div[2]/div")
	sell_submit.click()

	enter_count_input(count)
	enter_price_input(price)
	
	confirmtion()
	
def buy(count, price):
	buy_submit = driver.find_element_by_xpath("//div[2]/send-order/div/div[1]/div[1]/div")
	buy_submit.click()
	
	enter_count_input(count)
	enter_price_input(price)
	confirmtion()

driver = webdriver.Firefox()
driver.get(read_file("info.txt", "url"))

# login
username = driver.find_element_by_id("username")
username.send_keys(read_file("info.txt","username"))

password = driver.find_element_by_id("password")
password.send_keys(read_file("info.txt","password"))

captcha = driver.find_element_by_id("captcha")
captcha.send_keys(input("captcha:"))

login_butten = driver.find_element_by_class_name("btn-enter")
login_butten.click()

#abort popup box 
time.sleep(5)
if(len(driver.find_elements_by_class_name("popup-box")) != 0):
	abort = driver.find_elements_by_class_name("close")[1]
	abort.click()

#search
time.sleep(5)
stock = read_file("info.txt", "stock")
search = driver.find_elements_by_id("txt_search")[1]
search.send_keys(stock)
time.sleep(2)
driver.find_elements_by_xpath("//div[contains(@isin, 'IR')]")[0].click()

#price
time.sleep(5)
hight_price = convert_str_to_int(driver.find_element_by_id("dailyslider_Hight").text)
low_price = convert_str_to_int(driver.find_element_by_id("dailyslider_Low").text)

#print("hight price:" + str(hight_price))
#print("low price:" + str(low_price))

#Alogorithm
min = int(read_file('info.txt', 'min'))
wage = float(read_file('info.txt', 'wage'))

for i in range(1, min+1):
	now_sell_price = convert_str_to_int(driver.find_element_by_xpath('//table/tbody/tr[1]/td[3]/span[2]').text)
	now_buy_price = convert_str_to_int(driver.find_element_by_xpath('//table/tbody/tr[1]/td[4]/span[2]').text)

	write_log('Date:{0}		price :   sell {1}, buy {2}\n'.format(datetime.datetime.now(), now_sell_price, now_buy_price))

	count = int(read_file('stock.txt', 'count'))
	last_sell_price = int(read_file('stock.txt', 'last_sell_price'))
	last_buy_price = int(read_file('stock.txt', 'last_buy_price'))
	money = int(read_file('stock.txt', 'money'))
	buy_price = int(read_file('stock.txt', 'buy_price'))

	#SELL
	if count != 0:
		if now_sell_price >= int(buy_price + (buy_price * wage)):
			if now_sell_price < last_sell_price:
				#update file
				new_money = money + int((now_sell_price * count) - (now_sell_price * count * wage))
				update_stock_file(0, 0, now_buy_price, now_sell_price, new_money)			

				print("sell count '{0}' , price '{1}'".format(count, now_sell_price))
				write_log("Date:{0}		sell count {1} , price {2}, money {3}\n".format(datetime.datetime.now(), count, now_sell_price, new_money))
				#sell(count, now_sell_price)
				continue

	#BUY
	if count == 0:
		if now_buy_price > last_buy_price:	
			#update file
			new_count = int(money/now_buy_price)
			new_money = money - int((now_buy_price * new_count) + (now_buy_price * new_count * wage))
			update_stock_file(new_count, now_buy_price , now_buy_price, now_sell_price, new_money)			

			print("buy count '{0}' , price '{1}'".format(new_count, now_buy_price))
			write_log("Date:{0}		buy count {1} , price {2}, money {3}\n".format(datetime.datetime.now(),new_count, now_sell_price, new_money))
			#buy(new_count, now_buy_price)				
			continue
		
	write_file('stock.txt', 'last_sell_price', now_sell_price)
	write_file('stock.txt', 'last_buy_price', now_buy_price)

	time.sleep(30)
