# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi


class SpiderOnScrapyPipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
            dbapiName = 'pymysql',
            host = '192.168.1.106',
            db = 'scrapy',
            user = 'root',
            passwd = 'root',
            cursorclass = pymysql.cursors.DictCursor,
            charset = 'utf8'
        )
        self.file = open('data.txt', 'wb')

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_db, item)
        self.file.write(item['keyword'].encode())
        return item

    def insert_db(self, conn, item):
        conn.execute("select * from 51job where jobID = %s", item['jobID'])
        result = conn.fetchone()
        if result:
            conn.execute("update 51job set title=%s, salary=%s, date=%s,cname=%s, location=%s"
                         " where jobID=%s", (item['title'][0], item['salary'][0], item['date'],
                         item['cname'][0],item['location'], item['jobID']))

        else:
            conn.execute("insert into 51job values (%s, %s, %s, %s, %s, %s)",
                         (item['jobID'], item['title'][0], item['salary'][0], item['date'],
                         item['cname'][0],item['location']))

    def closeSpider(self):
        self.file.close()