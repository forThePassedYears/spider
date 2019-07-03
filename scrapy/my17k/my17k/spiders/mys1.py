# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from ..items import My17KItem


class Mys1Spider(scrapy.Spider):
    name = 'mys1'
    allowed_domains = ['17k.com']
    start_urls = ['http://www.17k.com/book/1.html']

    def parse(self, response):
        item = My17KItem()
        item['name'] = response.xpath('//div[@class="Info "]/h1/a/text()').extract()
        print('--------------' + item['name'][0] + '-----------------')
        yield item
        for i in range(2, 3011081):
            thisurl = 'http://www.17k.com/book/' + str(i) + '.html'
            yield Request(thisurl, callback=self.parse)
