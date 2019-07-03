# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from ..items import DangdangItem


class DdwSpider(scrapy.Spider):
    name = 'ddw'
    allowed_domains = ['dangdang.com']
    start_urls = [
        'http://search.dangdang.com/?key=%C1%AC%D2%C2%C8%B9&act=input&page_index=1']

    def parse(self, response):
        item = DangdangItem()
        item['url'] = response.xpath("//p[@class='name']/a/@href").extract()
        item['title'] = response.xpath("//p[@class='name']/a/@title").extract()
        item['price'] = response.xpath(
            "//span[@class='price_n']/text()").extract()
        item['count'] = response.xpath("//p[@class='star']/a/text()").extract()
        yield item
        for i in range(2, 101):
            url = 'http://search.dangdang.com/?key=%C1%AC%D2%C2%C8%B9&act=input&page_index=' + \
                str(i)
            yield Request(url, callback=self.parse)
