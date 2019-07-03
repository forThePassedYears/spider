# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class HexunPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1', user='root', passwd='123456', db='pc')

    def process_item(self, item, spider):
        title = item['title']
        link = item['link']
        click = item['click']
        comment = item['comment']
        sql = "insert into hexun(title,link,click,comment) values('%s','%s','%s','%s')" % (
            str(title), str(link), str(click), str(comment))
        self.conn.query(sql)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
