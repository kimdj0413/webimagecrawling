from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import time
import os

# options = Options()
# options.add_argument('headless')
# options.add_argument('disable-gpu')
driver = webdriver.Chrome()


def scroll_down():
    cnt=0
    while True:
        time.sleep(3)
        # 페이지 맨 아래로 스크롤
        driver.find_element(By.XPATH, '//body').send_keys(Keys.END)
        time.sleep(3)
        cnt+=1
        try:
            # '더보기' 버튼이 보이면 클릭
            load_more_button = driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
            if load_more_button.is_displayed():
                load_more_button.click()
        except:
            pass
        time.sleep(3)
        try:
            # 종료
            if cnt<image_cnt<60:
                break
            if cnt == image_cnt//60:
                break
        except:
            pass

if __name__ == "__main__":
    query = input("검색어 : ") 
    if " " in query:
        name_query = query.split(' ')[1]
    else :
        name_query = query
    image_cnt = int(input("수집할 이미지 개수 : ")) 

    save_dir = name_query # 저장할 디렉토리 이름
    os.makedirs(save_dir, exist_ok=True)  # 디렉토리 생성 (이미 존재하면 무시)
    os.chdir(save_dir)  # 작업 디렉토리 변경

    driver = webdriver.Chrome()  # Chrome 웹 드라이버 실행
    URL = 'https://www.google.com/search?tbm=isch&q='
    driver.get(URL + query)  # 검색어를 포함한 URL로 이동

    scroll_down()  # 페이지 스크롤 함수 호출

    # 이미지 정보 추출
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    image_info_list=[]
    for img in soup.find_all('img'):
    # 클래스 속성을 가져옵니다.
        class_attr = img.get('class')
        
        # 클래스 속성이 정확히 ['YQ4gaf']인 경우에만 리스트에 추가합니다.
        if class_attr == ['YQ4gaf']:
            image_info_list.append(img)
    
    image_and_name_list = []

    print('=== 이미지 수집 시작 ===')

    downlaod_cnt = 0
    for i in range(len(image_info_list)):
        if i == image_cnt:
            break
        if 'src' in image_info_list[i].attrs:
            save_image = image_info_list[i]['src']

            image_path = os.path.join(name_query.replace(' ', '_') + '__' + str(downlaod_cnt) + '.jpg')
            image_and_name_list.append((save_image, image_path))
            downlaod_cnt += 1

    # 이미지 다운로드
    for i in range(len(image_and_name_list)):
        try:
            urllib.request.urlretrieve(image_and_name_list[i][0], image_and_name_list[i][1])
        except ValueError:
            continue

    print('=== 이미지 수집 종료 ===')
    driver.close()  # 브라우저 닫기