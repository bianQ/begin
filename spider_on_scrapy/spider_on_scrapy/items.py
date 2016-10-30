# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyItem(scrapy.Item):
    link = scrapy.Field()
    cname = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    date = scrapy.Field()
    #info = scrapy.Field()