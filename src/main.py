import re
import time
from selenium import webdriver

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
time.sleep(2)
if(len(driver.find_elements_by_class_name("popup-box")) != 0):
	abort = driver.find_elements_by_class_name("close")[1]
	abort.click()

#search
time.sleep(2)
stock = read_file("info.txt", "stock")
search = driver.find_elements_by_id("txt_search")[1]
search.send_keys(stock)
time.sleep(2)
driver.find_elements_by_xpath("//div[contains(@isin, 'IR')]")[0].click()

#price
time.sleep(2)
hight_price = int(re.sub(',','', driver.find_element_by_id("dailyslider_Hight").text))
low_price = int(re.sub(',','', driver.find_element_by_id("dailyslider_Low").text))
print("hight price:" + str(hight_price))
print("low price:" + str(low_price))
