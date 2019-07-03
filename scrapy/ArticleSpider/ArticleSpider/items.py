# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

# from ..settings import SQL_DATETIME_FORMAT
from .settings import SQL_DATETIME_FORMAT


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()


def remove_splash(value):
    # 去掉工作城市的斜线
    return value.replace('/', '')


def handle_jobaddr(value):
    # 处理工作城市中的空格 \n等字符
    addr_list = value.split('\n')
    addr_list = [item.strip() for item in addr_list if item.strip() != '查看地图']
    return ''.join(addr_list)


class LagoyJobItemLoader(ItemLoader):
    # 自定义 itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 拉钩网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
            insert into lagou(title, url, url_object_id, salary, job_city, work_years, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_name,
            company_url, crawl_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            ON DUPLICATE KEY UPDATE salary=values(salary), job_desc=values(job_desc)
        '''

        params = (
            self['title'], self['url'], self['url_object_id'], self['salary'], self['job_city'],
            self['work_years'], self['degree_need'], self['job_type'], self['publish_time'],
            self['job_advantage'], self['job_desc'], self['job_addr'], self['company_name'],
            self['company_url'], self['crawl_time'].strftime(SQL_DATETIME_FORMAT)
        )
        return insert_sql, params
