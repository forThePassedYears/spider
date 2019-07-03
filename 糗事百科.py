# -*- coding: utf-8 -*-

import requests
import threadpool
from lxml import etree
from w3lib.html import remove_tags
from fake_useragent import UserAgent
from retrying import retry
import re


class QiuShiSpider(object):

    def __init__(self):
        self.base_url = 'https://www.qiushibaike.com/text/page/{}/'
        self.ua = UserAgent()

    @retry(stop_max_attempt_number=3)
    def parse_url(self, url):
        response = requests.get(url, headers={'User-Agent': self.ua.random})
        return response.content.decode() if response.status_code == 200 else ''

    @staticmethod
    def parse_response(response):
        pat = '<div class="content">.*?<span>(.*?)</span>'
        contents = re.compile(pat, re.S).findall(response)
        return contents

    @staticmethod
    def save_and_print(contents):
        with open('QiuShiSpider.txt', 'a') as f:
            for content in contents:
                f.write(remove_tags(content.strip()))
                f.write('\n----------------------------\n')
                print(remove_tags(content.strip()))
                print('-------------------------\n')

    def run(self):
        # 多线程方法
        # codes = [self.base_url.format(page) for page in range(10)]
        # pool = threadpool.ThreadPool(5)
        # tasks = threadpool.makeRequests(self.parse_url, codes)
        # [pool.putRequest(task) for task in tasks]
        # pool.wait()
        # 时间 0.7762303352355957
        # 单线程方法
        # 时间 2.872859477996826
        for i in range(1, 10):
            url = self.base_url.format(i)
            response = self.parse_url(url)
            contents = self.parse_response(response)
            self.save_and_print(contents)


if __name__ == '__main__':
    q = QiuShiSpider()
    q.run()
