from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import time
import os

driver = webdriver.Chrome()
URL = 'https://pixabay.com/ko/images/search/fruit%20apple/'
driver.get(URL)
div = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[4]/div[3]/div')
text = div.text
page_num, total_pages = text.split('/')
total_pages = total_pages.strip()
print("전체 페이지 수 : " + total_pages)