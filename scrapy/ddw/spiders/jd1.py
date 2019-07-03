# -*- coding: utf-8 -*-
import scrapy
from ..items import DdwItem


class Jd1Spider(scrapy.Spider):
    name = 'jd1'
    allowed_domains = ['jd.com']
    start_urls = ['https://jd.com/']

    def parse(self, response):
        item = DdwItem()
        item['title'] = response.xpath('/html/head/title/text()').extract()
        item['url'] = response.url
        yield item
