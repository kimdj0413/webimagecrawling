from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv
from tqdm import tqdm

driver1 = webdriver.Chrome()
URL = "https://www.mk.co.kr/search?word=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&dateType=direct&startDate=2023-06-11&endDate=2024-05-22"
driver1.get(URL)
wait = WebDriverWait(driver1, 10)

# driver2 = webdriver.Chrome()
# URL = "https://finance.naver.com/item/sise.naver?code=016360"
# driver2.get(URL)
# wait = WebDriverWait(driver2, 10)

def dateChanger(date):
    cleaned_string = date.strip()
    date_part, year_part = cleaned_string.split('\n')
    month, day = date_part.split('.')
    formatted_date = f"{year_part}{month}{day}"
    return formatted_date

for i in tqdm(range(0,1)):#315
    wait = WebDriverWait(driver1, 10)
    driver1.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
    load_more_button = wait.until(EC.presence_of_element_located((By.ID, 'api_243')))
    driver1.execute_script("arguments[0].click();", load_more_button)
    time.sleep(2)

page_source = driver1.page_source.encode('UTF-8')
soup1 = BeautifulSoup(driver1.page_source, 'html.parser')
news_list = []
title_elements = soup1.find_all(class_='news_ttl')
time_elements = soup1.find_all(class_='time_area')
for time_element, title_element in zip(time_elements, title_elements):
    date = time_element.get_text()
    date = dateChanger(date)
    news_list.append([date,title_element.get_text()])
# news_titles = [element.get_text() for element in title_elements]
# print(news_titles)
# print(news_list)
print(len(news_list))
csv_filename = 'news_list1.csv'
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(news_list)

print(f"CSV 파일 '{csv_filename}'이(가) 생성되었습니다.")