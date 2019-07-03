# -*- coding: utf-8 -*-

from urllib.request import urljoin
import requests
import re

from fake_useragent import UserAgent


class BiliBiliSpider(object):
    """爬取哔哩哔哩弹幕"""

    def __init__(self):
        self.url = 'https://www.bilibili.com/'
        self.base_url = 'https://m.bilibili.com{}.html'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'}
        self.ua = UserAgent()

    def parse_url(self, url):
        """根据URL获取响应"""
        if 'm.' in url:
            response = requests.get(url, headers=self.headers)
        else:
            response = requests.get(url, headers={'User-Agent': self.ua.random})
        res = response.content.decode()
        return res if response.status_code == 200 else None

    def get_urls(self, response):
        """提取URL"""
        pat = re.compile(r'(/video/av\d+)["/?]', re.S)
        urls = pat.findall(response)
        return urls

    def get_shot_id(self, url):
        """获取字幕文件的ID"""
        response = self.parse_url(url)
        pat_id = re.compile('comment.bilibili.com.*?(\d+).*?xml', re.S)
        ids = pat_id.findall(response)
        return ids[0] if len(ids) > 0 else None

    def show_comments(self, shot_id):
        """打印评论内容"""
        url = 'https://comment.bilibili.com/{}.xml'.format(shot_id)
        response = self.parse_url(url)
        if response is not None:
            comments = re.compile(r'>(.*?)<', re.S).findall(response)
            for comment in comments[8::2]:
                print(comment)

    def run(self):
        response = self.parse_url(self.url)
        avs = self.get_urls(response)
        urls = [self.base_url.format(av) for av in avs]
        shot_ids = [self.get_shot_id(url) for url in urls]
        for shot_id in shot_ids:
            if shot_id is not None:
                self.show_comments(shot_id)


if __name__ == '__main__':
    b = BiliBiliSpider()
    b.run()
