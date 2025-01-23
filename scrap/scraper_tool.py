from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import traceback
import csv
import os
import re

def scrape_fb_data():
    url = 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BD&is_targeted_country=false&media_type=all&q=Hoodie&search_type=keyword_unordered'

    # Set up Selenium WebDriver
    options = Options()
    options.headless = False  # Run in headless mode
    service = Service('/usr/local/bin/chromedriver')  # Path to your WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open the URL
    driver.get(url)

    products_path = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]/div'
    products_type_path = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/input'
    load_more_button_xpath = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[5]/div[2]/a'
    # making a directory to save the file with the column name
    media_dir = 'media'
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    filename = 'fb_file.csv'
    file_path = os.path.join(media_dir, filename)
    
    filecsv = open(file_path, 'w', encoding='utf8')
    csv_columns = ['ID', 'Company_Name', ]
    writer = csv.DictWriter(filecsv, fieldnames = csv_columns)
    writer.writeheader()
    
    export_data = {}
    # Wait for the page to load and the elements to be present
    try:
        # finding the products type part
        products_type = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, products_type_path)))
        products_type = products_type[0].get_attribute('value')
        print(f'products_type : ', products_type)
        export_data['products_type'] = products_type
        
        previous_product_count = 0
        while True:
            # finding all the products part
            products = WebDriverWait(driver, 30).until(
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
                    id_element = product.find_element(By.CLASS_NAME, "x8t9es0.xw23nyj.xo1l8bm.x63nzvj.x108nfp6.xq9mrsl.x1h4wwuj.xeuugli")
                    name_element = product.find_element(By.CLASS_NAME, "x8t9es0.x1fvot60.xxio538.x108nfp6.xq9mrsl.x1h4wwuj.x117nqv4.xeuugli")
                    
                    if id_element:
                        id_text = id_element.text.strip()
                        match = re.search(r'Library ID:\s*(\d+)', id_text)
                        id = match.group(1) if match else None
                    else:
                        id = None
                    
                    name = name_element.text if name_element else None
                    writer.writerow({'ID': id, 'Company_Name': name})
                except Exception as inner_e:
                    print(f"Error processing product: {inner_e}")
                    # print(product.text)
            # Try clicking the "Load More" button
            try:
                load_more_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, '_8n_3'))
                    # EC.element_to_be_clickable((By.LINK_TEXT, 'See more'))
                )
                print(f'type of button is : ', type(load_more_button))
                print(load_more_button.text)
                load_more_button.get_property('href') 
                load_more_button.click()  # Click the button
                print("Clicked the 'See more' button. Waiting for new content...")
                
                
                # Wait for new content to load by comparing product count
                WebDriverWait(driver, 10).until(
                    lambda driver: len(driver.find_elements(By.XPATH, products_path)) > previous_product_count
                )
            except Exception as e:
                print("No 'See more' button found or an error occurred. Exiting...")
                break  

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        products = []
    
    # Close the WebDriver
    driver.quit()
    
    # export_data.append(products_type)
    
    return export_data

def scrape_data():
    # url = 'https://www.amazon.com/?gclid=Cj0KCQiAhbi8BhDIARIsAJLOluevUVNI_RYrqx9K_jgJnNCBFNnc8ILAMKNQCu-QRNJGeNJ_7_shspUaAlc-EALw_wcB'
    # url = 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BD&is_targeted_country=false&media_type=all&q=Hoodie&search_type=keyword_unordered'
    url = 'https://www.scrapingcourse.com/ecommerce/'
    
    # Set up Selenium WebDriver
    options = Options()
    options.headless = True  # Run in headless mode
    service = Service('/usr/local/bin/chromedriver')  # Path to your WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    
    
    # Open the URL
    driver.get(url)
    print('URL is opened')
    # print(driver.page_source)
    
    # //*[@id="product-list"]/li
    # path = '//*[@id="mount_0_0_rQ"]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]/div'
    # path = '//*[@id="mount_0_0_zg"]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]/div[1]'
    # path = '//*[@id="gw-card-layout"]'
    # path = '//*[@id="js_16a"]/a/span'
    path = '//*[@id="main"]/ul/li'
    # Wait for the page to load and the elements to be present
    media_dir = 'media'
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    filename = 'file.csv'
    
    file_path = os.path.join(media_dir, filename)
    
    filecsv = open(file_path, 'w', encoding='utf8')
    csv_columns = ['name', 'price', 'img', 'link']
    writer = csv.DictWriter(filecsv, fieldnames = csv_columns)
    writer.writeheader()
    
    try:
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, path)))

        print(f'Length of products is : {len(products)}')
        print(f'type of products is : {type(products)}')
        for product in products:
            name = product.find_element(By.XPATH, ".//h2").text
            price = product.find_element(By.XPATH, ".//span").text
            img = product.find_element(By.XPATH, ".//img").get_attribute("src")
            link = product.find_element(By.XPATH, ".//a").get_attribute("href")
            writer.writerow({'name': name, 'price': price, 'img': img, 'link': link})
            # print(f'name : {name}, price : {price}, img : {img}, link : {link}')

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        products = []
    
    # Close the WebDriver
    driver.quit()
    
    return products



# from bs4 import BeautifulSoup
# import requests

# def scrape_data():
#     url = 'https://www.scrapingcourse.com/ecommerce/'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'lxml')

#     products = soup.find_all(class_="x8t9es0 x1fvot60 xxio538 x108nfp6 xq9mrsl x1h4wwuj x117nqv4 xeuugli")

#     print(len(products))
#     return products
