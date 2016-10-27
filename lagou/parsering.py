import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
import random
from download import intoMongo


class parsering(object):

    def __init__(self, job, city):
        self.job = job
        self.city = city
        self.page = self.getPage()

    def getPage(self):
        #获取查询结果总页数
        url = 'http://www.lagou.com/jobs/list_{job}?city={city}'.format(job=self.job, city=self.city)
        html = requests.get(url)
        selector = etree.HTML(html.text)
        page = selector.xpath('//span[@class="span totalNum"]/text()')[0]
        return int(page)

    def getjobInfo(self, url):
        #通过json数据构造每条招聘的详细信息
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        data = soup.find_all('dd', class_='job_bt')
        for item in data:
            return item.get_text().strip()

    def getPageResult(self):
        #解析json数据，获取想要的信息，并调用intoMongo()保存到数据库
        pageUrl = 'http://www.lagou.com/jobs/positionAjax.json?city={city}&needAddtionalResult=false'.format(city=self.city)
        x = 1
        for page in range(self.page):
            post_data = {'pn': page+1,'kd': self.job}
            html = requests.post(pageUrl, data=post_data)
            json_data = html.json()['content']['positionResult']['result']
            if json_data:
                for data in json_data:
                    url = 'http://www.lagou.com/jobs/{id}.html'.format(id=data['positionId'])
                    jobInfo = self.getjobInfo(url)
                    dataInfo = {'公司名称': data['companyFullName'],
                                '公司规模': data['companySize'],
                                '职位名称': data['positionName'],
                                '工作经验': data['workYear'],
                                '学历要求': data['education'],
                                '薪资待遇': data['salary'],
                                '发布时间': data['createTime'],
                                '招聘详情': jobInfo,
                                '源链接': url
                                }
                    if dataInfo:
                        intoMongo(dataInfo)
                        print('已获取到 %s 条相关职位信息。。。' % x)
                        x += 1
                        time.sleep(random.randrange(1,2))