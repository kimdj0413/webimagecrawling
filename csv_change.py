import csv

from tqdm import tqdm

data_dict = {}

with open('data_2353_20240612.csv', mode='r', encoding='cp949') as file:
    reader = csv.reader(file)
    next(reader)
    
    for row in reader:
        key = row[0]
        value = row[2]
        
        data_dict[key] = value
# print(data_dict)
rows = []

with open('news_list.csv', mode='r', encoding='cp949') as file:
    reader = csv.reader(file)
    
    for row in tqdm(reader):
        key = row[0]
        if len(row) <= 2:  # 3열이 없는 경우
            row.append('')  # 빈 값 추가
        if key in data_dict:
            if int(data_dict[key])>0:
                row[2] = "1"
            else:
                row[2] = "0"
            # row[2] = data_dict[key]  # 3열 값을 딕셔너리의 value로 변경
        rows.append(row)
        # print(row[0]+"+"+row[1]+"+"+row[2])

with open('new_list_result.csv', mode='w', encoding='cp949', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)