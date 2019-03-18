# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaPipeline(object):
    def process_item(self, item, spider):
        level3_url = item['level3_url']

        # 文件名为子链接 URL 中间部分，并将 / 替换为 _，保存为 .txt 格式
        filename = level3_url[7:-6].replace('/', '_')
        filename += '.txt'

        with open(item['level2_filename'] + '/' + filename, 'w') as f:
            f.write(item['content'])

        return item
