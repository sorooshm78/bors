import re
import time
from selenium import webdriver
import datetime

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

print("hight price:" + str(hight_price))
print("low price:" + str(low_price))

#Alogorithm
min = int(read_file('info.txt', 'min'))
wage = float(read_file('info.txt', 'wage'))
log = open('log.txt', 'a')

for i in range(1, min+1):
	now_sell_price = convert_str_to_int(driver.find_element_by_xpath('//table/tbody/tr[1]/td[3]/span[2]').text)
	now_buy_price = convert_str_to_int(driver.find_element_by_xpath('//table/tbody/tr[1]/td[4]/span[2]').text)

	log.write('Date:{0}		sell price {1}, buy price {2}\n'.format(datetime.datetime.now(), now_sell_price, now_buy_price))

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
				n_count = 0
				n_buy_price = 0
				n_last_buy_price = now_buy_price
				n_last_sell_price = now_sell_price
				n_money = money + int((now_sell_price * count) - (now_sell_price * count * wage))
				write_file('stock.txt', n_count, n_buy_price, n_last_buy_price, n_last_sell_price, n_money)

				print("sell count '{0}' , price '{1}'".format(count, now_sell_price))
				log.write("Date:{0}		sell count {1} , price {2}, money {3}\n".format(datetime.datetime.now(), count, now_sell_price, n_money))
				continue
				#sell()

	#BUY
	if count == 0:
		if now_buy_price > last_buy_price:
			
			#update file
			n_count = int(money/now_buy_price)
			n_buy_price = now_buy_price
			n_last_buy_price = now_buy_price
			n_last_sell_price = now_sell_price
			n_money = money - int((now_buy_price * n_count) + (now_buy_price * n_count * wage))
			write_file('stock.txt', n_count, n_buy_price, n_last_buy_price, n_last_sell_price, n_money)

			print("buy count '{0}' , price '{1}'".format(n_count, now_buy_price))
			log.write("Date:{0}		buy count {1} , price {2}, money {3}\n".format(datetime.datetime.now(),n_count, now_sell_price, n_money))
			continue
			#buy()				

	n_count = count
	n_buy_price = read_file('stock.txt', 'buy_price')
	n_last_buy_price = now_buy_price
	n_last_sell_price = now_sell_price
	n_money = money
	write_file('stock.txt', n_count, n_buy_price, n_last_buy_price, n_last_sell_price, n_money)

	time.sleep(60)
