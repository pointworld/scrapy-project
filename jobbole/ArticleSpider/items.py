# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import datetime

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader

from ArticleSpider.utils.common import get_md5


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + '-jobbole'


def date_convert(value):
    """
    将 create_date 字符串转换为 date 类型
    :param value: 提取出来的日期字符串
    :return: date 对象
    """

    try:
        create_date = re.findall(r'(\d+/\d+/\d+)', value)[0]
        create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def return_value(value):
    return value


def remove_comment_tags(value):
    """
    去除标签中提取的评论二字
    :param value:
    :return:
    """
    if '评论' in value:
        return ''
    else:
        return value


class ArticleItemLoader(ItemLoader):
    """
    自定义 ItemLoader 类
    重载 ItemLoader 类
    """

    # 只取 item 值列表中的第一个值
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    # 文章标题
    title = scrapy.Field(
        # MapCompose 会从左到右依次调用所传递的处理函数，处理 item 的值
        input_processor=MapCompose(lambda x: x + '-point', add_jobbole),
    )
    # 文章内容
    content = scrapy.Field()
    # 文章链接
    url = scrapy.Field()
    url_object_id = scrapy.Field(
        # 以 MD5 形式储存文章链接
        input_processor=MapCompose(get_md5)
    )
    # 列表页中每条数据左侧的小图链接
    front_image_url = scrapy.Field(
        # 覆盖默认的 default_output_processor 方法，这里以列表的形式返回
        # 因为在处理下载图片时，该字段的值需要是列表的形式
        output_processor=MapCompose(return_value)
    )
    # 列表页中每条数据左侧的小图存放路径
    front_image_path = scrapy.Field()
    # 文章标签
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        # 重载默认的 default_output_processor
        # 标签本身就是一个列表，在这里将该列表的值用逗号拼接为一个字符串
        output_processor=Join(',')
    )
    # 文章的创建日期
    create_date = scrapy.Field(
        # 将 create_date 字符串转换为 date 类型
        input_processor=MapCompose(date_convert)
    )
