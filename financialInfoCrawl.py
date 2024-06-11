from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv
from tqdm import tqdm

driver = webdriver.Chrome()
URL = "https://finance.naver.com/item/sise.naver?code=016360"
driver.get(URL)
wait = WebDriverWait(driver, 10)

soup = BeautifulSoup(driver.page_source, 'html.parser')
financial_list = []
time_elements = soup.find_all(class_='tah p10 gray03')
