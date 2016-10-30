import scrapy
from spider_on_scrapy.items import ScrapyItem
import re


class testSpider(scrapy.Spider):
    name = 'test'
    start_urls = ['http://search.51job.com/jobsearch/search_result.php?jobarea=040000%2C00&'
                  'keyword=python&curr_page={}'.format(x) for x in range (1, 48)]

    def parse(self, response):
        for sel in response.xpath('//div[@class="el"]/p//a/@href')[1:]:
            url = sel.extract()
            yield scrapy.Request(url, callback=self.parse_jobs)

    def parse_jobs(self, response):
        item = ScrapyItem()
        #delete = []
        item['title'] = response.xpath('//div[@class="cn"]/h1/text()').extract() or ['NULL']
        item['salary'] = response.xpath('//div[@class="cn"]/strong/text()').extract() or ['NULL']
        item['cname'] = response.xpath('//div[@class="cn"]/p/a/text()').extract() or ['NULL']
        data = response.xpath('//div[@class="t1"]/span/text()').extract() or 'NULL'
        for i in data:
            if '发布' in i:
                item['date'] = i
        item['link'] = response.url
        #item['info'] = response.xpath('//div[@class="bmsg job_msg inbox"]/text()').extract() or 'NULL'
        '''info2 = response.xpath('//div[@class="bmsg job_msg inbox"]/div/text()').extract()
        if info2:
            for i in info2:
                item['info'].append(i)

        info3 = response.xpath('//div[@class="bmsg job_msg inbox"]/div/div/text()').extract()
        if info3:
            for i in info3:
                item['info'].append(i)

        for i in item['info']:
            if re.findall(('\t*\r\n\t+'), i):
                if i == re.findall(('\t*\r\n\t+'), i):
                    delete.append(i)
                else :
                    item['info'][item['info'].index(i)] = i.strip()
                if i == '':
                    delete.append(i)
        for i in delete:
            item['info'].remove(i)'''

        return item