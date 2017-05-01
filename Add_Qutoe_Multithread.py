# import time
# import credentials
# import re
# import csv
# from selenium.common.exceptions import NoSuchElementException
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import threading
# import time
# 
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, seller):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.seller = seller
#     def run(self):
#         global WeBuy_Price_List
#         global Ziffit_Price_List
#         global MM_Price_List
#         global Zapper_Price_List
#         global wbb_Price_List
#         print("Starting thread" + self.name)
#         if (self.seller == "WeBuy"):
#             WeBuy_Price_List = WeBuy_Get_Price_List(SKU_List, WeBuy_Price_List)
#         elif (self.seller == "Ziffit"):
#             Ziffit_Price_List = Ziffit_Get_Price_List(SKU_List, Ziffit_Price_List)
#         elif (self.seller == "MM"):
#             MM_Price_List = MM_Get_Price_List(SKU_List, MM_Price_List)
#         elif (self.seller == "Zapper"):
#             Zapper_Price_List = Zapper_Get_Price_List(SKU_List, Zapper_Price_List)
#         elif (self.seller == "WBB"):
#             wbb_Price_List = wbb_Get_Price_List(SKU_List, wbb_Price_List)
# 
# 
# def SKU_File_To_List2(SKU_List):
#     with open("SKU_File2.csv") as SKU_File:
#         for SKU in SKU_File:
#             SKU = SKU.strip()
#             if (SKU not in SKU_List):
#                 SKU_List.append(SKU)
#     return SKU_List 
# 
# def Ziffit_Get_Price_List(SKU_List, Ziffit_Price_List):
#     Ziffitdriver = webdriver.Chrome('C:\Python36\selenium\webdriver\Ziffitchromedriver.exe')
#     global Ziffit_Basket_Total
#     global num_requests
#     global num_requests_total
#     for SKU in SKU_List:
#         price = Ziffit_Get_Price(SKU, Ziffitdriver)
#         Ziffit_Basket_Total = Ziffit_Basket_Total + price
#         Ziffit_Price_List.append(price)
#         num_requests = num_requests + 1
#         #print(num_requests,"/",num_requests_total)
#     Ziffitdriver.quit()
#     return Ziffit_Price_List
# def Ziffit_Get_Price(SKU,  Ziffitdriver):
#     URL = 'https://www.ziffit.com/'
#     Ziffitdriver.get(URL)
#     try:
#         Ziffitdriver.find_element_by_id("ean").clear()
#         Ziffitdriver.find_element_by_id("ean").send_keys(SKU)
#         Ziffitdriver.find_element_by_id("get-value-button").click()
#         
#         elem = Ziffitdriver.find_element_by_id("scan-response-message-container")
#         elem2 = Ziffitdriver.find_element_by_id("offerColumn")
#         
#         if 'Sorry' in elem.text:
#             price = int(0)
#         elif 'Unfortunately' in elem.text:
#             price = int(0)
#         else:
#             elem2 = Ziffitdriver.find_element_by_id("offerColumn")
#             price = int(round(float(elem2.text[1:])*100))
#     except:
#         price = int(0)
#     return price
# 
# def MM_Get_Price_List(SKU_List, MM_Price_List):
#     MMdriver = webdriver.Chrome('C:\Python36\selenium\webdriver\MMchromedriver.exe')
#     global MM_Basket_Total
#     global num_requests
#     global num_requests_total
#     for SKU in SKU_List:
#         price = MM_Get_Price(SKU, MMdriver)
#         MM_Basket_Total = MM_Basket_Total + price
#         MM_Price_List.append(price)
#         num_requests = num_requests + 1
#         #print(num_requests,"/",num_requests_total)
#     MMdriver.quit()
#     return MM_Price_List
# def MM_Get_Price(SKU, MMdriver):
#     URL = 'http://www.musicmagpie.co.uk/start-selling/basket-media'
#     MMdriver.get(URL)
#     try:
#         MMdriver.find_element_by_id("txtBarcode").clear()
#         MMdriver.find_element_by_id("txtBarcode").send_keys(SKU)
#         MMdriver.find_element_by_id("getValSmall").click()
#         
#         elem = MMdriver.find_element_by_id("lblMessage1")
#         
#         if "don't" in elem.text:
#             price = int(0)
#             return price
#         else:
#             prepprice = re.search('<div class="col_Price">(.+?)</div>', MMdriver.page_source)
#             if prepprice is None:
#                 price = 0
#             else:
#                 price = int(round(float(prepprice.group(1))*100))
#     except:
#         price = int(0)
#     return price
# 
# def WeBuy_Get_Price_List(SKU_List, WeBuy_Price_List):
#     WeBuydriver = webdriver.Chrome('C:\Python36\selenium\webdriver\WeBuychromedriver.exe')
#     global WeBuy_Basket_Total
#     global num_requests
#     global num_requests_total
#     for SKU in SKU_List:
#         price = WeBuy_Get_Price(SKU, WeBuydriver)
#         WeBuy_Basket_Total = WeBuy_Basket_Total + price
#         WeBuy_Price_List.append(price)
#         num_requests = num_requests + 1
#         #print(num_requests,"/",num_requests_total)
#     WeBuydriver.quit()
#     return WeBuy_Price_List
# def WeBuy_Get_Price(SKU, WeBuydriver):
#     URL = 'https://uk.webuy.com/product.php?sku=' + SKU
#     WeBuydriver.get(URL)
#     try:
#         elem = WeBuydriver.find_element_by_id('Acashprice')
#         price = int(round(float(elem.text[1:])*100))
#         WeBuydriver.find_element_by_css_selector("div.sellNowButton > span").click()    
#     except:
#         price = int(0)
#     return price
# 
# def Zapper_Get_Price_List(SKU_List, Zapper_Price_List):
#     Zapperdriver = webdriver.Chrome('C:\Python36\selenium\webdriver\Zapperchromedriver.exe')
#     loginURL = "https://zapper.co.uk/sell-books-cds-dvds-games.html"
#     Zapperdriver.get(loginURL)
#     time.sleep(1)  
#     Zapperdriver.find_element_by_link_text("Log In").click()
#     time.sleep(1) 
#     Zapperdriver.find_element_by_id("zapper_email_input").clear()
#     Zapperdriver.find_element_by_id("zapper_email_input").send_keys(credentials.Zapper_Username)
#     time.sleep(1)
#     Zapperdriver.find_element_by_id("zapper_password_input").clear()
#     Zapperdriver.find_element_by_id("zapper_password_input").send_keys(credentials.Zapper_Password)
#     Zapperdriver.find_element_by_link_text("LOG IN").click()
#     try:
#         time.sleep(1)
#         Zapperdriver.find_element_by_id("cb_select_all").click()
#         time.sleep(1)
#         Zapperdriver.find_element_by_link_text("Remove selected items").click()
#         time.sleep(1)
#     except:
#         print("empty")
#     global Zapper_Basket_Total
#     global num_requests
#     global num_requests_total
#     for SKU in SKU_List:
#         price = Zapper_Get_Price(SKU, Zapperdriver)
#         Zapper_Basket_Total = Zapper_Basket_Total + price
#         #print(Zapper_Basket_Total)
#         Zapper_Price_List.append(price)
#         num_requests = num_requests + 1
#         #print(num_requests,"/",num_requests_total)
#     Zapperdriver.quit()
#     return Zapper_Price_List
# def Zapper_Get_Price(SKU, Zapperdriver):
#     URL = 'https://zapper.co.uk/sell-books-cds-dvds-games.html'
#     Zapperdriver.get(URL)
#     try:
#         Zapperdriver.find_element_by_id("identifier_input").clear()
#         Zapperdriver.find_element_by_id("identifier_input").send_keys(SKU)
#         Zapperdriver.find_element_by_css_selector("a.barcodesubmit_addtolist").click()
#         
#         time.sleep(1)
#     
#         errortext = Zapperdriver.find_element_by_id('list_items_form').text
#         error = errortext.split(".")[0]
#         
#         if "Barcode not recognised" in error:
#             price = int(0)
#         elif "already in your list" in error:
#             price = int(0)
#         elif "not currently accepting" in error:
#             price = int(0)
#         else:
#             pricetext = Zapperdriver.find_element_by_id("firstrow").text
#             price = int(float(pricetext.split("£")[1])*100)
#     except:
#         price = int(0)
#     return price
# 
# def wbb_Get_Price_List(SKU_List, wbb_Price_List):
#     WBBdriver = webdriver.Chrome('C:\Python36\selenium\webdriver\WBBchromedriver.exe')
#     global wbb_Basket_Total
#     global num_requests
#     global num_requests_total
#     for SKU in SKU_List:
#         price = wbb_Get_Price(SKU, WBBdriver)
#         wbb_Basket_Total = wbb_Basket_Total + price
#         wbb_Price_List.append(price)
#         num_requests = num_requests + 1
#         #print(num_requests,"/",num_requests_total)
#     WBBdriver.quit()
#     return wbb_Price_List
# def wbb_Get_Price(SKU, WBBdriver):
#     URL = 'http://www.webuybooks.co.uk/selling-basket/'
#     WBBdriver.get(URL)
#     try:
#         WBBdriver.find_element_by_id("isbn").clear()
#         WBBdriver.find_element_by_id("isbn").send_keys(SKU + Keys.ENTER)
#         time.sleep(2)
#         errortext = WBBdriver.find_element_by_id('error_modal').text
#         error = errortext.split(".")[0]
#         if len(error) > 0:
#             price = int(0)
#         else:
#             pricetext = WBBdriver.find_element_by_id("sellingb").text
#             pricetext2 = pricetext.split("\n")[1]
#             price = float(pricetext2.split("£")[1])*100
#             price = round(price,0) 
#             price = int(price)
#     except:
#         price = int(0)
#     return price
# 
# 
# print(time.ctime(time.time()))
# 
# SKU_List = []
# SKU_List = SKU_File_To_List2(SKU_List)
#   
# num_SKUs = len(SKU_List)
# print(len(SKU_List))
# num_requests_total = num_SKUs * 5
# num_requests = 0
#           
# WeBuy_Basket_Total = int(0)
# WeBuy_Price_List = []
# print("Webuytotal=",WeBuy_Basket_Total)
#   
# Ziffit_Basket_Total = int(0)
# Ziffit_Price_List = []
# print("Ziffittotal=",Ziffit_Basket_Total)
#   
# MM_Basket_Total = int(0)
# MM_Price_List = []
# print("mmtotal=",MM_Basket_Total)
#   
# Zapper_Basket_Total = int(0)
# Zapper_Price_List = []
# print("zappertotal=",Zapper_Basket_Total)
#   
# wbb_Basket_Total = int(0)
# wbb_Price_List = []
# print("wbbtotal=",wbb_Basket_Total)
#   
# threads = []
# # Create new threads
# thread1 = myThread(1, "WeBuy", "WeBuy")
# thread2 = myThread(2, "Ziffit", "Ziffit")
# thread3 = myThread(3, "MM", "MM")
# thread4 = myThread(4, "Zapper", "Zapper")
# thread5 = myThread(5, "WBB", "WBB")
# # Start new Threads
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()
# # Add threads to thread list
# threads.append(thread1)
# threads.append(thread2)
# threads.append(thread3)
# threads.append(thread4)
# threads.append(thread5)
#   
# # Wait for all threads to complete
# for t in threads:
#     t.join()
# print("Exiting Main Thread")
#   
# Master_List = list(zip(SKU_List, WeBuy_Price_List, Ziffit_Price_List, MM_Price_List, Zapper_Price_List, wbb_Price_List))
# with open("output3.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(['SKU','WeBuy', 'Ziffit', 'MM','Zapper', 'WBB'])
#     writer.writerows(Master_List)
# #      
#      
# 
# 
# 
# def Assign_Shops(To_Be_Sorted):
#     WeBuy_Sell_List.clear()
#     Ziffit_Sell_List.clear()
#     MM_Sell_List.clear()
#     Zapper_Sell_List.clear()
#     wbb_Sell_List.clear()
#     Rejected_Sell_List.clear()
#     RejectedCount = 0
#     for item in To_Be_Sorted:
#         SKU = item[0]
#         if WeBuy_Status == 1:
#             WeBuyPrice = item[1]
#         else:
#             WeBuyPrice = 0
#         if Ziffit_Status == 1:
#             ZiffitPrice = item[2]
#         else:
#             ZiffitPrice = 0
#         if MM_Status == 1:
#             MMPrice = item[3]
#         else:
#             MMPrice = 0
#         if Zapper_Status == 1:
#             ZapperPrice = item[4]
#         else:
#             ZapperPrice = 0
#         if wbb_Status == 1:
#             wbbPrice = item[5]
#         else:
#             wbbPrice = 0
#         
#         if WeBuyPrice >= max(ZiffitPrice, MMPrice, ZapperPrice, wbbPrice) and WeBuyPrice > 0:
#             WeBuy_Sell_List.append([SKU, WeBuyPrice])
#             
#         elif ZiffitPrice >= max(WeBuyPrice, MMPrice, ZapperPrice, wbbPrice) and ZiffitPrice > 0:
#             Ziffit_Sell_List.append([SKU, ZiffitPrice])
#             
#         elif MMPrice >= max(WeBuyPrice, ZiffitPrice, ZapperPrice, wbbPrice) and MMPrice > 0:
#             MM_Sell_List.append([SKU, MMPrice])
#             
#         elif ZapperPrice >= max(WeBuyPrice, ZiffitPrice, MMPrice, wbbPrice) and ZapperPrice > 0:
#             Zapper_Sell_List.append([SKU, ZapperPrice])
#             
#         elif wbbPrice >= max(WeBuyPrice, ZiffitPrice, MMPrice, ZapperPrice) and wbbPrice > 0:
#             wbb_Sell_List.append([SKU, wbbPrice])
#         else:
#             Rejected_Sell_List.append(SKU)
#             RejectedCount = RejectedCount + 1
#     return RejectedCount
#             
#         
# def Filter_Mins(Sell_List, min_price, shop):
#     pricesum = 0
#     for item in Sell_List:
#         price = item[1]
#         pricesum = pricesum + price
#     if pricesum < min_price:
#         if shop == "WeBuy":
#             global WeBuy_Status
#             WeBuy_Status = 0
#         if shop == "Ziffit":
#             global Ziffit_Status
#             Ziffit_Status = 0
#         if shop == "MM":
#             global MM_Status
#             MM_Status = 0
#         if shop == "Zapper":
#             global Zapper_Status
#             Zapper_Status = 0
#         if shop == "wbb":
#             global wbb_Status
#             wbb_Status = 0
# 
#     
# 
# def Sort_Shops(Master_List):     
#     
#     global Ziffit_Sell_List
#     global WeBuy_Sell_List
#     global Ziffit_Sell_List
#     global Zapper_Sell_List
#     global MM_Sell_List
#     global wbb_Sell_List
#     global Rejected_Sell_List
#     
#     To_Be_Sorted = Master_List
#     WeBuy_Sell_List = []
#     Ziffit_Sell_List = []
#     MM_Sell_List = []
#     Zapper_Sell_List = []
#     wbb_Sell_List = []
#     Rejected_Sell_List = []
#     
#     global WeBuy_Status
#     global Ziffit_Status
#     global MM_Status
#     global Zapper_Status
#     global wbb_Status
#     
#     WeBuy_Status = 0
#     Ziffit_Status = 0
#     MM_Status = 0
#     Zapper_Status = 1
#     wbb_Status = 0
#     
#     WeBuy_Min = 200
#     Ziffit_Min = 200
#     MM_Min = 200
#     Zapper_Min = 200
#     wbb_Min = 200
#        
#     Assign_Shops(To_Be_Sorted)
#     Filter_Mins(WeBuy_Sell_List, WeBuy_Min, "WeBuy")
#     Filter_Mins(Ziffit_Sell_List, Ziffit_Min, "Ziffit")
#     Filter_Mins(MM_Sell_List, MM_Min, "MM")
#     Filter_Mins(Zapper_Sell_List, Zapper_Min, "Zapper")
#     print("wbbstat=",wbb_Status)
#     Filter_Mins(wbb_Sell_List, wbb_Min, "wbb")
#     print("wbbstat=",wbb_Status)
#     Assign_Shops(To_Be_Sorted)
#     print("totallen=", len(WeBuy_Sell_List) + len(Ziffit_Sell_List) + len(MM_Sell_List) + len(Zapper_Sell_List) + len(wbb_Sell_List) + len(Rejected_Sell_List))
#     print("totalmaster=", len(Master_List))
#     if len(WeBuy_Sell_List) + len(Ziffit_Sell_List) + len(MM_Sell_List) + len(Zapper_Sell_List) + len(wbb_Sell_List) + len(Rejected_Sell_List) < len(Master_List):
#         Sort_Shops(Master_List)
#         
#     with open("webuy.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerows(WeBuy_Sell_List)
#     with open("ziffit.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerows(Ziffit_Sell_List)
#     with open("mm.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerows(MM_Sell_List)
#     with open("zapper.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerows(Zapper_Sell_List)
#     with open("wbb.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerows(wbb_Sell_List)
#     with open("rejected.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerows(Rejected_Sell_List)   
# 
#         
# Sort_Shops(Master_List)
# 
# 
#  
# def SKU_File_To_List(file):
#     with open(file) as SKU_File:
#         reader = csv.reader(SKU_File)
#         your_list = list(reader)
#         SKU_List=[]
#         for item in your_list:
#             SKU = item[0].strip()
#             if (SKU not in SKU_List):
#                 SKU_List.append(SKU)
#     return SKU_List
# 
def SoldSKU_File_To_List(file):
    import csv
    with open(file) as SKU_File:
        reader = csv.reader(SKU_File)
        your_list = list(reader)
        SKU_List=[]
        for item in your_list:
            SKU = item[0].strip()
            if (SKU not in SKU_List) and int(item[1]) > 0:
                SKU_List.append(SKU)
    return SKU_List 
#  
# def Ziffit_Add_Price_List(Ziffitdriver, SKU_List, Ziffit_Price_List):
#     for SKU in SKU_List:
#         price = Ziffit_Add_Price(SKU, Ziffitdriver)
#         Ziffit_Price_List.append(price)
#     #Ziffitdriver.quit()
#     return Ziffit_Price_List
# def Ziffit_Add_Price(SKU,  Ziffitdriver):
#     URL = 'https://www.ziffit.com/'
#     Ziffitdriver.get(URL)
#     try:
#         Ziffitdriver.find_element_by_id("ean").clear()
#         Ziffitdriver.find_element_by_id("ean").send_keys(SKU)
#         Ziffitdriver.find_element_by_id("get-value-button").click()
#          
#         elem = Ziffitdriver.find_element_by_id("scan-response-message-container")
#         elem2 = Ziffitdriver.find_element_by_id("offerColumn")
#          
#         if 'Sorry' in elem.text:
#             price = int(0)
#         elif 'Unfortunately' in elem.text:
#             price = int(0)
#         else:
#             elem2 = Ziffitdriver.find_element_by_id("offerColumn")
#             price = int(round(float(elem2.text[1:])*100))
#     except:
#         price = int(0)
#     return price
#  
# def MM_Add_Price_List(MMdriver, SKU_List, MM_Price_List):
#     for SKU in SKU_List:
#         price = MM_Add_Price(SKU, MMdriver)
#         MM_Price_List.append(price)
#     return MM_Price_List
#  
# def MM_Add_Price(SKU, MMdriver):
#     URL = 'http://www.musicmagpie.co.uk/start-selling/basket-media'
#     MMdriver.get(URL)
#     try:
#         MMdriver.find_element_by_id("txtBarcode").clear()
#         MMdriver.find_element_by_id("txtBarcode").send_keys(SKU)
#         MMdriver.find_element_by_id("getValSmall").click()
#          
#         elem = MMdriver.find_element_by_id("lblMessage1")
#          
#         if "don't" in elem.text:
#             price = int(0)
#             return price
#         else:
#             prepprice = re.search('<div class="col_Price">(.+?)</div>', MMdriver.page_source)
#             if prepprice is None:
#                 price = 0
#             else:
#                 price = int(round(float(prepprice.group(1))*100))
#     except:
#         price = int(0)
#     return price
#  
# def WeBuy_Add_Price_List(WeBuyDriver, SKU_List, WeBuy_Price_List):
#     for SKU in SKU_List:
#         print(SKU)
#         price = WeBuy_Add_Price(SKU, WeBuyDriver)
#         WeBuy_Price_List.append(price)
#     return WeBuy_Price_List
# def WeBuy_Add_Price(SKU, WeBuydriver):
#     URL = 'https://uk.webuy.com/product.php?sku=' + str(SKU)
#     WeBuydriver.get(URL)
#     try:
#         elem = WeBuydriver.find_element_by_id('Acashprice')
#         price = int(round(float(elem.text[1:])*100))
#         WeBuydriver.find_element_by_css_selector("div.sellNowButton > span").click()    
#     except:
#         price = int(0)
#     return price
#  
# def Zapper_Add_Price_List(Zapperdriver, SKU_List, Zapper_Price_List):
#     loginURL = "https://zapper.co.uk/sell-books-cds-dvds-games.html"
#     Zapperdriver.get(loginURL)
#     time.sleep(1)  
#     Zapperdriver.find_element_by_link_text("Log In").click()
#     time.sleep(1) 
#     Zapperdriver.find_element_by_id("zapper_email_input").clear()
#     Zapperdriver.find_element_by_id("zapper_email_input").send_keys(credentials.Zapper_Username)
#     time.sleep(1)
#     Zapperdriver.find_element_by_id("zapper_password_input").clear()
#     Zapperdriver.find_element_by_id("zapper_password_input").send_keys(credentials.Zapper_Password)
#     Zapperdriver.find_element_by_link_text("LOG IN").click()
#     try:
#         time.sleep(1)
#         Zapperdriver.find_element_by_id("cb_select_all").click()
#         time.sleep(1)
#         Zapperdriver.find_element_by_link_text("Remove selected items").click()
#         time.sleep(1)
#     except:
#         print("empty")
#     for SKU in SKU_List:
#         price = Zapper_Add_Price(SKU, Zapperdriver)
#         Zapper_Price_List.append(price)
#     #Zapperdriver.quit()
#     return Zapper_Price_List
# def Zapper_Add_Price(SKU, Zapperdriver):
#     URL = 'https://zapper.co.uk/sell-books-cds-dvds-games.html'
#     Zapperdriver.get(URL)
#     try:
#         Zapperdriver.find_element_by_id("identifier_input").clear()
#         Zapperdriver.find_element_by_id("identifier_input").send_keys(SKU)
#         Zapperdriver.find_element_by_css_selector("a.barcodesubmit_addtolist").click()
#          
#         time.sleep(1)
#      
#         errortext = Zapperdriver.find_element_by_id('list_items_form').text
#         error = errortext.split(".")[0]
#          
#         if "Barcode not recognised" in error:
#             price = int(0)
#         elif "already in your list" in error:
#             price = int(0)
#         elif "not currently accepting" in error:
#             price = int(0)
#         else:
#             pricetext = Zapperdriver.find_element_by_id("firstrow").text
#             price = int(float(pricetext.split("£")[1])*100)
#     except:
#         price = int(0)
#     return price
#  
# def wbb_Add_Price_List(WBBdriver, SKU_List, wbb_Price_List):
#     for SKU in SKU_List:
#         price = wbb_Add_Price(SKU, WBBdriver)
#         wbb_Price_List.append(price)
#     return wbb_Price_List
# def wbb_Add_Price(SKU, WBBdriver):
#     URL = 'http://www.webuybooks.co.uk/selling-basket/'
#     WBBdriver.get(URL)
#     try:
#         WBBdriver.find_element_by_id("isbn").clear()
#         WBBdriver.find_element_by_id("isbn").send_keys(SKU + Keys.ENTER)
#         time.sleep(2)
#         errortext = WBBdriver.find_element_by_id('error_modal').text
#         error = errortext.split(".")[0]
#         if len(error) > 0:
#             price = int(0)
#         else:
#             pricetext = WBBdriver.find_element_by_id("sellingb").text
#             pricetext2 = pricetext.split("\n")[1]
#             price = float(pricetext2.split("£")[1])*100
#             price = round(price,0) 
#             price = int(price)
#     except:
#         price = int(0)
#     return price
# 
#     
# WeBuy_Sell_List = []
# WeBuy_List = []
# WeBuyList = SKU_File_To_List("webuy.csv")
# print(WeBuyList)
# WeBuyDriver = webdriver.Chrome('C:\Python36\selenium\webdriver\WeBuychromedriver.exe')
# WeBuy_Sell_List = WeBuy_Add_Price_List(WeBuyDriver, WeBuyList, WeBuy_Sell_List)
# WeBuyMaster = list(zip(WeBuyList, WeBuy_Sell_List))
# with open("webuyoutput3.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(WeBuyMaster)
#       
# Ziffit_Sell_List = []
# Ziffit_List = []
# ZiffitList = SKU_File_To_List("ziffit.csv")
# print(ZiffitList)
# ZiffitDriver = webdriver.Chrome('C:\Python36\selenium\webdriver\Ziffitchromedriver.exe')
# Ziffit_Sell_List = Ziffit_Add_Price_List(ZiffitDriver, ZiffitList, Ziffit_Sell_List)
# ZiffitMaster = list(zip(ZiffitList, Ziffit_Sell_List))
# with open("Ziffitoutput3.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(ZiffitMaster)
#  
# MM_Sell_List = []
# MM_List = []
# MMList = SKU_File_To_List("mm.csv")
# print(MMList)
# MMDriver = webdriver.Chrome('C:\Python36\selenium\webdriver\MMchromedriver.exe')
# MM_Sell_List = MM_Add_Price_List(MMDriver, MMList, MM_Sell_List)
# MMMaster = list(zip(MMList, MM_Sell_List))
# with open("MMoutput3.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(MMMaster)
#   
# Zapper_Sell_List = []
# Zapper_List = []
# ZapperList = SKU_File_To_List("zapper.csv")
# print(ZapperList)
# ZapperDriver = webdriver.Chrome('C:\Python36\selenium\webdriver\Zapperchromedriver.exe')
# Zapper_Sell_List = Zapper_Add_Price_List(ZapperDriver, ZapperList, Zapper_Sell_List)
# ZapperMaster = list(zip(ZapperList, Zapper_Sell_List))
# with open("Zapperoutput3.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(ZapperMaster)
#            
# wbb_Sell_List = []
# wbb_List = []
# wbbList = SKU_File_To_List("wbb.csv")
# print(wbbList)
# wbbDriver = webdriver.Chrome('C:\Python36\selenium\webdriver\wbbchromedriver.exe')
# wbb_Sell_List = wbb_Add_Price_List(wbbDriver, wbbList, wbb_Sell_List)
# wbbMaster = list(zip(wbbList, wbb_Sell_List))
# with open("wbboutput3.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(wbbMaster)
# 
WeBuyList = SoldSKU_File_To_List("webuyoutput3.csv")
ZiffitList = SoldSKU_File_To_List("Ziffitoutput3.csv")
MMList = SoldSKU_File_To_List("MMoutput3.csv")
ZapperList = SoldSKU_File_To_List("Zapperoutput3.csv")
WBBList = SoldSKU_File_To_List("wbboutput3.csv")
# 
import winsound
while True:
    SKU = input("Enter SKU? ")
    if any(SKU in item for item in WeBuyList):
        print("WeBuy")
        winsound.PlaySound('Sounds/WeBuy.wav', winsound.SND_FILENAME)
    elif any(SKU in item for item in ZiffitList):
        print("Ziffit")
        winsound.PlaySound('Sounds/Ziffit.wav', winsound.SND_FILENAME)
    elif any(SKU in item for item in MMList):
        print("MusicMagpie")
        winsound.PlaySound('Sounds/MM.wav', winsound.SND_FILENAME)
    elif any(SKU in item for item in ZapperList):
        print("Zapper")
        winsound.PlaySound('Sounds/Zapper.wav', winsound.SND_FILENAME)
    elif any(SKU in item for item in WBBList):
        print("WBB")
        winsound.PlaySound('Sounds/WBB.wav', winsound.SND_FILENAME)
    else:
        print("Reject")
        winsound.PlaySound('Sounds/Reject.wav', winsound.SND_FILENAME)
# 
#         
# print(time.ctime(time.time()))