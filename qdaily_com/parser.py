from selenium import webdriver
from lxml import etree
import requests
import time

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36',
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
          }

def getTypeUrlList(url):
    html = requests.get(url, headers=header)
    selector = etree.HTML(html.text)
    urls = selector.xpath('//div[@class="section-center"]/ul/li[@class="item cate "]/a/@href')
    return urls

def getUrlList(url):
    '''
    模拟鼠标滚动刷新，获取最终页面源码
    提取url及所属类别
    '''
    driver = webdriver.PhantomJS(executable_path='E:/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    driver.get(url)
    js1 = 'return document.body.scrollHeight'
    js2 = 'window.scrollTo(0, document.body.scrollHeight)'
    old_scroll_height = 0
    while(driver.execute_script(js1) > old_scroll_height):
        old_scroll_height = driver.execute_script(js1)
        driver.execute_script(js2)
        time.sleep(3)
    selector = etree.HTML(driver.page_source)
    urls = selector.xpath('//div[@class="packery-item article size1x2 animated fadeIn"]/a/@href')
    title = selector.xpath('//title/text()')[0][:-6]
    with open('downloadList.txt','wb') as file:
        file.write((str(title)+' : '+str(urls)).encode())
    print('网页加载完毕，即将开始下载。。。')
    return [title, urls]