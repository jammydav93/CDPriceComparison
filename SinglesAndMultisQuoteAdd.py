import time
import re
import csv
import credentials
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

print(time.ctime(time.time()))

driver = webdriver.Chrome('C:\Python36\selenium\webdriver\chromedriver.exe')

def SKU_File_To_List(SKU_List):
    with open("SKU_File.csv") as SKU_File:
        for SKU in SKU_File:
            SKU = SKU.strip()
            if (SKU not in SKU_List):
                SKU_List.append(SKU)
    return SKU_List 

def Ziffit_Get_Price(SKU):
    URL = 'https://www.ziffit.com/'
    driver.get(URL)
    try:
        driver.find_element_by_id("ean").clear()
        driver.find_element_by_id("ean").send_keys(SKU)
        driver.find_element_by_id("get-value-button").click()
        
        elem = driver.find_element_by_id("scan-response-message-container")
        elem2 = driver.find_element_by_id("offerColumn")
        
        if 'Sorry' in elem.text:
            price = int(0)
            #print('sorry')
        elif 'Unfortunately' in elem.text:
            price = int(0)
            #print('Unfortunately')
        else:
            elem2 = driver.find_element_by_id("offerColumn")
            price = int(round(float(elem2.text[1:])*100))
    except NoSuchElementException:
        price = int(0)
    #print(SKU,',',price)
    return price
def Ziffit_Get_Price_List(SKU_List, Ziffit_Price_List):
    global Ziffit_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = Ziffit_Get_Price(SKU)
        Ziffit_Basket_Total = Ziffit_Basket_Total + price
        #print(Ziffit_Basket_Total)
        Ziffit_Price_List.append(price)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    return Ziffit_Price_List

def MM_Get_Price_List(SKU_List, MM_Price_List):
    global MM_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = MM_Get_Price(SKU)
        MM_Basket_Total = MM_Basket_Total + price
        MM_Price_List.append(price)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    return MM_Price_List
def MM_Get_Price(SKU):
    URL = 'http://www.musicmagpie.co.uk/start-selling/basket-media'
    driver.get(URL)
    try:
        driver.find_element_by_id("txtBarcode").clear()
        driver.find_element_by_id("txtBarcode").send_keys(SKU)
        driver.find_element_by_id("getValSmall").click()
        
        elem = driver.find_element_by_id("lblMessage1")
        
        if "don't" in elem.text:
            price = int(0)
            return price
        else:
            prepprice = re.search('<div class="col_Price">(.+?)</div>', driver.page_source)
            if prepprice is None:
                price = 0
            else:
                price = int(round(float(prepprice.group(1))*100))
    except NoSuchElementException:
        price = 1
    return price

def WeBuy_Get_Price_List(SKU_List, WeBuy_Price_List):
    
    global WeBuy_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = WeBuy_Get_Price(SKU)
        WeBuy_Basket_Total = WeBuy_Basket_Total + price
        WeBuy_Price_List.append(price)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    return WeBuy_Price_List
def WeBuy_Get_Price(SKU):
    URL = 'https://uk.webuy.com/product.php?sku=' + SKU
    driver.get(URL)
    try:
        elem = driver.find_element_by_id('Acashprice')
        price = int(round(float(elem.text[1:])*100))
        driver.find_element_by_css_selector("div.sellNowButton > span").click()    
    except NoSuchElementException:
        price = 0
    return price

def Zapper_Get_Price_List(SKU_List, Zapper_Price_List):
    loginURL = "https://zapper.co.uk/sell-books-cds-dvds-games.html"
    driver.get(loginURL)
    time.sleep(1)  
    driver.find_element_by_link_text("Log In").click()
    time.sleep(1) 
    driver.find_element_by_id("zapper_email_input").clear()
    driver.find_element_by_id("zapper_email_input").send_keys(credentials.Zapper_Username)
    time.sleep(1)
    driver.find_element_by_id("zapper_password_input").clear()
    driver.find_element_by_id("zapper_password_input").send_keys(credentials.Zapper_Password)
    driver.find_element_by_link_text("LOG IN").click()
    try:
        time.sleep(1)
        driver.find_element_by_id("cb_select_all").click()
        time.sleep(1)
        driver.find_element_by_link_text("Remove selected items").click()
        time.sleep(1)
    except:
        time.sleep(1)
    global Zapper_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = Zapper_Get_Price(SKU)
        Zapper_Basket_Total = Zapper_Basket_Total + price
        #print(Zapper_Basket_Total)
        Zapper_Price_List.append(price)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    return Zapper_Price_List
def Zapper_Get_Price(SKU):
    URL = 'https://zapper.co.uk/sell-books-cds-dvds-games.html'
    driver.get(URL)
    try:
        driver.find_element_by_id("identifier_input").clear()
        driver.find_element_by_id("identifier_input").send_keys(SKU)
        driver.find_element_by_css_selector("a.barcodesubmit_addtolist").click()
        
        time.sleep(1)
    
        errortext = driver.find_element_by_id('list_items_form').text
        error = errortext.split(".")[0]
        
        if "Barcode not recognised" in error:
            price = int(0)
            #print(SKU,price,error)
        elif "already in your list" in error:
            price = int(0)
            #print(SKU,price,error)
        elif "not currently accepting" in error:
            price = int(0)
        else:
            pricetext = driver.find_element_by_id("firstrow").text
            price = int(float(pricetext.split("£")[1])*100)
    except NoSuchElementException:
        price = 1
    return price

def wbb_Get_Price_List(SKU_List, wbb_Price_List):
    global wbb_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = wbb_Get_Price(SKU)
        wbb_Basket_Total = wbb_Basket_Total + price
        wbb_Price_List.append(price)
        #print("baskettotal=",wbb_Basket_Total)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    return wbb_Price_List
def wbb_Get_Price(SKU):
    URL = 'http://www.webuybooks.co.uk/selling-basket/'
    driver.get(URL)
    try:
        driver.find_element_by_id("isbn").clear()
        driver.find_element_by_id("isbn").send_keys(SKU + Keys.ENTER)
        time.sleep(2)
        errortext = driver.find_element_by_id('error_modal').text
        error = errortext.split(".")[0]
        #print("errorlen=",len(error))
        if len(error) > 0:
            price = int(0)
        else:
            pricetext = driver.find_element_by_id("sellingb").text
            pricetext2 = pricetext.split("\n")[1]
            price = float(pricetext2.split("£")[1])*100
            price = round(price,0) 
            price = int(price)
    except NoSuchElementException:
        price = 0
    return price

SKU_List = []
SKU_List = SKU_File_To_List(SKU_List)

num_SKUs = len(SKU_List)
num_requests_total = num_SKUs * 5
num_requests = 0
        
WeBuy_Basket_Total = int(0)
WeBuy_Price_List = []
WeBuy_Price_List = WeBuy_Get_Price_List(SKU_List, WeBuy_Price_List)
print("Webuytotal=",WeBuy_Basket_Total)

Ziffit_Basket_Total = int(0)
Ziffit_Price_List = []
Ziffit_Price_List = Ziffit_Get_Price_List(SKU_List, Ziffit_Price_List)
print("Ziffittotal=",Ziffit_Basket_Total)

MM_Basket_Total = int(0)
MM_Price_List = []
MM_Price_List = MM_Get_Price_List(SKU_List, MM_Price_List)
print("mmtotal=",MM_Basket_Total)

Zapper_Basket_Total = int(0)
Zapper_Price_List = []
Zapper_Price_List = Zapper_Get_Price_List(SKU_List, Zapper_Price_List)
print("zappertotal=",Zapper_Basket_Total)

wbb_Basket_Total = int(0)
wbb_Price_List = []
wbb_Price_List = wbb_Get_Price_List(SKU_List, wbb_Price_List)
print("wbbtotal=",wbb_Basket_Total)

Master_List = list(zip(SKU_List, WeBuy_Price_List, Ziffit_Price_List, MM_Price_List, Zapper_Price_List, wbb_Price_List))
with open("output3.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['SKU','WeBuy', 'Ziffit', 'MM','Zapper', 'WBB'])
    writer.writerows(Master_List)
#driver.quit()

print(time.ctime(time.time()))
