from django.test import TestCase

# Create your tests here.
import re
import requests
from lxml import etree
import threading
import pymysql

def getURL(i):
    start_url = 'http://so.csdn.net/so/search/s.do?q=python&t=blog&p={}'.format(i)
    html = requests.get(start_url, headers=header)
    sel = etree.HTML(html.text)
    urlList = sel.xpath('//dd[@class="search-link"]/a/@href')
    for url in urlList:
        getData(url)

def getData(url):
    data = {}
    conn = pymysql.Connection(host='192.168.1.106',user='root',password='root',db='django',charset='utf8')
    cursor = conn.cursor()
    html = requests.get(url, headers=header)
    sel = etree.HTML(html.text)
    data['title'] = sel.xpath('//title/text()')[0].split('-')[0]
    body = sel.xpath('//div[@class="article_content"]/p/text()')
    if body != []:
        for i in body:
            data['body'] = ''.join(i)
        cursor.execute("insert into blog_blog values('test', %s, %s, '2016-11-15','test')", (data['title'], data['body']))

if __name__ == '__main__':
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    for i in range(1,11):
        thread = threading.Thread(target=getURL, args=[i])
        thread.start()