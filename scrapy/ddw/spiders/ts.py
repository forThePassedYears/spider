# -*- coding: utf-8 -*-
import scrapy


class TsSpider(scrapy.Spider):
    name = 'ts'
    allowed_domains = ['hellobi.com']
    start_urls = ['http://hellobi.com/']

    def parse(self, response):
        pass
