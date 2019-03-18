# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YouyuanItem(scrapy.Item):
    # 用户名
    username = scrapy.Field()
    # 年龄
    age = scrapy.Field()
    # 头像
    avatar = scrapy.Field()
    # 相册
    album = scrapy.Field()
    # 内心独白
    monologue = scrapy.Field()
    # 籍贯
    birthplace = scrapy.Field()
    # 学历
    degree = scrapy.Field()
    # 爱好
    hobby = scrapy.Field()
    # 个人主页
    homepage = scrapy.Field()
    # 数据来源
    data_source = scrapy.Field()