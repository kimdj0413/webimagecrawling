from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import csv
from tqdm import tqdm

# driver2 = webdriver.Chrome()
# URL = "https://finance.naver.com/item/sise.naver?code=016360"
# driver2.get(URL)
# wait = WebDriverWait(driver2, 10)

query_date = "20110706"

def remove_unicode_characters(text):
    return text.encode('cp949', 'ignore').decode('cp949')

def dateChanger(date):
    cleaned_string = date.strip()
    date_part, year_part = cleaned_string.split('\n')
    month, day = date_part.split('.')
    formatted_date = f"{year_part}{month}{day}"
    return formatted_date

while(True):
    year = query_date[:4]
    month = query_date[4:6]
    day = query_date[6:]
    formatted_date = f"{year}-{month}-{day}"

    options = Options()
    options.add_argument('headless')
    options.add_argument('disable-gpu')

    driver1 = webdriver.Chrome(options=options)    # options=options
    URL = "https://www.mk.co.kr/search?word=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&dateType=direct&startDate=2004-06-12&endDate="+formatted_date
    driver1.get(URL)
    wait = WebDriverWait(driver1, 10)
    previous_height = driver1.execute_script("return document.body.scrollHeight")

    for i in tqdm(range(0,1000)):#315
        wait = WebDriverWait(driver1, 10)
        driver1.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
        load_more_button = wait.until(EC.presence_of_element_located((By.ID, 'api_243')))
        driver1.execute_script("arguments[0].click();", load_more_button)
        time.sleep(2)
        current_height = driver1.execute_script("return document.body.scrollHeight")
        
        if current_height == previous_height:
            print("화면 구성에 변화가 없습니다. 루프를 종료합니다.")
            break
        
        previous_height = current_height

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
    if(query_date==date):
        break
    query_date = date
    print(date)
    
    cleaned_news_list = [[remove_unicode_characters(item) for item in row] for row in news_list]
    csv_filename = 'news_list.csv'
    with open(csv_filename, mode='a', newline='', encoding='cp949') as file:
        writer = csv.writer(file)
        writer.writerows(cleaned_news_list)

    print(f"CSV 파일 '{csv_filename}'이(가) 생성되었습니다.")
    driver1.quit()