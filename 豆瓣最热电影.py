# -*- coding: utf-8 -*-
# create_time: 18-12-22

import requests
import json


class DouBanSpider(object):
    """豆瓣爬虫
    
    爬取豆瓣上的最热电影
    """

    def __init__(self):
        self.base_url = 'https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?os=android&for_mobile=1&start={}&count=18&loc_id=108288'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36',
            'Referer': 'https://m.douban.com/movie/nowintheater?loc_id=108288'
        }

    def parse_url(self, url):
        """爬取内容"""
        response = requests.get(url, headers=self.headers, allow_redirects=False)
        if response.status_code == 200:
            return json.loads(response.content.decode())

    @staticmethod
    def get_content_list(response):
        """解析结果"""
        return response['subject_collection_items'], \
               response['total'], \
               response['subject_collection']['name']

    @staticmethod
    def print_info(content_list):
        """打印结果"""
        for content in content_list:
            print('剧名： ', content['title'])
            print('信息： ', content['info'], end='\n-----------------------\n')

    def save_content_list(self, content_list, name):
        """将结果存储"""
        with open(name + '.txt', 'a') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False) + '\n')

    def run(self):
        num = 0
        total = 1
        while num < total + 18:
            url = self.base_url.format(num)
            response = self.parse_url(url)
            content_list, total, name = self.get_content_list(response)
            self.print_info(content_list)
            self.save_content_list(content_list, name)
            num += 18


if __name__ == '__main__':
    d = DouBanSpider()
    d.run()
