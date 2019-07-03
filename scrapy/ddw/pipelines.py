# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DdwPipeline(object):
    def process_item(self, item, spider):
        with open('./jd_result.txt', 'a', encoding='utf-8') as f:
            title = item['title'][0]
            url = item['url']
            d = '网页标题：' + str(title) + '\n网页链接是：' + str(url)
            f.write(d)
        return item
