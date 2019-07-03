# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import HexunItem
import re
import requests
# import urllib.request


class HxSpider(CrawlSpider):
    name = 'hx'
    allowed_domains = ['hexun.com']
    start_urls = ['http://blog.hexun.com/']

    rules = (
        Rule(LinkExtractor(allow=('http://.*?.blog.hexun.com/.*?_d.html'),
                           allow_domains=('hexun.com')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = HexunItem()
        item['title'] = response.xpath(
            '//span[@class="ArticleTitleText"]/a/text()').extract()[0]
        item['link'] = response.url
        pat_link = '(http://click.tool.hexun.com/click.aspx\?articleid=.*?)"'
        clicklink = re.compile(pat_link, re.S).findall(str(response.body))[0]
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Referer': response.url
        }
        data = requests.get(clicklink, headers=header).text
        # opener = urllib.request.build_opener()
        # headall = []
        # for k, v in header.items():
        #     i = (k, v)
        #     headall.append(i)
        # opener.addheaders = headall
        # urllib.request.install_opener(opener)
        # print(clicklink)
        # data = urllib.request.urlopen(
        #     clicklink).read().decode('utf-8', 'ignore')
        # with open('./hx.txt', 'a+', encoding='utf-8') as f:
        #     f.write(data + '\n' + '\n')
        # document.getElementById("articleClickCount").innerHTML = 1748;
        # document.getElementById("articleCommentCount").innerHTML = 0;
        pat_click = '"articleClickCount"\).innerHTML = (.*?);'
        pat_comment = '"articleCommentCount"\).innerHTML = (.*?);'
    #   pat_click = '"articleClickCount"\).innerHTML = (.*?);'
    #   pat_comment = '"articleCommentCount"\).innerHTML = (.*?);'
        item['click'] = re.compile(pat_click, re.S).findall(data)[0]
        item['comment'] = re.compile(pat_comment, re.S).findall(data)[0]
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return item

    # rules = (
    #     Rule(LinkExtractor(allow=('http://.*?.blog.hexun.com/.*?_d.html'),
    #                        allow_domains=('hexun.com')), callback='parse_item', follow=True),
    # )

    # def parse_item(self, response):
    #     item = HexunItem()
    #     item["title"] = response.xpath(
    #         "//span[@class='ArticleTitleText']/a/text()").extract()[0]
    #     item["link"] = response.url
    #     pat_link = '(http://click.tool.hexun.com/click.aspx\?articleid=.*?)"'
        # pat_link = '(http://click.tool.hexun.com/click.aspx\?articleid=.*?)"'
    #     # fh=open("./hx_test.html","w",encoding="utf-8")
    #     # fh.write(str(response.body))
    #     # fh.close()
    #     click_link = re.compile(pat_link, re.S).findall(str(response.body))[0]
    #     headers = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
    #         "Referer": response.url,
    #     }
    #     opener = urllib.request.build_opener()
    #     headall = []
    #     for key, value in headers.items():
    #         item1 = (key, value)
    #         headall.append(item1)
    #     opener.addheaders = headall
    #     urllib.request.install_opener(opener)
    #     click_data = urllib.request.urlopen(
    #         click_link).read().decode("utf-8", "ignore")
    #     pat_click = '"articleClickCount"\).innerHTML = (.*?);'
    #     pat_comment = '"articleCommentCount"\).innerHTML = (.*?);'
    #     click = re.compile(pat_click, re.S).findall(click_data)[0]
    #     comment = re.compile(pat_comment, re.S).findall(click_data)[0]
    #     item["click"] = str(click)
    #     item["comment"] = str(comment)
    #     #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    #     #i['name'] = response.xpath('//div[@id="name"]').extract()
    #     #i['description'] = response.xpath('//div[@id="description"]').extract()
    #     return item
