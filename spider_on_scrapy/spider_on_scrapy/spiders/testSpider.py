import scrapy
from spider_on_scrapy.items import ScrapyItem
import re
import json


class testSpider(scrapy.Spider):
    name = 'test'
    start_urls = ['http://search.51job.com/jobsearch/search_result.php' \
                  '?keyword=python&curr_page={}'.format(x) for x in range (1, 453)]

    def parse(self, response):
        for sel in response.xpath('//div[@class="el"]/p//a/@href')[1:]:
            url = sel.extract()
            yield scrapy.Request(url, callback=self.parse_jobs)

    def parse_jobs(self, response):
        item = ScrapyItem()
        info = []
        filterlist = ['zhaopin', 'www', 'com', 'cn', 'python','hr','api','ps','pc']
        item['title'] = response.xpath('//div[@class="cn"]/h1/text()').extract() or ['NULL']
        item['location'] = response.xpath('//div[@class="cn"]/span/text()').extract() or ['NULL']
        item['salary'] = response.xpath('//div[@class="cn"]/strong/text()').extract() or ['NULL']
        item['cname'] = response.xpath('//div[@class="cn"]/p/a/text()').extract() or ['NULL']
        item['jobID'] = re.findall('[0-9]{3,}', response.url)[0]

        data = response.xpath('//div[@class="t1"]/span/text()').extract() or 'NULL'
        for i in data:
            if '发布' in i:
                item['date'] = i

        if '-' in item['location'][0]:
            item['location'] = item['location'][0].split('-')[0]
        else:
            item['location'] = item['location'][0]

        if 'python' in item['title'][0] or 'Python' in item['title'][0]:
            item['info'] = response.xpath('//div[@class="bmsg job_msg inbox"]/text()').extract() or 'NULL'
        else:
            item['info'] = ['NULL']
        if item['info'] != 'NULL':
            for i in item['info']:
                if re.findall(('\t*\r\n\t+'), i):
                    if i != re.findall(('\t*\r\n\t+'), i)[0]:
                        info.append(i.strip())
                else:
                    info.append(i)
            item['info'] = info
        keyword = set()
        if item['info'] :
            for i in item['info']:
                key = re.findall('[a-zA-Z]{2,}', i)
                if key:
                    for i in key:
                        if i.lower() not in filterlist:
                            keyword.add(i.lower())
        item['keyword'] = json.dumps({item['location']: list(keyword)})
        #item['keyword'] = list(keyword)
        return item