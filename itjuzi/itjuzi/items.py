# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # 公司 ID
    id = scrapy.Field()
    # 公司全名
    fullname = scrapy.Field()
    # 公司名
    name = scrapy.Field()
    # 公司简介
    brief = scrapy.Field()
    # 公司成立时间
    found_time = scrapy.Field()
    # 公司运行状况
    status = scrapy.Field()
    # 公司投资情况：包含获投时间、融资阶段、融资金额、投资公司
    investment_info = scrapy.Field()
    # 公司职员情况：包含职员姓名、职称、简介
    employee_info = scrapy.Field()
    # 公司产品信息：包含产品名称、产品类型、产品介绍
    product_info = scrapy.Field()
    # 公司口号
    slogan = scrapy.Field()
    # 分类
    category = scrapy.Field()
    # 子类
    sub_category = scrapy.Field()
    # 公司所在城市
    city = scrapy.Field()
    # 公司所在区域
    area = scrapy.Field()
    # 公司主页
    homepage = scrapy.Field()
    # 公司标签
    tags = scrapy.Field()

