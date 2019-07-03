# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class JdplPipeline(object):
    def __init__(self):
        headers = ['商品型号', '评论内容']
        with open('./jdcomments.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()

    def process_item(self, item, spider):
        print('---------------------------进入pipeline--------------------------')
        with open('./jdcomments.csv', 'a', newline='') as f:
            headers = ['商品型号', '评论内容']
            writer = csv.DictWriter(f, headers)
            row = {'商品型号': item['model'],
                   '评论内容': item['comment']}
            writer.writerow(row)
        return item
