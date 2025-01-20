from django.shortcuts import render
from django.http import JsonResponse
import json
from .scraper_tool import scrape_data
from selenium.webdriver.common.by import By

def dashboard(request):
    products = scrape_data()  # Print the data type(data))
    # for product in products:
    #     name = product.find_element(By.XPATH, './/h3').text
    #     print(f'name : ', name)
    #     price = product.find_element(By.XPATH, ".//span").text
    #     print(f'price : ', price)
    #     img = product.find_element(By.XPATH, ".//img").get_attribute("src")
    #     print(f'img : ', img)
    #     link = product.find_element(By.XPATH, ".//a").get_attribute("href")
    #     print(f'link : ', link)
    return render(request, 'dashboard.html',{'products': products})
    # return JsonResponse(data, safe=False)