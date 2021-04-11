import re
from selenium import webdriver

def read_file(file_name, field):
	file = open(file_name, "r")
	result = re.findall("%s.*=\s*(.+)"%field, file.read())[0]
	file.close()
	return result

url = "https://www.mofidonline.com/Account/Login"
driver = webdriver.Firefox()
driver.get(url)

# login
username = driver.find_element_by_id("username")
username.send_keys(read_file("info.txt","username"))

password = driver.find_element_by_id("password")
password.send_keys(read_file("info.txt","password"))

captcha = driver.find_element_by_id("captcha")
captcha.send_keys(input("captcha:"))

login_butten = driver.find_element_by_class_name("btn-enter")
login_butten.click()
