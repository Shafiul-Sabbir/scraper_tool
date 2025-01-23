from django.shortcuts import render
from django.http import JsonResponse
import json
from .scraper_tool import scrape_data, scrape_fb_data
from selenium.webdriver.common.by import By
import os
import csv


def dashboard(request):
    fb_products = scrape_fb_data() 
    make_dir = 'media' 
    fb_filename = 'fb_file.csv' 
    fb_file_path = os.path.join(make_dir, fb_filename)
    
    datas = []
    if os.path.exists(fb_file_path):
        with open(fb_file_path, 'r', encoding='utf-8' ) as filecsv:
            reader = csv.DictReader(filecsv)
            for row in reader:
                datas.append(row) 

    return render(request, 'dashboard.html',{'datas': datas, 'fb_products': fb_products})

    
# def dashboard(request):
#     products = scrape_data() 
#     make_dir = 'media'
#     filename = 'file.csv'   
#     file_path = os.path.join(make_dir, filename)  
    
#     datas = []
#     if os.path.exists(file_path):
#         with open(file_path, 'r', encoding='utf-8' ) as filecsv:
#             reader = csv.DictReader(filecsv)
#             for row in reader:
#                 datas.append(row) 

#     return render(request, 'dashboard.html',{'datas': datas})