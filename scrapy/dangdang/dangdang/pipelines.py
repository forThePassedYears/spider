# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re


class DangdangPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(
            host='127.0.0.1', user='root', passwd='123456', db='pc')
        counts = list(re.compile('\d+', re.S).findall(str(item['count'])))
        prices = list(re.compile('\d+\.\d+', re.S).findall(str(item['price'])))
        for i in range(0, len(item['title'])):
            url = item['url'][i]
            title = item['title'][i]
            price = prices[i]
            count = counts[i]
            sql = "insert into dangdang(url,title,price,count) values('%s','%s','%s','%s')" % (
                url, title, price, count)
            try:
                conn.query(sql)
                conn.commit()
            except Exception as err:
                print('----------此条数据未插入---------')
                continue
        conn.close()
        return item
