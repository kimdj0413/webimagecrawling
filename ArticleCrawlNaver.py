from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import csv
from tqdm import tqdm
import datetime
import re
import pandas as pd

# nowDate = datetime.datetime.now()
financialName = "삼성전자"
startDate = "20240603"
startDate = datetime.datetime.strptime(startDate, "%Y%m%d")

def scroll_down():
    cnt = 0
    previous_height = 0
    print(previous_height)
    while True:
        driver.find_element(By.XPATH, '//body').send_keys(Keys.END)
        time.sleep(1)
        current_height = driver.execute_script("return document.body.scrollHeight")
        cnt += 1
        if previous_height == current_height:
            print(f"{cnt}회 스크롤 완료")
            break
        previous_height = current_height

while True:
    options = Options()
    options.add_argument('headless')
    options.add_argument('disable-gpu')

    driver = webdriver.Chrome(options=options)
    URL = "https://search.naver.com/search.naver?where=news&query="+financialName+"&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds="+startDate.strftime("%Y.%m.%d")+"&de="+startDate.strftime("%Y.%m.%d")+"&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20240624to20240625&is_sug_officeid=0&office_category=0&service_area=0"
    driver.get(URL)
    time.sleep(3)
    scroll_down()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    date = startDate.strftime("%Y.%m.%d")
    day = startDate.weekday()
    mediaElements = soup.find_all(class_='info press')
    titleElements = soup.find_all(class_='news_tit')
    mainElements = soup.find_all(class_='api_txt_lines dsc_txt_wrap')
    newsList=[]

    for mediaElement, titleElement, mainElement in zip(mediaElements, titleElements, mainElements):
        media = mediaElement.get_text()
        media = media.replace("선정","")
        media = media.replace(" ","")
        title = titleElement['title']
        title = re.sub(r'[^\w\s]', '', title)
        main = mainElement.get_text()
        newsList.append([date, day, media, title, main])

    fileName = 'naverNews.csv'
    with open(fileName, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(newsList)
    
    sample = pd.read_csv(fileName)
    crawlLength = len(sample)
    print(f"======================= {date}, {day} 크롤링 완료 =======================")
    print(sample[-3:])
    print(f"총 {crawlLength}건 크롤링")

    startDate = startDate - datetime.timedelta(days=1)
    driver.quit()