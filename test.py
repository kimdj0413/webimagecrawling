import pandas as pd
import re
from konlpy.tag import Okt
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

sentence = 'AI 반도체주는 올들어 주가가 급등세를 이어오며 밸류에이션이 많이 높아진 상황이다. 따라서 반도체기업들의 실적이 높은 밸류에이션을 정당화하면서 주가를 더 끌어올릴 수 있을 만큼 좋을 수 있을 것인가가 관건이다. 이는 오는 9월 금리 인하 가능성이 높아지면서 그간 많이 올랐던 AI 수혜주와 대형주에서 주가가 지지부진했던 중소형주로 순환매가 가속화할 것인가를 결정하는데 있어서도 중요하다. 지난 11일에 6월 소비자 물가지수(CPI)가 예상치보다 낮게 나오자 S&P500지수와 나스닥지수는 하락하고 소형주 지수인 러셀2000지수는 급등했다. 지난 12일에는 S&P500지수와 나스닥지수도 올랐지만 러셀2000지수의 상승률이 더 컸다.'

##    정규 표현식(특문 제거)
regSentence = re.sub(r'[^A-Za-z0-9가-힣\s]', '', sentence)
print(f'특수문자가 제거된 뉴스 : \n{regSentence}')
input()

##    형태소 분석
okt = Okt()
oktSentence = okt.morphs(regSentence)   # stem = True 안씀. 반도체주 -> '반도체', '주다'
print(f'형태소 분석한 뉴스 : \n{oktSentence}')
input()

##    딕셔너리화
tokenizer = Tokenizer()
tokenizer.fit_on_texts(oktSentence)
print(f'딕셔너리화 : \n{tokenizer.word_index}')
input()
print(f"key가 '주가'에 해당하는 value : \n{tokenizer.word_index['주가']}")
input()

##    문장 정수화
indexSentence = tokenizer.texts_to_sequences(oktSentence)
print(f'뉴스를 정수화 : \n{indexSentence}')
input()

##    딕셔너리 수정
newWord = ['반도체주','급등세','밸류에이션','수혜주','순환매','가속화','소비자물가지수','예상치','sp500','소형주','러셀2000','상승률']
newWordIndex = []
newIndex = max(tokenizer.word_index.values())+1
for index, word in enumerate(newWord):
  tokenizer.word_index[word] = newIndex + index
  tokenizer.index_word[newIndex + index] = word
  newWordIndex.append(newIndex + index)
print(f'새로운 단어가 추가된 사전 : \n{tokenizer.word_index}')
input()
print(f'새로운 단어들의 인덱스 값 : \n{newWordIndex}')
input()

##    수정된 딕셔너리로 정수 문장 다시 맵핑
combinedWord = [['반도체','주는'],['급등','세'],['밸류', '에', '이', '션'],['수', '혜주'],['순환', '매가'],['가속', '화할'],['소비자', '물가', '지수'],['예', '상치'],['sp', '500'],['소', '형주'],['러셀', '2000'],['상', '승률']]

combinedIndex = []
for i in range(0, len(combinedWord)):
  tempList = []
  for word in combinedWord[i]:
    tempList.append(tokenizer.word_index[word])
  combinedIndex.append(tempList)
print(f'합칠 단어들의 리스트를 인덱스로 변환 : \n{combinedIndex}')
input()

flattenList = []
for i in range(0, len(indexSentence)):
  for index in indexSentence[i]:
    flattenList.append(index)
print(f'정수화 되었던 문장을 1차원 배열로 변환 : \n{flattenList}')
input()

for i in range(0, len(combinedIndex)):
  windowSize = len(combinedIndex[i])
  for j in range(len(flattenList)-windowSize):
    if flattenList[j:j+windowSize] == combinedIndex[i]:
      print(f'합칠 정수 발견 : {flattenList[j:j+windowSize]} => {newWordIndex[i]}')
      flattenList[j:j+windowSize] = [newWordIndex[i]]
print(f'\n리스트를 슬라이딩 윈도우로 새로운 인덱스로 치환 : \n{flattenList}')
input()

##    다시 문자화
unflattenList = []
for index in flattenList:
  tempList = []
  tempList.append(index)
  unflattenList.append(tempList)
originalText = tokenizer.sequences_to_texts(unflattenList)
print(f'2차원 배열로 변경 : \n{unflattenList}')
input()
print(f'다시 자른 문장 : \n{originalText}')
input()

##    불용어 처리
stopwords = ['가','를','따라서','의','이','을','이다','가','로','에']
stopwordRemoveSentence = [word for word in originalText if not word in stopwords]
print(f'불용어 처리된 문장 : \n{stopwordRemoveSentence}')
input()

##    결과
print('**************************************** 결과 ****************************************')
print(f'원본 : \n{sentence}')
print(f'\n정제된 문장 : \n{stopwordRemoveSentence}')
print(f'\n인덱스된 문장 : \n{tokenizer.texts_to_sequences(stopwordRemoveSentence)}')
print(f'\n사전 : \n{tokenizer.word_index}')