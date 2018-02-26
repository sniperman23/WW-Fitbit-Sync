from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup
import requests
import fitbit
import datetime


option = webdriver.ChromeOptions()
option.add_argument('--headless')

browser = webdriver.Chrome( )

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

numFoodItems =  len(foodList)

def grabMacros( foodItem ):
	foodItem.click()
	macroList = list()
	##grabbing foodName and unitId and amount/serving size and putting at front of list
	
	
	
	select = Select(WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, 'dropdown-'+ str( dropDownCount )  ))))
	unit = select.first_selected_option.get_attribute("value")
	foodName = browser.find_element_by_xpath( '//*[@id="main-content"]/div/div[1]/div[2]/h1' )
	
	
	macroList.append( foodName.text )
	macroList.append( unit )
	
	##finding the actual macros now
	webElements = browser.find_elements_by_xpath( "//div[@class='amount ng-binding']" )
	
	
	for n in webElements:
		macroList.append( n.text )
	
	
	
	browser.execute_script("window.history.go(-1)")
	return macroList
	
dropDownCount = 0
allFoodsWithMacros = list()	
for x in range(0, numFoodItems):
	foodList = browser.find_elements_by_class_name('daily-log-item-content-extra')
	dropDownCount = dropDownCount + 2
	allFoodsWithMacros.append( grabMacros( foodList[x] ) )



##-------------------IMPORTING INTO FITBIT PART ---------------------- ##

authd_client = fitbit.Fitbit('22CN7D', 'ec4bf572e89c8234be12f0913df103a8',
							 access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzQko1RFQiLCJhdWQiOiIyMkNON0QiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNTE5NjkwNDE1LCJpYXQiOjE1MTk2NjE2MTV9.CuemtzY6q6M2zBmvZNitJKUH1V5bifLWsTqghWr7Xls',
							 refresh_token= '688357beb834df3830f3901551a951390b5942721653d6d79d1ca31e8f360161')
count = 0;			 
for x in allFoodsWithMacros:
	count = count + 1
	foodDictionary = {
		"foodId" : count,
		"foodName" : x[0],
		"mealTypeId" : 1,
		"unitId" : x[1],
		"amount" : 1,
		"date" : datetime.datetime.now().strftime( "%Y-%m-%d" ),
		"calories" : x[2],
		"totalFat(g)" : x[3],
		"saturatedFat(g)" : x[4],
		"totalCarbohydrate(g)" : x[5],
		"dietaryFiber(g)" : x[6],
		"sugars(g)" : x[7],
		"protein(g)" : x[8]
	}
	
	print ( foodDictionary )
	authd_client._COLLECTION_RESOURCE( resource = 'foods/log', data = foodDictionary )	

	



