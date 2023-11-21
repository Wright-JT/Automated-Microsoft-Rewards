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

mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1"
date = datetime.date.today()
pointsCheck1 = 0
pointsCheck2 = 0
error_detected_max = 5 #Amount of times the program will restart if the program crashes.

desktop_searches = 0 #34 Searches = 170 Points
mobile_searches = 0 #20 Searches = 100 Points
desktop_searches = 0 #34 Searches = 170 Points
mobile_searches = 0 #20 Searches = 100 Points

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

def auto_search(SearchType):
def auto_search(SearchType):
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
    driver.get('https://www.bing.com')
    while True:
        try: 
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_rc")))
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
    try: 
        driver.find_element(By.CLASS_NAME, "wk_choicesInstLink")
    try: 
        driver.find_element(By.CLASS_NAME, "wk_choicesInstLink")
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
    except:
    except:
        pass

def popup_quiz():
    try:
        timeout = 0
        driver.find_element(By.ID,'rqStartQuiz').click()
        time.sleep(5)
        span_element = driver.find_element(By.CLASS_NAME,"rqMCredits")
        total_questions = int(span_element.text) // 10
        while total_questions != 0 or timeout == 10:
            try:
                print(f'Total questions: {total_questions}')
                correctAnswer = driver.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
                for AnswerNum in range(4):
                    option_value = driver.find_element(By.ID, f"rqAnswerOption{AnswerNum}").get_attribute("data-option")
                    if option_value == correctAnswer:
                        driver.find_element(By.ID, f"rqAnswerOption{AnswerNum}").click()
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
        driver.find_element(By. ID,"btoption" + str(random.randint(0, 1))).click()
        time.sleep(5)
    except:
    except:
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

def credentials():
    Credentials = 'Credentials.txt'
    if os.path.exists(Credentials):
        with open(Credentials, 'r') as file:
            UserPass = file.read()

            EmailStart = UserPass.find('Username: "') + len('Username: "')
            EmailEnd = UserPass.find('"', EmailStart)
            Email = UserPass[EmailStart:EmailEnd]

            PasswordStart = UserPass.find('Password: "') + len('Password: "')
            PasswordEnd = UserPass.find('"', PasswordStart)
            Password = UserPass[PasswordStart:PasswordEnd]

        if (Email == 'YOUR EMAIL HERE') and (Password == 'YOUR PASSWORD HERE'):
            print('Please add a username and password to the credentials text document.')
            time.sleep(10)
            driver.quit()
            sys.exit()
        else:
            sign_in(Email, Password)

    else:
        with open(Credentials, 'w') as file:
            file.write('Do not change or modify anything that is not in quotes.\n\nUsername: "YOUR EMAIL HERE" \nPassword: "YOUR PASSWORD HERE"')
            print('Please add a username and password to the credentials text document.')
        time.sleep(10)
        driver.quit()
        sys.exit()

def sign_in(Username, Password):
    driver.get('https://tinyurl.com/ydfke3nt') 
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "i0116")))
            driver.find_element('id', 'i0116').send_keys(Username)
            driver.find_element('id', 'idSIButton9').click()
            break
        except:
            time.sleep(2)

    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "i0118")))
            driver.find_element('id', 'i0118').send_keys(Password)
            driver.find_element('id', 'idSIButton9').click()
            break
        except:
            time.sleep(2)

def find_all_dailies():
    try:
        driver.get('https://rewards.bing.com/')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.mee-icon.mee-icon-AddMedium')))
        icon_elements = driver.find_elements(By.CSS_SELECTOR, 'span.mee-icon.mee-icon-AddMedium')
        for icon_element in icon_elements:
            icon_element.find_element(By.XPATH, './ancestor::a[contains(@class, "ds-card-sec")]').click()
            driver.switch_to.window(driver.window_handles[1])
            try:
                time.sleep(3)
                browser_quiz()
                popup_quiz()
                daily_poll()
            except:
                pass
            time.sleep(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        print(f'Error {e}')

def power_off():
    driver.quit()
    ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
    sys.exit()
      
if __name__ == "__main__":
    driver = initialize_driver()
    while True:
        internet_check() 
        while True:
            try:
                if driver is None:
                    driver = initialize_driver()
                driver.maximize_window()
                credentials()
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
            else:
                break
        break
    print('AutoBing successful.')
    time.sleep(5)
    power_off()