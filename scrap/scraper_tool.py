from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import traceback

def scrape_data():
    # url = 'https://www.amazon.com/?gclid=Cj0KCQiAhbi8BhDIARIsAJLOluevUVNI_RYrqx9K_jgJnNCBFNnc8ILAMKNQCu-QRNJGeNJ_7_shspUaAlc-EALw_wcB'
    url = 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BD&is_targeted_country=false&media_type=all&q=Hoodie&search_type=keyword_unordered'
    # url = 'https://www.scrapingcourse.com/ecommerce/'
    
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
    path = '//*[@id="mount_0_0_rQ"]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]/div'
    # path = '//*[@id="mount_0_0_zg"]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]/div[1]'
    # path = '//*[@id="gw-card-layout"]'
    # path = '//*[@id="js_16a"]/a/span'
    # Wait for the page to load and the elements to be present
    try:
        products = WebDriverWait(driver, 300).until(
            EC.presence_of_all_elements_located((By.XPATH, path)))

        print(f'Length of products is : {len(products)}')
        print(f'type of products is : {type(products)}')
        for product in products:
            print(product.text)
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
