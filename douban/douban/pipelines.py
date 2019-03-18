# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo

class DoubanPipeline(object):
    def __init__(self):
        host = '127.0.0.1'
        port = 27017
        dbname = 'Douban'
        sheetname = 'movie'

        client = pymongo.MongoClient(host=host, port=port)
        mdb = client[dbname]
        self.post = mdb[sheetname]

    def process_item(self, item, spider):
        self.post.insert_one(dict(item))
        return item

