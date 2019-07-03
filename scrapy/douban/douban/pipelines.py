# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class DoubanPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1', user='root', passwd='123456', db='pc'
        )

    def process_item(self, item, spider):
        for i in range(0, len(item['name'])):
            uname = item['name'][i]
            comment = item['comment'][i]
            zan = item['zan'][i]
            sql = "insert into douban(uname,comment,zan) values('%s','%s','%s')" % (str(uname), str(comment), str(zan))
            try:
                self.conn.query(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
                continue
        return item

    def close_spider(self, spider):
        self.conn.close()
