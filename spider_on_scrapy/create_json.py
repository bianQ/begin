import json
import pymysql
import os
import re


filename = os.path.join(os.getcwd(), 'data.txt')
city = []
keyword = []
with open(filename, 'r')as f:
    file = f.read()
    data_list = da = re.findall('(\{.+?\})',file)
    for i in data_list:
        data = json.loads(i)
        for key in data.keys():
            if data[key] != ['null']:
                city.append(key)
                keyword.append(data[key])

city_result = {}
keyword_result = {}
for item in city:
    city_result[item] = city_result.setdefault(item, 0) + 1

for item in keyword:
    for word in item:
        keyword_result[word] = keyword_result.setdefault(word, 0) + 1

with open('city.json','w', encoding='utf-8') as file:
    file.write(json.dumps(city_result))

with open('keyword.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(keyword_result))
