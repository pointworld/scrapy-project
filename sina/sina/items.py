# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # 大类的标题和 URL
    level1_title = scrapy.Field()
    level1_url = scrapy.Field()

    # 小类的标题和 URL
    level2_title = scrapy.Field()
    level2_url = scrapy.Field()
    # 小类目录存储路径
    level2_filename = scrapy.Field()

    # 小类下的子链接
    level3_url = scrapy.Field()

    # 文章标题和内容
    head = scrapy.Field()
    content = scrapy.Field()
