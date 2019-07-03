# -*- coding: utf-8 -*-
import os
import re
import urllib.request

import scrapy
from scrapy.http import Request, FormRequest

from ..items import DoubanItem


class Db1Spider(scrapy.Spider):
    name = 'db1'
    allowed_domains = ['douban.com']
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}

    # start_urls = ['http://douban.com/']

    def start_requests(self):
        # 内置方法， 第一次爬取的请求
        # 爬取登录页面，看是否有验证码
        return [Request(
            'https://accounts.douban.com/login',
            meta={'cookiejar': 1},
            callback=self.parse)]

    def parse(self, response):
        # 判断是否有验证码
        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()
        if len(captcha) > 0:
            # 有验证码时：
            # https://www.douban.com/misc/captcha?id=Pmdtvhucnz8W8fZLoRNftDX0:en&amp;size=s
            # source: index_nav
            # form_email: 18234126616
            # form_password: woaiyou.1
            # captcha - solution: across
            # captcha - id: ShFcRarhYbFDWkaKM4LezBhX:en
            # user_login: 登录
            localpath = '/media/wangxl/a84d5450-ee22-469c-a813-c774821af033/wangxl/爬虫笔记/PythonAPI/captcha.png'
            urllib.request.urlretrieve(captcha[0], filename=localpath)
            captchaid = re.compile('.*?captcha\?id=(.*?)&', re.S).findall(captcha[0])
            # answer = input('请输入验证码：')
            print('--------正在识别验证码-------')
            r = os.popen(
                'python3 /media/wangxl/a84d5450-ee22-469c-a813-c774821af033/wangxl/爬虫笔记/PythonAPI/ydm.py')
            answer = r.read()
            print('识别成功！识别结果：', answer)
            data = {
                'source': 'index_nav',
                'redir': 'https://www.douban.com/',
                'form_email': '18234126616',
                'form_password': 'woaiyou.1',
                'captcha-solution': answer,
                'captcha-id': captchaid[0],
                'login': '登录'
            }

        else:
            data = {
                'source': 'index_nav',
                'redir': 'https://www.douban.com/',
                'form_email': '18234126616',
                'form_password': 'woaiyou.1',
                'login': '登录'
            }
        return [FormRequest.from_response(
            response,
            meta={'cookiejar': response.meta['cookiejar']},
            headers=self.header,
            formdata=data,
            callback=self.next
        )]

    def next(self, response):
        title = response.xpath("/html/head/title/text()").extract()
        print(title)
        return [Request(
            'https://movie.douban.com/subject/26302614/comments?&sort=new_score&status=P',
            meta={'cookiejar': response.meta['cookiejar']},
            headers=self.header,
            callback=self.duanping_index
        )]

    def duanping_index(self, response):
        item = DoubanItem()
        item['name'] = response.xpath('//span[@class="comment-info"]/a/text()').extract()
        item['comment'] = response.xpath('//span[@class="short"]/text()').extract()
        item['zan'] = response.xpath('//span[@class="votes"]/text()').extract()
        yield item
        for i in range(1, 24):
            start = 20 * i
            url = 'https://movie.douban.com/subject/26302614/comments?start=' + str(
                start) + '&limit=20&sort=new_score&status=P'
            yield Request(url, headers=self.header, callback=self.duanping_index,
                          meta={'cookiejar': response.meta['cookiejar']})
