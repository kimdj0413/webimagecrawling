from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import pandas as pd

##    옵션 사용하면 크롤링이 안됨.
# options = Options()
# options.add_argument('headless')
# options.add_argument('disable-gpu')

start_time = time.time()

driver = webdriver.Chrome() #options=options
URL = "https://m.place.naver.com/restaurant/1820419594/review/visitor"
driver.get(URL)
wait = WebDriverWait(driver, 10)

btn_cnt = 0
while True : 
  try:
    button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "fvwqf")))
    button.click()
    time.sleep(1)
    btn_cnt += 1
    if btn_cnt == 29:   # '더보기' 버튼 누르기 30번으로 제한
      break
  except Exception as e:
    print(f"모든 페이지({btn_cnt}회) 로드 완료", e)
    break

soup = BeautifulSoup(driver.page_source, 'html.parser')

review_list = []
review_elements = soup.find_all(class_='pui__xtsQN-')
for review_element in tqdm(review_elements):
  review_list.append(review_element.get_text())

end_time = time.time()
total_time = end_time - start_time
minutes, seconds = divmod(total_time, 60)

df = pd.DataFrame({
  'review' : review_list
})

df.to_csv('Naver_Review.csv')

print(f'총 크롤링 리뷰 : {len(review_list)}')
print(f"\n총 소요 시간: {int(minutes)}분 {seconds:.2f}초")