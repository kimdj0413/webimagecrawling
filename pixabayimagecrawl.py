from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import time
import os
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36
query = input("검색어 : ") 
if " " in query:
    name_query = query.split(' ')[1]
else :
    name_query = query

save_dir = name_query
os.makedirs(save_dir, exist_ok=True)
os.chdir(save_dir) 

options=Options()
user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
options.add_argument(user_agent)
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
URL = 'https://pixabay.com/ko/images/search/'
driver.get(URL+query)

div = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[4]/div[3]/div')
text = div.text
page_num, total_pages = text.split('/')
total_pages = total_pages.strip()
next_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[4]/div[2]/a')
name_cnt=0

for i in range(0,int(total_pages)):
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    image_info_list=[]
    image_and_name_list = []
    for img in soup.find_all('img'):
        class_attr = img.get('src')
        if class_attr.startswith('https://'):
            image_info_list.append(class_attr)
            image_and_name_list.append(str(name_cnt))
            name_cnt+=1
    for i in range(len(image_and_name_list)):
        urllib.request.urlretrieve(image_info_list[i], image_and_name_list[i]+'.jpg')
        time.sleep(0.3)
    next_button.click()

driver.close()