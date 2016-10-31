import requests
from bs4 import BeautifulSoup
import os
import random
import time

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36',
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
          }

def download(url, dir):
    html = requests.get(url, headers=header)
    soup = BeautifulSoup(html.content,'html.parser')
    title = soup.find('title').get_text()[:-9]
    contents = soup.find('div','detail')

    root_dir = os.path.join('E:\\爬虫数据', 'qdaily_com')
    Dir = os.path.join(root_dir, dir)
    if not os.path.exists(Dir):
        os.makedirs(Dir)

    error_str = ['\\','/','*','?','"',':','<','>','|']
    for str in error_str:
        if str in title:
            title = title.split(str)[0]
    filename = os.path.join(Dir, title + '.txt')
    l = []
    for content in contents:
        if isinstance(content,type(list(contents)[0])):
            data = content.get_text().strip()
            if '\n' not in data and data != '':
                l.append('    '+data)
    with open(filename,'wb') as file:
        for i in l[1:-1]:
            file.write((i+'\r\n\r\n').encode())
    time.sleep(random.randrange(3))
    print('%s 下载完成。。。' % title)

