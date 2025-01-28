from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pickle
import time
import os


def save_cookies(driver, filepath):
    with open(filepath, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, filepath):
    with open(filepath, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def login_and_save_cookies(username, password):
    url = 'https://www.facebook.com/login'
    options = Options()
    options.headless = False
    # for windows
    service = Service('C:/Windows/chromedriver.exe')
    # for macos
    # service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    
    username_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'pass')
    
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    

    while True:
        try:
            # Check if the CAPTCHA modal is still present
            time.sleep(20)  # Wait for 5 seconds before checking again
            captcha_element = driver.find_element(By.CLASS_NAME, 'xz74otr')  # Adjust the XPath as needed
            # print(f'type of captcha is : ', type(captcha_element))
            # print(f'captcha_element : ', captcha_element)
            if captcha_element:
                print("CAPTCHA is still present, waiting...")   
                break   
        except:
            # CAPTCHA modal is no longer present
            print("CAPTCHA solved. Continuing...")
            break
        
    # Making a directory to save the file with the column name
    media_dir = 'media'
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    filename = 'login_cookies.pkl'
    filepath = os.path.join(media_dir, filename)
    
    save_cookies(driver, filepath)
    print("Logged in successfully. Saved cookies...")
    load_cookies(driver, filepath)
    driver.refresh()
    # driver.quit()

