# -*- coding: utf-8 -*-
import scrapy


class Ts1Spider(scrapy.Spider):
    name = 'ts1'
    allowed_domains = ['hellobi.com']
    start_urls = ['http://hellobi.com/']

    def parse(self, response):
        pass
