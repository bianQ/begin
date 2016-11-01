# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyItem(scrapy.Item):
    jobID = scrapy.Field()
    cname = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    date = scrapy.Field()
    keyword = scrapy.Field()
    location = scrapy.Field()
    info = scrapy.Field()