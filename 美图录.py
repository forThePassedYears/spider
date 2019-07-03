# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree
from urllib.parse import urljoin
from fake_useragent import UserAgent
import threadpool


class Picture(object):

    def __init__(self, start_url, path):
        self.start_url = start_url
        self.path = path
        self.ua = UserAgent()

    def get_response(self, url):
        # 解析url 获取响应
        response = requests.get(url, headers={'User-Agent': self.ua.random})
        html = etree.HTML(response.content.decode())
        return html

    def get_pages(self, html):
        # 获取当前分类每页的URL
        all_nums = html.xpath('//div[@id="pages"]/a/text()')[0]
        page = re.compile('\d+', re.S).findall(all_nums)[0]
        x, y = divmod(int(page), 60)
        pages = x + 1 if y > 0 else x
        return ['https://www.meitulu.com/t/heisi/' + str(x) + '.html' 
            for x in range(2, (pages + 1))]

    def parse_url(self, html):
        # 获取每页的 item 地址, 返回每页的 item 地址列表
        urls = html.xpath('//ul[@class="img"]/li/a/@href')
        return urls

    def get_img_list(self, url):
        s = requests.session()
        next_page = url
        while True:
            print('---------------------------' +
                  next_page + '-----------------------------')
            response = s.get(next_page, headers={'User-Agent': self.ua.random})
            html = etree.HTML(response.content.decode())
            next_page = urljoin(next_page, html.xpath(
                '//div[@id="pages"]/a/@href')[-1])
            current_page = html.xpath('//div[@id="pages"]/span/text()')[-1]
            next_nums = next_page.split('_')[-1]
            next_num = re.compile('\d+').findall(next_nums)[0]
            img_list = html.xpath('//img[@class="content_img"]/@src')
            for img in img_list:
                print('\t\t\t' + img)
                i = s.get(img, headers={
                          'User-Agent': self.ua.random, 'Referer': response.url}).content
                filename = img.split('/')[-2] + img.split('/')[-1]
                with open(self.path + filename, 'wb') as f:
                    f.write(i)
            if int(next_num) == int(current_page):
                break

    def run(self):
        first_page = self.get_response(self.start_url)
        pages = self.get_pages(first_page)
        items = self.parse_url(first_page)
        for page in pages:
            # 获取所有的item URL
            res = self.get_response(page)
            items += self.parse_url(res)
        pool = threadpool.ThreadPool(5)
        tasks = threadpool.makeRequests(self.get_img_list, items)
        [pool.putRequest(task) for task in tasks]
        pool.wait()


if __name__ == '__main__':
    save_path = '/media/wxl/f0a47203-99ca-4696-a90f-d684ca5e245a/images/'
    start_url = 'https://www.meitulu.com/t/heisi/'
    p = Picture(start_url, save_path)
    p.run()
