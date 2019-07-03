# -*- coding: utf-8 -*-
import scrapy
from ..items import JdplItem
from scrapy.http.request import Request
import urllib.request
import re
import time
import json


class Jd1Spider(scrapy.Spider):
    name = 'jd1'
    allowed_domains = ['jd.com']
    # start_urls = ['http://jd.com/']

    def start_requests(self):
        keyname = input('请输入要查询的商品：')
        key = urllib.request.quote(keyname)
        url = 'https://search.jd.com/Search?keyword=' + \
            str(key) + '&enc=utf-8&wq=' + str(key)
        yield Request(url, callback=self.parse)

    def parse(self, response):
        res = response.body.decode('gbk', 'ignore')
        sku_list = re.compile(
            'class="gl-item" data-sku="(.*?)"', re.S).findall(res)
        if len(sku_list) > 0:
            for sku in sku_list:
                for i in range(0, 100):
                    print('----------正在爬取第%s页-----------' % (str(i),))
                    if(i % 2 == 0):
                        thisurl = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv100258&productId=' + \
                            str(sku) + '&score=0&sortType=5&page=' + \
                            str(i) + '&pageSize=10&isShadowSku=0&fold=1'
                    else:
                        thisurl = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2477&productId=' + \
                            str(sku) + '&score=0&sortType=5&page=' + \
                            str(i) + '&pageSize=10&isShadowSku=0&fold=1'
                    time.sleep(0.5)
                    yield Request(thisurl, callback=self.parse_next)
        else:
            print('-----------当前查询未成功----------')

    def parse_next(self, response):
        item = JdplItem()
        reqdata = response.body.decode('gbk', 'ignore')
        if len(reqdata) < 10000:
            print('-----------当前页未爬取成功-----------')
            pass
        else:
            data = re.compile('fetchJSON_comment.*?\((.*?)\);',
                              re.S).findall(reqdata)[0]
            data2 = json.loads(data)
            for i in data2['comments']:
                item['model'] = (i['productColor'] + i['productSize'])
                item['comment'] = i['content']
                yield item
