import bs4

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import sys
import time
import os

def slack(msg):
   os.system("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"%s\"}' https://hooks.slack.com/services/<webhook url ending>" % msg)
   print('sent slack notification')

def getWFSlot(productUrl):
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
   }

   driver = webdriver.Chrome('/usr/local/bin/chromedriver')
   driver.get(productUrl)           
   html = driver.page_source
   soup = bs4.BeautifulSoup(html)
   slack("Starting search for <insert area here>")
   time.sleep(60)
   no_open_slots = True

   while no_open_slots:
      driver.refresh()
      print("refreshed")
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
            slack("Delivery slots are open")
            no_open_slots = False
            time.sleep(1400)
      except NoSuchElementException:
         print('SLOTS OPEN!')
         os.system('say "Slots for delivery opened!"')
         slack("Delivery slots are open")
         no_open_slots = False
         time.sleep(1400)


      try:
         open_slots = soup.find('div', class_ ='orderSlotExists').text()
         if open_slots != "false":
            print('SLOTS OPEN!')
            os.system('say "Slots for delivery opened!"')
            slack("Delivery slots are open")
            no_open_slots = False
            time.sleep(1400)
      except AttributeError:
         pass

      

      


getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')


