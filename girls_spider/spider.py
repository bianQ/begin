import url
import download


if __name__ == '__main__':
    girlUrlXpath = '//div[@class="pic-list"]//a[@target="_blank"]/@href'
    pageUrlXapth = '//div[@class="page"]//a/@href'
    imgTitleXpath = '//div[@class="title"]/h2/text()'
    root_url = 'http://www.zbjuran.com/mei/'
    #返回所有美女图片的url
    girlUrls = url.get_UrlList(root_url, girlUrlXpath)
    #根据类型将url分类，并返回dict
    girlUrlDict = url.getUrlDict(girlUrls)
    #获取各类型的url list并调用download函数下载
    pageUrls_xinggan = url.get_pageDict(girlUrlDict, 'xinggan',pageUrlXapth)
    download.download(pageUrls_xinggan)
    print('性感美女图片下载成功。。。')
    pageUrls_qingchun = url.get_pageDict(girlUrlDict, 'qingchun', pageUrlXapth)
    download.download(pageUrls_qingchun)
    print('青春美女图片下载成功。。。')
    pageUrls_xiaohua = url.get_pageDict(girlUrlDict, 'xiaohua', pageUrlXapth)
    download.download(pageUrls_xiaohua)
    print('校花美女图片下载成功。。。')
    pageUrls_mingxing = url.get_pageDict(girlUrlDict, 'mingxing', pageUrlXapth)
    download.download(pageUrls_mingxing)
    print('明星美女图片下载成功。。。')

