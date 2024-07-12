from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import csv
from tqdm import tqdm
import re
import pandas as pd

basicURL = "https://finance.naver.com/"
URL = "https://finance.naver.com/sise/sise_market_sum.naver?&page="

options = Options()
options.add_argument('headless')
options.add_argument('disable-gpu')
codeList = []
volList = []
nameList = []
for i in tqdm(range(1,46)):
  driver = webdriver.Chrome(options=options) # options
  driver.get(URL+str(i))
  wait = WebDriverWait(driver, 10)
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  titles = soup.find_all(class_='tltle')
  links = [tag['href'] for tag in titles]
  for link in links:
    time.sleep(1)
    driver = webdriver.Chrome(options=options)
    driver.get(basicURL + link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    #   주식 코드
    code = soup.find(class_='code')
    code = code.get_text()
    codeList.append(code)
    
    #   상장 주식 수
    volSum = soup.find('th', text='상장주식수').find_next_sibling('td').find('em')
    text = volSum.get_text()
    text = re.findall(r'\d+', text)
    volText = ''.join(text)
    volList.append(volText)
    
    #   주식 이름
    name = soup.find(class_='wrap_company')
    companyName = name.find('h2').find('a').get_text()
    nameList.append(companyName)
    
    
  print(nameList[-3:])
  print(codeList[-3:])
  print(volList[-3:])
  print(len(nameList), len(codeList), len(nameList))
  
  df = pd.DataFrame({
      'Name': nameList,
      'Code': codeList,
      'Volume': volList
  })

  df.to_csv('FinanceList.csv', index=False)
driver.quit()