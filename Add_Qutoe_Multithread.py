import time
import credentials
import re
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import time

class myThread (threading.Thread):
    def __init__(self, threadID, name, seller):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.seller = seller
    def run(self):
        global WeBuy_Price_List
        global Ziffit_Price_List
        global MM_Price_List
        global Zapper_Price_List
        global wbb_Price_List
        print("Starting thread" + self.name)
        if (self.seller == "WeBuy"):
            WeBuy_Price_List = WeBuy_Get_Price_List(SKU_List, WeBuy_Price_List)
        elif (self.seller == "Ziffit"):
            Ziffit_Price_List = Ziffit_Get_Price_List(SKU_List, Ziffit_Price_List)
        elif (self.seller == "MM"):
            MM_Price_List = MM_Get_Price_List(SKU_List, MM_Price_List)
        elif (self.seller == "Zapper"):
            Zapper_Price_List = Zapper_Get_Price_List(SKU_List, Zapper_Price_List)
        elif (self.seller == "WBB"):
            wbb_Price_List = wbb_Get_Price_List(SKU_List, wbb_Price_List)


def SKU_File_To_List(SKU_List):
    with open("SKU_File.csv") as SKU_File:
        for SKU in SKU_File:
            SKU = SKU.strip()
            if (SKU not in SKU_List):
                SKU_List.append(SKU)
    return SKU_List 

def Ziffit_Get_Price_List(SKU_List, Ziffit_Price_List):
    Ziffitdriver = webdriver.Chrome('C:\Python36\selenium\webdriver\Ziffitchromedriver.exe')
    global Ziffit_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = Ziffit_Get_Price(SKU, Ziffitdriver)
        Ziffit_Basket_Total = Ziffit_Basket_Total + price
        Ziffit_Price_List.append(price)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    Ziffitdriver.quit()
    return Ziffit_Price_List
def Ziffit_Get_Price(SKU,  Ziffitdriver):
    URL = 'https://www.ziffit.com/'
    Ziffitdriver.get(URL)
    try:
        Ziffitdriver.find_element_by_id("ean").clear()
        Ziffitdriver.find_element_by_id("ean").send_keys(SKU)
        Ziffitdriver.find_element_by_id("get-value-button").click()
        
        elem = Ziffitdriver.find_element_by_id("scan-response-message-container")
        elem2 = Ziffitdriver.find_element_by_id("offerColumn")
        
        if 'Sorry' in elem.text:
            price = int(0)
        elif 'Unfortunately' in elem.text:
            price = int(0)
        else:
            elem2 = Ziffitdriver.find_element_by_id("offerColumn")
            price = int(round(float(elem2.text[1:])*100))
    except NoSuchElementException:
        price = int(0)
    return price

def MM_Get_Price_List(SKU_List, MM_Price_List):
    MMdriver = webdriver.Chrome('C:\Python36\selenium\webdriver\MMchromedriver.exe')
    global MM_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = MM_Get_Price(SKU, MMdriver)
        MM_Basket_Total = MM_Basket_Total + price
        MM_Price_List.append(price)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    MMdriver.quit()
    return MM_Price_List
def MM_Get_Price(SKU, MMdriver):
    URL = 'http://www.musicmagpie.co.uk/start-selling/basket-media'
    MMdriver.get(URL)
    try:
        MMdriver.find_element_by_id("txtBarcode").clear()
        MMdriver.find_element_by_id("txtBarcode").send_keys(SKU)
        MMdriver.find_element_by_id("getValSmall").click()
        
        elem = MMdriver.find_element_by_id("lblMessage1")
        
        if "don't" in elem.text:
            price = int(0)
            return price
        else:
            prepprice = re.search('<div class="col_Price">(.+?)</div>', MMdriver.page_source)
            if prepprice is None:
                price = 0
            else:
                price = int(round(float(prepprice.group(1))*100))
    except NoSuchElementException:
        price = 1
    return price

def WeBuy_Get_Price_List(SKU_List, WeBuy_Price_List):
    WeBuydriver = webdriver.Chrome('C:\Python36\selenium\webdriver\WeBuychromedriver.exe')
    global WeBuy_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = WeBuy_Get_Price(SKU, WeBuydriver)
        WeBuy_Basket_Total = WeBuy_Basket_Total + price
        WeBuy_Price_List.append(price)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    WeBuydriver.quit()
    return WeBuy_Price_List
def WeBuy_Get_Price(SKU, WeBuydriver):
    URL = 'https://uk.webuy.com/product.php?sku=' + SKU
    WeBuydriver.get(URL)
    try:
        elem = WeBuydriver.find_element_by_id('Acashprice')
        price = int(round(float(elem.text[1:])*100))
        WeBuydriver.find_element_by_css_selector("div.sellNowButton > span").click()    
    except NoSuchElementException:
        price = 0
    return price

def Zapper_Get_Price_List(SKU_List, Zapper_Price_List):
    Zapperdriver = webdriver.Chrome('C:\Python36\selenium\webdriver\Zapperchromedriver.exe')
    loginURL = "https://zapper.co.uk/sell-books-cds-dvds-games.html"
    Zapperdriver.get(loginURL)
    time.sleep(1)  
    Zapperdriver.find_element_by_link_text("Log In").click()
    time.sleep(1) 
    Zapperdriver.find_element_by_id("zapper_email_input").clear()
    Zapperdriver.find_element_by_id("zapper_email_input").send_keys(credentials.Zapper_Username)
    time.sleep(1)
    Zapperdriver.find_element_by_id("zapper_password_input").clear()
    Zapperdriver.find_element_by_id("zapper_password_input").send_keys(credentials.Zapper_Password)
    Zapperdriver.find_element_by_link_text("LOG IN").click()
    try:
        time.sleep(1)
        Zapperdriver.find_element_by_id("cb_select_all").click()
        time.sleep(1)
        Zapperdriver.find_element_by_link_text("Remove selected items").click()
        time.sleep(1)
    except:
        print("empty")
    global Zapper_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = Zapper_Get_Price(SKU, Zapperdriver)
        Zapper_Basket_Total = Zapper_Basket_Total + price
        #print(Zapper_Basket_Total)
        Zapper_Price_List.append(price)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    Zapperdriver.quit()
    return Zapper_Price_List
def Zapper_Get_Price(SKU, Zapperdriver):
    URL = 'https://zapper.co.uk/sell-books-cds-dvds-games.html'
    Zapperdriver.get(URL)
    try:
        Zapperdriver.find_element_by_id("identifier_input").clear()
        Zapperdriver.find_element_by_id("identifier_input").send_keys(SKU)
        Zapperdriver.find_element_by_css_selector("a.barcodesubmit_addtolist").click()
        
        time.sleep(1)
    
        errortext = Zapperdriver.find_element_by_id('list_items_form').text
        error = errortext.split(".")[0]
        
        if "Barcode not recognised" in error:
            price = int(0)
        elif "already in your list" in error:
            price = int(0)
        elif "not currently accepting" in error:
            price = int(0)
        else:
            pricetext = Zapperdriver.find_element_by_id("firstrow").text
            price = int(float(pricetext.split("£")[1])*100)
    except NoSuchElementException:
        price = 1
    return price

def wbb_Get_Price_List(SKU_List, wbb_Price_List):
    WBBdriver = webdriver.Chrome('C:\Python36\selenium\webdriver\WBBchromedriver.exe')
    global wbb_Basket_Total
    global num_requests
    global num_requests_total
    for SKU in SKU_List:
        price = wbb_Get_Price(SKU, WBBdriver)
        wbb_Basket_Total = wbb_Basket_Total + price
        wbb_Price_List.append(price)
        num_requests = num_requests + 1
        #print(num_requests,"/",num_requests_total)
    WBBdriver.quit()
    return wbb_Price_List
def wbb_Get_Price(SKU, WBBdriver):
    URL = 'http://www.webuybooks.co.uk/selling-basket/'
    WBBdriver.get(URL)
    try:
        WBBdriver.find_element_by_id("isbn").clear()
        WBBdriver.find_element_by_id("isbn").send_keys(SKU + Keys.ENTER)
        time.sleep(2)
        errortext = WBBdriver.find_element_by_id('error_modal').text
        error = errortext.split(".")[0]
        if len(error) > 0:
            price = int(0)
        else:
            pricetext = WBBdriver.find_element_by_id("sellingb").text
            pricetext2 = pricetext.split("\n")[1]
            price = float(pricetext2.split("£")[1])*100
            price = round(price,0) 
            price = int(price)
    except NoSuchElementException:
        price = 0
    return price


print(time.ctime(time.time()))

SKU_List = []
SKU_List = SKU_File_To_List(SKU_List)

num_SKUs = len(SKU_List)
print(len(SKU_List))
num_requests_total = num_SKUs * 5
num_requests = 0
        
WeBuy_Basket_Total = int(0)
WeBuy_Price_List = []
print("Webuytotal=",WeBuy_Basket_Total)

Ziffit_Basket_Total = int(0)
Ziffit_Price_List = []
print("Ziffittotal=",Ziffit_Basket_Total)

MM_Basket_Total = int(0)
MM_Price_List = []
print("mmtotal=",MM_Basket_Total)

Zapper_Basket_Total = int(0)
Zapper_Price_List = []
print("zappertotal=",Zapper_Basket_Total)

wbb_Basket_Total = int(0)
wbb_Price_List = []
print("wbbtotal=",wbb_Basket_Total)

threads = []
# Create new threads
thread1 = myThread(1, "WeBuy", "WeBuy")
thread2 = myThread(2, "Ziffit", "Ziffit")
thread3 = myThread(3, "MM", "MM")
thread4 = myThread(4, "Zapper", "Zapper")
thread5 = myThread(5, "WBB", "WBB")
# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
# Add threads to thread list
threads.append(thread1)
threads.append(thread2)
threads.append(thread3)
threads.append(thread4)
threads.append(thread5)

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")

Master_List = list(zip(SKU_List, WeBuy_Price_List, Ziffit_Price_List, MM_Price_List, Zapper_Price_List, wbb_Price_List))
with open("output3.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['SKU','WeBuy', 'Ziffit', 'MM','Zapper', 'WBB'])
    writer.writerows(Master_List)
    
print(time.ctime(time.time()))