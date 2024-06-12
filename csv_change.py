import csv

data_dict = {}

with open('data_2353_20240612.csv', mode='r', encoding='cp949') as file:
    reader = csv.reader(file)
    next(reader)
    
    for row in reader:
        key = row[0]
        value = row[2]
        
        data_dict[key] = value

print(data_dict)

