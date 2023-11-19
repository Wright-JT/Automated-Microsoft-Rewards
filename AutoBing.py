from selenium import webdriver
from faker import Faker
from ping3 import ping
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import ctypes
import os
import datetime
import random
import time
import sys

#TODO: Fix when and where print statements happen, such as poll started and poll finished.

mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1"
date = datetime.date.today()
pointsCheck1 = 0
pointsCheck2 = 0
error_detected_max = 5 #Amount of times the program will restart if the program crashes.

desktop_searches = 1 #34 Searches = 170 Points
mobile_searches = 1 #20 Searches = 100 Points

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
        time.sleep(random.randint(3,4))
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

def point_counter(BeforeOrAfter): #Checks how many points were made before and after script
    driver.get('https://www.bing.com')
    driver.refresh()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_rc")))
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
            time.sleep(10)

def browser_quiz():
    if driver.find_element(By.CLASS_NAME, "wk_choicesInstLink"): #Finding quiz type
        timeout = 0
        while timeout < 10: 
            try:
                driver.find_element(By.XPATH, '//img[contains(@alt, "Checkmark Image")]')
                break
            except:
                while True:
                    driver.find_element(By.CLASS_NAME, "wk_choicesInstLink").click()
                    time.sleep(3)
                    driver.find_element(By.XPATH,'//input[@type="submit" and @name="submit"]').click()
                    time.sleep(8)
                    break
    else:
        pass

def popup_quiz():
    try:
        driver.find_element(By.ID,'rqStartQuiz') #Finding the type of quiz
        timeout = 0
        driver.find_element(By.ID,'rqStartQuiz').click()
        time.sleep(5)
        span_element = driver.find_element(By.CLASS_NAME,"rqMCredits")
        total_questions = int(span_element.text) // 10
        while total_questions != 0 or timeout == 10:
            try:
                print(f'Total questions: {total_questions}')
                correctAnswer = driver.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
                if driver.find_element(By.ID,"rqAnswerOption0").get_attribute("data-option") == correctAnswer:
                    driver.find_element(By.ID,"rqAnswerOption0").click()
                elif driver.find_element(By.ID,"rqAnswerOption1").get_attribute("data-option") == correctAnswer:
                    driver.find_element(By.ID,"rqAnswerOption1").click()
                elif driver.find_element(By.ID,"rqAnswerOption2").get_attribute("data-option") == correctAnswer:
                    driver.find_element(By.ID,"rqAnswerOption2").click()
                elif driver.find_element(By.ID,"rqAnswerOption3").get_attribute("data-option") == correctAnswer:
                    driver.find_element(By.ID,"rqAnswerOption3").click()    
                else:
                    break
                total_questions = total_questions - 1
                time.sleep(5)
            except NoSuchElementException:
                timeout = timeout + 1
                print(f'Quiz Error: {timeout} timeouts.')
                time.sleep(2)
    except:
        pass

def daily_poll():
    try:
        time.sleep(5)
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btoption")))
        driver.find_element(By. ID,"btoption" + str(random.randint(0, 1))).click()
        print('Poll started')
        time.sleep(5)
    except Exception as e:
        pass

def switch_window():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def log_points(pointsCheck1, pointsCheck2): #Logs made points into text document
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

def sign_in():
    driver.get('https://tinyurl.com/ydfke3nt') 
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "i0116")))
            driver.find_element('id', 'i0116').send_keys(Credentials['Username'])
            driver.find_element('id', 'idSIButton9').click()
            break
        except:
            pass
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "i0118")))
            driver.find_element('id', 'i0118').send_keys(Credentials['Password'])
            driver.find_element('id', 'idSIButton9').click()
            break
        except:
            pass

def dailies():
    driver.get('https://rewards.bing.com/?ref=rewardspanel') 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="daily-sets"]//mee-card-group[1]/div/mee-card')))
    dailies_list = driver.find_elements(By.XPATH, '//*[@id="daily-sets"]//mee-card-group[1]/div/mee-card') 
    DailyCardNum = 0
    for daily in dailies_list:
        DailyCardNum = DailyCardNum + 1
        time.sleep(5)
        while True:
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='daily-sets']//mee-card-group[1]/div/mee-card"))).click()
                driver.switch_to.window(driver.window_handles[1])
                break
            except Exception as e:
                time.sleep(3)
                print(f'Error: {e}')
                pass
        if DailyCardNum == 1: #CLICK
            print('Daily started')
            print(DailyCardNum)
            time.sleep(5)
            switch_window()
            print('Daily passed')
        if DailyCardNum == 2: #QUIZ
            print('Quiz started')
            time.sleep(3)
            print(DailyCardNum)
            if driver.find_element(By.XPATH, '//img[contains(@alt, "Checkmark Image")]'):
                time.sleep(3)
            else:
                try:
                    browser_quiz() 
                    popup_quiz()
                except:
                    pass
            switch_window()
            print('Quiz passed')
        if DailyCardNum == 3: #POLL
            print('Poll started')
            daily_poll()
            switch_window()
            print('Poll passed')

def find_all_dailies():
    try:
        driver.get('https://rewards.bing.com/')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.mee-icon.mee-icon-AddMedium')))
        icon_elements = driver.find_elements(By.CSS_SELECTOR, 'span.mee-icon.mee-icon-AddMedium')
        for icon_element in icon_elements:
            icon_element.find_element(By.XPATH, './ancestor::a[contains(@class, "ds-card-sec")]').click()
            driver.switch_to.window(driver.window_handles[1])
            try:
                #browser_quiz()
                #popup_quiz()
                daily_poll()
            except:
                pass
            time.sleep(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        print(f'Error {e}')

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
                sign_in()
                pointsCheck1 = point_counter(pointsCheck1)
                auto_search(desktop_searches)
                mobile_swap(driver, 'mobile')
                auto_search(mobile_searches)
                mobile_swap(driver, 'desktop')
                find_all_dailies()
                pointsCheck2 = point_counter(pointsCheck1)
                log_points(pointsCheck1, pointsCheck2)
            except Exception:               
                error_detected_max = error_detected_max - 1
                driver = None   
                total_errors(error_detected_max)
                pass
            else:
                break
        break
    print('AutoBing successful.')
    time.sleep(5)
    #power_off()
    