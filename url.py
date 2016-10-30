import requests
from lxml import etree


headers = {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Set-Cookie':
    'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Connection': 'Keep-Alive', 'Date':
    'Thu, 13 Oct 2016 11:56:59 GMT', 'Content-Type': 'text/html', 'Last-Modified':
    'Mon, 25 Jul 2016 11:11:39 GMT', 'Pragma': 'no-cache', 'Content-Encoding':
    'gzip', 'Server': 'bfe/1.0.8.18', 'Transfer-Encoding': 'chunked'}
def get_UrlList(url, xpath):
    #函数返回url或url list
    html = requests.get(url)
    selector = etree.HTML(html.text)
    urls = selector.xpath(xpath)
    return urls

def get_girlTitle(url, xpath):
    #函数返回每个美女的标题名称。因编码问题额外写一个
    html = requests.get(url)
    selector = etree.HTML(html.content.decode('gbk'))
    title = selector.xpath(xpath)
    return title

def getUrlDict(list):
    #函数返回关于美女类型及url list的dict
    url = 'http://www.zbjuran.com'
    xinggan = []
    qingchun = []
    xiaohua = []
    mingxing = []
    for each_urls in list:
        if 'xinggan' in each_urls:
            xinggan.append(''.join([url,each_urls]))
        if 'qingchun' in each_urls:
            qingchun.append(''.join([url,each_urls]))
        if 'xiaohua' in each_urls:
            xiaohua.append(''.join([url,each_urls]))
        if 'mingxing' in each_urls:
            mingxing.append(''.join([url,each_urls]))
    return {'xinggan': xinggan,'qingchun':qingchun,'xiaohua':xiaohua,'mingxing':mingxing}

def get_pageDict(dict, type, pageUrlXapth):
    '''函数返回一个list 起初打算返回dict，后来发现list好用一点，名字也懒得换了
    返回格式例如 [type,{title:[url]}]
    '''
    pageUrlDict = {}
    girlList = {}
    list = dict[type]
    for url in list:
        title = get_girlTitle(url, '//div[@class="title"]/h2/text()')
        #第一页的url直接添加进list
        pageUrl = [url]
        links = get_UrlList(url, pageUrlXapth)
        #去除用于翻页的多余的url
        pageLinks = links[2:-1]
        for page in pageLinks:
            #替换第一页的url的尾部，生成其它页面的url
            pageUrl.append(url.replace(url.split('/')[-1], page))
        #将url list及title添加近dict
        pageUrlDict[str(title)] = pageUrl
        #生成最终的list
        girlList = [type, pageUrlDict]
    return girlList
