import re
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

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

time.sleep(5)

#abort pop up box 
if(len(driver.find_elements_by_class_name("popup-box")) != 0):
	abort = driver.find_elements_by_class_name("close")[1]
	abort.click()

time.sleep(5)

#search
search = driver.find_elements_by_id("txt_search")
search[1].send_keys("طلا")
#list_container = driver.find_elements_by_id("auto-list-container")
time.sleep(5)

list_drop_down = driver.find_elements_by_id("list_dropdown")[1]

#list_drop_down.click()
