# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy import Request
from scrapy import signals
from scrapy.xlib import pydispatch
from selenium import webdriver

from ..items import LagoyJobItemLoader, LagouJobItem
from ..utils.common import get_md5


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/Python/?labelWords=label']

    def __init__(self):
        # 当spider初始化时， 添加driver
        self.driver = webdriver.Chrome(
            executable_path='/media/wangxl/a84d5450-ee22-469c-a813-c774821af033/wangxl/chromedriver/chromedriver',
        )
        super(LagouSpider, self).__init__()
        # 当收到spider_closed信号时，执行self.spider_closed方法
        pydispatch.dispatcher.connect(
            self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print('spider closed!')
        self.driver.quit()

    def parse(self, response):
        # 取出当前页的job URL
        job_urls = response.xpath(
            '//a[@class="position_link"]/@href').extract()
        for url in job_urls:
            yield Request(url=url, callback=self.parse_detail)

        # 取出下一页
        pages_num = response.xpath(
            '//div[@class="pager_container"]//a/text()').extract()[-2]
        for i in range(1, int(pages_num)):
            next_url = 'https://www.lagou.com/zhaopin/Python/' + \
                str(i) + '/?filterOption=3'
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        # 解析拉钩网的job
        item_loader = LagoyJobItemLoader(
            item=LagouJobItem(), response=response)
        item_loader.add_xpath('title', '//div[@class="job-name"]/@title')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('salary', '.job_request .salary::text')
        item_loader.add_xpath(
            'job_city', '//*[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath(
            'work_years', '//*[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath(
            'degree_need', '//*[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath(
            'job_type', '//*[@class="job_request"]/p/span[5]/text()')
        item_loader.add_xpath('job_advantage', '//*[@class="job-advantage"]')
        item_loader.add_xpath('job_desc', '//*[@class="job_bt"]')
        item_loader.add_xpath(
            'publish_time', '//*[@class="publish_time"]/text()')
        item_loader.add_xpath('job_addr', '//*[@class="work_addr"]')
        item_loader.add_xpath(
            'company_name', '//*[@id="job_company"]/dt/a/img/@alt')
        item_loader.add_xpath(
            'company_url', '//*[@id="job_company"]/dt/a/@href')
        item_loader.add_value('crawl_time', datetime.now())

        job_item = item_loader.load_item()

        return job_item
