# -*- coding: utf-8 -*-

import requests
from fake_useragent import UserAgent
from lxml import etree
import re
import time
import random


class TiebaSpider(object):
    """百度贴吧爬虫

    爬取
    """

    def __init__(self, tieba_name, page_num=20):
        self.tieba_name = tieba_name
        self.base_url = 'http://tieba.baidu.com/f?kw=' + \
            self.tieba_name + '&ie=utf-8&pn={}'
        self.page_num = page_num
        self.ua = UserAgent()

    def get_url_list(self):
        """构造URL列表"""
        return [self.base_url.format(i * 50) for i in range(self.page_num)]

    def get_response(self, url):
        """获取响应内容"""
        headers = {'User-Agent': self.ua.random}
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            return None
        time.sleep(random.uniform(0.5, 2))
        pn = re.compile(
            '&pn=(.*?)$', re.S).findall(response.request.url)[0]
        pn = int(int(pn) / 50 + 1)
        if response.status_code == 200 and not response.is_redirect:
            print('-----------{}--第{}页---------------'.format(self.tieba_name, pn))
            return response.text.replace('<!--', '').replace('-->', '')
        else:
            print('----------{}-第{}页未爬取成功！---------------'.format(self.tieba_name, pn))
            return None

    def parse_response(self, response):
        """解析HTML 获取数据，并写入文件"""
        data = etree.HTML(response)
        contents = data.xpath(
            '//div[contains(@class, "j_threadlist_li_right")]')

        with open(self.tieba_name + '.txt', 'a') as f:
            for content in contents:
                title = content.xpath('div[1]/div[1]/a/text()')
                desc = content.xpath('div[2]/div[1]/div[1]/text()')
                t = title[0] if len(title) != 0 else None
                d = desc[0] if len(desc) != 0 else ''
                print(t.strip(), '\n', d.strip(), '\n',
                      '-------------------------')
                f.write(t.strip() + '\n')
                f.write(d.strip() + '\n')
                f.write('-------------------------- \n')

    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            response = self.get_response(url)
            if response is not None:
                self.parse_response(response)


if __name__ == '__main__':
    spider = TiebaSpider('中北大学')
    spider.run()
