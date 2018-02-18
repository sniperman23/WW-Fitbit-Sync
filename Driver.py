from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup

option = webdriver.ChromeOptions()

browser = webdriver.Chrome()

browser.get("https://auth.weightwatchers.com/login/")

timeout = 10

try:
	WebDriverWait( browser, timeout).until(EC.element_to_be_clickable((By.ID, 'loginButton')))
except TimeoutException:
	print("Timed out waiting for page to load")
	browser.quit();
	
username = browser.find_element_by_id("username")
password = browser.find_element_by_id("password")

username.send_keys("sniperman23")
password.send_keys("halo3rulz")

browser.find_element_by_id("loginButton").click()

time.sleep(4)
	
html = browser.page_source

soup = BeautifulSoup(html, "html.parser")

foodList = browser.find_elements_by_class_name('daily-log-item-content-extra')

for item in foodList:
	grabMacros( foodItem = item )

def grabMacros( foodItem )
	foodItem.click()
	time.sleep(10)
	print("nigga we made it")
	
print( foodList )
