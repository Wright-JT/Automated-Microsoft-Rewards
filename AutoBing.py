from selenium import webdriver
from faker import Faker
from ping3 import ping
import ctypes
import os
import datetime
import random
import time
import sys

mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1"
date = datetime.date.today()
pointsCheck1 = 0
pointsCheck2 = 0
error_detected_max = 5 #Amount of times the program will restart if the program crashes.

desktop_searches = 2 #34 Searches = 170 Points
mobile_searches = 2 #20 Searches = 100 Points

Credentials = {
'Username': 'YOUR EMAIL',
'Password': 'YOUR PASSWORD' }

def initialize_driver():
    try:
        driver = webdriver.Edge()
        return driver
    except Exception:
        print('Failed to initialize the driver.')
        return None

def total_errors(errors_detected):
    if errors_detected == 0:
        print('Colossal failure.')
        time.sleep(5)
        sys.exit()
    else:       
        print(f'Error detected, restarting in 10 seconds... ({errors_detected} restarts remaining.)')
        time.sleep(10)

def auto_search(SearchType): #Searches with random fake names.
    while SearchType > 0:
        fake = Faker()
        search = fake.name()
        driver.get(f'https://www.bing.com/search?q={search}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={search}&sc=11-4&sk=&cvid=B71527E3F16E44EC859237C4FC049012&ghsh=0&ghacc=0&ghpl=')
        time.sleep(random.randint(7,10))
        SearchType = SearchType - 1

def mobile_swap(driver, x):
    while True:
        try:
            if x == 'mobile':
                driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                    "userAgent": mobile_user_agent, })
            if x == 'desktop':
                driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                    "userAgent": '', })
            driver.refresh()
            break
        except:
            time.sleep(5)

def internet_check():
    try:
        return ping("8.8.8.8", timeout=2) is not None
    except Exception:
        print('No internet detected. Trying again in 10 minutes.')
        time.sleep(600)

def point_counter(BeforeOrAfter):
    while True:
        try: 
            pointsCheckerData = driver.find_element('id', "id_rc")
            pointsChecked = int(pointsCheckerData.text)
            if BeforeOrAfter == 0:
                print(f'Current points before search: {pointsChecked}')
            else:
                print(f'Current points after search: {pointsChecked}')
            return pointsChecked
        except:
            driver.refresh()
            time.sleep(5)

def log_points(pointsCheck1, pointsCheck2):
    pointsLog = 'PointsLog.txt'
    newLine = (str(f'{pointsCheck2-pointsCheck1} points generated on {date}, {pointsCheck2} total.\n'))
    if os.path.exists(pointsLog):
        with open(pointsLog, 'r') as file:
            oldLines = file.read()
        with open(pointsLog, 'w') as file:
            file.write(newLine + oldLines)
    else:
        with open(pointsLog, 'w') as file:
            file.write(newLine)

def sign_in(Username, Password):
    driver.get('https://tinyurl.com/ydfke3nt') 
    while True:
        try:
            driver.find_element('id', 'i0116').send_keys(Username)
            driver.find_element('id', 'idSIButton9').click()
            break
        except:
            time.sleep(2)
    while True:
        try:
            driver.find_element('id', 'i0118').send_keys(Password)
            driver.find_element('id', 'idSIButton9').click()
            break
        except:
            time.sleep(2)

def power_off():
    while True:
        try:
            driver.quit()
            ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
            sys.exit()
        except:
            ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
            sys.exit(1)

if __name__ == "__main__":
    driver = initialize_driver()
    while True:
        internet_check() 
        while True:
            try:
                if driver is None:
                    driver = initialize_driver()
                driver.maximize_window()
                sign_in(Credentials['Username'], Credentials['Password'])
                driver.get('https://www.bing.com')
                driver.refresh()
                time.sleep(5)
                pointsCheck1 = point_counter(pointsCheck1)
                auto_search(desktop_searches)
                mobile_swap(driver, 'mobile')
                auto_search(mobile_searches)
                mobile_swap(driver, 'desktop')
                pointsCheck2 = point_counter(pointsCheck1)
                log_points(pointsCheck1, pointsCheck2)
            except Exception:               
                error_detected_max = error_detected_max - 1
                driver = None   
                total_errors(error_detected_max)
            else:
                break
        break
    print('AutoBing successful.')
    time.sleep(10)
    power_off()
    