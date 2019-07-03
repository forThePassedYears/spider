# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
import urllib.parse as par
from ..items import JobBoleArticleItem
from ..utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbloe.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # 收集伯乐在线所有的404页面的数量，以及404页面的URL
    handle_httpstatus_list = [404]

    def __init__(self):
        self.fail_urls = []
        # 信号的使用
        dispatcher.connect(handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value('failed_urls', ','.join(self.fail_urls))

    def parse(self, response):
        if response.status == 404:
            self.fail_urls.append(response.url)
            # 404 页面数+1
            self.crawler.stats.inc_value('failed_urls')

        post_nodes = response.xpath(
            '//div[@id="archive"]/div[@class="post floated-thumb"]/div[@class="post-thumb"]/a')
        for node in post_nodes:
            image_url = node.xpath('img/@src').extract_first()
            post_url = node.xpath('@href').extract_first()
            yield Request(
                url=par.urljoin(response.url, post_url),
                callback=self.parse_detail,
                meta={'front_image_url': image_url},
                dont_filter=True)

        next_url = response.xpath(
            '//a[@class="next page-numbers"]/@href').extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        # 解析文章详细字段
        # 文章标题
        front_image_url = response.meta.get('front_image_url', '')
        title = response.xpath(
            '//div[@class="entry-header"]/h1/text()').extract_first()
        # 文章发表时间
        create_date_tmp = response.xpath(
            '//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first()
        create_date = create_date_tmp.strip().replace(' ·', '')
        # 文章类型
        tag_list = response.xpath(
            '//p[@class="entry-meta-hide-on-mobile"]//a/text()').extract()
        tag_list2 = [ele for ele in tag_list if not ele.endswith('评论')]
        tags = ','.join(tag_list2)
        # 赞 评 收藏
        fav_list = response.xpath(
            '//div[@class="post-adds"]//span/text()').extract()[2:]
        zan = response.xpath(
            '//div[@class="post-adds"]//h10/text()').extract_first()
        fav_list.append(zan + '赞')

        fav_nums = fav_list[0]
        comment_nums = fav_list[1]
        praise_nums = fav_list[2]

        articleitem = JobBoleArticleItem()
        articleitem['title'] = title
        articleitem['url'] = response.url
        articleitem['create_date'] = create_date
        articleitem['tags'] = tags
        articleitem['fav_nums'] = fav_nums
        articleitem['comment_nums'] = comment_nums
        articleitem['praise_nums'] = praise_nums
        articleitem['front_image_url'] = [front_image_url]
        articleitem['url_object_id'] = get_md5(response.url)
        yield articleitem
