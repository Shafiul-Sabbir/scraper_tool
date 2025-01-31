from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from .login_cookies import load_cookies, save_cookies, login_and_save_cookies
import traceback
import csv
import os
import re
import pickle

# Making a directory to save the file with the column name
media_dir = 'media'
if not os.path.exists(media_dir):
    os.makedirs(media_dir)
filename = 'login_cookies.pkl'
filepath = os.path.join(media_dir, filename)

def scrape_fb_data():
    url = 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BD&is_targeted_country=false&media_type=all&q=Shirt&search_type=keyword_unordered'

    # Set up Selenium WebDriver
    options = Options()
    options.headless = False  # Run without headless mode for debugging
    # for windows
    service = Service('C:/Windows/chromedriver.exe')
    # for macos
    # service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open the URL
    driver.get(url)
    
    username = '01881652629'
    password = '835137'
    
    login_and_save_cookies(username, password)

    products_path = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]/div'
    products_type_path = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/input'
    load_more_button_xpath = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[5]/div[2]/a'
    
    # Making a directory to save the file with the column name
    media_dir = 'media'
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    filename = 'fb_file.csv'
    file_path = os.path.join(media_dir, filename)
    
    filecsv = open(file_path, 'w', encoding='utf8')
    csv_columns = ['Number', 'ID', 'Company_Name']
    writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
    writer.writeheader()
    
    export_data = {}
    # Wait for the page to load and the elements to be present
    try:
        # Finding the products type part
        products_type = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, products_type_path)))
        products_type = products_type[0].get_attribute('value')
        print(f'products_type : ', products_type)
        export_data['products_type'] = products_type
        
        previous_product_count = 0
        number = 0
        while True:
            # Finding all the products part
            products = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, products_path)))

            print(f'Length of products is : {len(products)}')
            print(f'type of products is : {type(products)}')
            
            # Check if new data has been loaded
            if len(products) == previous_product_count:
                print("No new products found. Exiting...")
                break

            previous_product_count = len(products)
            
            for product in products:
                try:
                    number += 1
                    id_element = product.find_element(By.CLASS_NAME, "x8t9es0.xw23nyj.xo1l8bm.x63nzvj.x108nfp6.xq9mrsl.x1h4wwuj.xeuugli")
                    name_element = product.find_element(By.CLASS_NAME, "x8t9es0.x1fvot60.xxio538.x108nfp6.xq9mrsl.x1h4wwuj.x117nqv4.xeuugli")
                    
                    if id_element:
                        id_text = id_element.text.strip()
                        match = re.search(r'Library ID:\s*(\d+)', id_text)
                        id = match.group(1) if match else None
                    else:
                        id = None
                    
                    name = name_element.text if name_element else None
                    writer.writerow({'Number': number, 'ID': id, 'Company_Name': name})
                except Exception as inner_e:
                    print(f"Error processing product: {inner_e}")
            
            # Try clicking the "Load More" button
            try:
                load_more_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, '_8n_3'))
                )
                
                # Get the href attribute
                href_value = load_more_button.get_attribute('href')
                # print(f"href attribute value: {href_value}")
                
                # Check if the href value is "#"
                if href_value == "#":
                    print("The href attribute is set to '#'")
                
                # Scroll the element into view
                driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                
                # Click the "Load More" button using Actions class
                actions = ActionChains(driver)
                actions.move_to_element(load_more_button).click().perform()
                print("Clicked the 'See more' button. Waiting for new content...")
                
                # Wait for new content to load by comparing product count
                WebDriverWait(driver, 20).until(
                    lambda driver: len(driver.find_elements(By.XPATH, products_path)) > previous_product_count
                )
            except StaleElementReferenceException as e:
                print(f"Stale element reference: {e}")
                # Re-find the load more button and try again
                try:
                    load_more_button = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, '_8n_3'))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                    actions = ActionChains(driver)
                    actions.move_to_element(load_more_button).click().perform()
                    print("Clicked the 'See more' button after re-finding it. Waiting for new content...")
                    
                    # Wait for new content to load by comparing product count
                    WebDriverWait(driver, 20).until(
                        lambda driver: len(driver.find_elements(By.XPATH, products_path)) > previous_product_count
                    )
                except Exception as e:
                    print(f"An error occurred after re-finding the 'See more' button: {e}")
                    break
            except Exception as e:
                print("No 'See more' button found or an error occurred. Exiting... ", e)
                break
        
        export_data['total_products'] = number
        
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        products = []
    
    # Close the WebDriver
    driver.quit()
    
    return export_data

