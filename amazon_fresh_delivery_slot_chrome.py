import bs4
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys
import time
import os
from twilio.rest import Client
#twilio credentials
account_sid = ""
auth_token = ""
#search area
search_area = ""

def text(msg):
   client = Client(account_sid, auth_token)
   client.messages.create(
     to="+1",
     from_="+1",
     body = msg)
   print("text message sent")

def textAdmin(msg):
   client = Client(account_sid, auth_token)
   client.messages.create(
     to="+1",
     from_="+1",
     body = msg)
   print("text message to admin sent")

def slack(msg):
   os.system("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"%s\"}' https://hooks.slack.com/services/webhook link ending" % msg)
   print('sent slack notification')

def getWFSlot(productUrl):
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
   }

   driver = webdriver.Chrome('/usr/local/bin/chromedriver')
   driver.get(productUrl)
   html = driver.page_source
   soup = bs4.BeautifulSoup(html)
   #slack("Starting search for %s" % (search_area))
   textAdmin("Starting Amazon Fresh delivery slot search for %s" % (search_area))
   #text("Starting Amazon Fresh delivery slot search for %s" % (search_area))
   time.sleep(60)
   no_open_slots = True
   refreshcount = 0

   while no_open_slots:
      driver.refresh()
      refreshcount+= 1
      print("refreshed (%s/720)" % refreshcount)
      if refreshcount > 700:
         print ('2 hour timeout - refreshing cart and checkout page')
         #textAdmin("Delivery search stopped - 2 hour timeout")
         driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
         time.sleep(3)
         driver.find_element_by_xpath("//input[@value='Proceed to checkout']").click();
         time.sleep(3)
         driver.find_element_by_link_text("Continue").click();
         time.sleep(3)
         refreshcount = 0
      html = driver.page_source
      soup = bs4.BeautifulSoup(html)
      time.sleep(10)

      #no_open_slots = "No doorstep delivery windows are available for"
      no_open_slots_text = "No delivery windows available. New windows are released throughout the day."
      try:
         no_slots_from_web = driver.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/h4[1]').text
         if no_open_slots_text in no_slots_from_web:
            pass
         else:
            print('SLOTS OPEN!')
            os.system('say "Slots for delivery opened!"')
            #slack("Delivery slots are open for %s" % (search_area))
            #text("Delivery slots are open for %s" % (search_area))
            textAdmin("Delivery slots are open for %s" % (search_area))
            no_open_slots = False
            time.sleep(60)
      except NoSuchElementException:
         if driver.current_url == productUrl:
            print('SLOTS OPEN! by exception')
            print('exception slot')
            os.system('say "Slots for delivery opened!"')
            #slack("Delivery slots are open for %s" % (search_area))
            #text("Delivery slots are open for %s" % (search_area))
            textAdmin("Delivery slots are open for %s" % (search_area))
            no_open_slots = False
            time.sleep(60)
         else:
            print('Exception and current_url isnt matching producturl')
            driver.get(productUrl)

      try:
         open_slots = soup.find('div', class_ ='orderSlotExists').text()
         if open_slots != "false":
            print('SLOTS OPEN! (soup.find)')
            os.system('say "Slots for delivery opened!"')
            #slack("Delivery slots are open for %s" % (search_area))
            #text("Delivery slots are open for %s" % (search_area))
            textAdmin("Delivery slots are open for %s" % (search_area))
            no_open_slots = False
            time.sleep(60)
      except AttributeError:
         pass

      

      


getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')


