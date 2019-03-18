# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

import pymysql
import pymysql.cursors
# adbapi 即异步数据库的 API，将 MySQL 的操作变成异步操作
from twisted.enterprise import adbapi


class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    """
    定制 ImagesPipeline 类，实现将下载到的图片路径与相应的 item 字段做映射
    """

    def item_completed(self, results, item, info):
        """
        重载 ImagesPipeline 类的 item_completed 方法
        :param results:
        :param item:
        :param info:
        :return:
        """

        if 'front_image_url' in item:
            for ok, value in results:
                image_file_path = value['path']
                item['front_image_path'] = image_file_path

        return item


class JSONWithEncodingPipeline:
    """
    自定义 JSON 文件的导出
    """

    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        """
        该方法必须实现
        :param item:
        :param spider:
        :return:
        """
        json_text = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(json_text)

        return item

    def close_spider(self, spider):
        """
        当 spider 被关闭的时候，该方法就会被调用
        :param spider:
        :return:
        """
        self.file.close()


class JsonExporterPipeline:
    """
    调用 scrapy 提供的 JsonItemExporter 类导出 JSON 文件
    """

    def __init__(self):
        self.file = open('article_export.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class MySQLPipeline:
    """
    将数据插入 MySQL 的传统做法，同步方式
    因为 Spider 解析的速度远大于数据入库的速度，所以这种方式会经常发生 IO 阻塞
    """
    def __init__(self):
        self.mysql_cli = pymysql.connect(
            host='172.16.195.195',
            port=3306,
            user='root',
            password='mysql',
            db='article_spider'
        )

    def process_item(self, item, spider):
        with self.mysql_cli.cursor() as cursor:
            # 创建 MySQL 游标对象，可以执行 MySQL 语句
            sql = """
                insert into jobbole_article (`title`) values (%s)"""
            values = (item['title'][0])

            cursor.execute(sql, values)

            # 提交事务
            self.mysql_cli.commit()


class MySQLTwistedPipeline:
    """
    通过异步的方式将数据插入 MySQL
    twisted 提供了一个工具 - 连接池：可以异步插入数据到数据库
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        自定义组件或扩展很有用的方法，该方法名固定
        该方法会被 Scrapy 调用
        :param settings: 即配置文件，会被 Scrapy 读取
        :return:
        """
        db_params = dict(
            host = settings['MYSQL_HOST'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            db = settings['MYSQL_DBNAME'],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode=True
        )

        # 创建一个数据库连接池对象，这个连接池中可以包含多个 connect 连接对象
        # 参数1：操作数据库的包名
        # 参数2：链接数据库的参数
        dbpool = adbapi.ConnectionPool('pymysql', **db_params)

        # 初始化这个类的对象并返回
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用 twisted 将 MySQL 插入变成异步执行
        在连接池中，开始执行数据的多线程写入操作
        :param item:
        :param spider:
        :return:
        """

        # 参数1：在线程中被执行的 sql 语句
        # 参数2：要保存的数据
        result = self.dbpool.runInteraction(self.do_insert, item)
        # 给 result 绑定一个回调函数，用于监听错误信息
        result.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):

            # 创建 MySQL 游标对象，可以执行 MySQL 语句
            sql = """
                insert into jobbole_article
                (`title`, `create_date`, `content`, `url`, `url_object_id`, `front_image_url`, `front_image_path`, `tags`) 
                values (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                item['title'],
                item['create_date'],
                item['content'],
                item['url'],
                item['url_object_id'],
                item['front_image_url'][0] if item['front_image_url'] else '',
                item['front_image_path'] if item['front_image_path'] else '',
                item['tags']
            )

            cursor.execute(sql, values)

    def handle_error(self, failure, item, spider):
        """
        处理异步插入的异常
        :param failure: 错误信息
        :param item:
        :param spider:
        :return:
        """
        print('*'*50)
        print(failure)
