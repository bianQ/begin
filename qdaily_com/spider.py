from qdaily_com import parser
from qdaily_com import download

if __name__ == '__main__':
    x = 1
    root_url = 'http://www.qdaily.com'
    print('爬虫启动中，请稍后。。。')
    TypeUrlList = parser.getTypeUrlList(root_url)
    for type_url in TypeUrlList:
        TypeUrl = root_url + type_url
        print('开始加载网页。。。')
        UrlList = parser.getUrlList(TypeUrl)
        for url in UrlList[1]:
            Url = root_url + url
            download.download(Url, UrlList[0])
            x += 1

    print('爬虫运行完毕，共下载%s篇文章，请验收。。。' % x)