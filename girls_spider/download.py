import requests
import url
import os
from lxml import etree

headers = {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Set-Cookie':
    'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Connection': 'Keep-Alive', 'Date':
    'Thu, 13 Oct 2016 11:56:59 GMT', 'Content-Type': 'text/html', 'Last-Modified':
    'Mon, 25 Jul 2016 11:11:39 GMT', 'Pragma': 'no-cache', 'Content-Encoding':
    'gzip', 'Server': 'bfe/1.0.8.18', 'Transfer-Encoding': 'chunked'}

def download(list):
        #设定各类型图片的根目录
        root_dir = 'C:/Users/邊/Desktop/My_Python/爬虫/girls/' + list[0]
        #获取美女标题作为文件夹名称
        girl_folders = list[1].keys()
        for girl_folder in girl_folders:
            #图片保存路径
            girl_dir = root_dir + '/' + girl_folder
            #获取每个美女的url list
            img_url = list[1][girl_folder]
            x = 1
            #判断保存图片的文件夹是否存在，若不存在则创建
            if not os.path.exists(girl_dir):
                os.makedirs(girl_dir)
            #遍历每个美女的url list
            for each_url in img_url:
                #设置图片保存路径
                path = os.path.join(girl_dir, str(x)) + '.jpg'
                with open(path,'wb') as root:
                    try:
                        #通过xpath获取图片的url并与主域名拼接
                        html = requests.get(each_url)
                        selector = etree.HTML(html.text)
                        urls = selector.xpath('//div[@class="picbox"]/p/img/@src')[0]
                        Url = 'http://www.zbjuran.com/' + urls
                        data = requests.get(Url)
                        root.write(data.content)
                        x += 1
                    except IndexError:
                        print('下载失败 —— —— ！ 。。。')
                        pass
                print('%s 下载成功。。。' % path)
