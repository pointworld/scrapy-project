import os

import scrapy
from ..items import SinaItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []

        # 所有大类的 URL 和标题
        level1_titles = response.xpath('//div[@id="tab01"]//h3/a/text()').extract()
        level1_urls = response.xpath('//div[@id="tab01"]//h3/a/@href').extract()

        # 所有小类的 URL 和标题
        level2_titles = response.xpath('//div[@id="tab01"]//li/a/text()').extract()
        level2_urls = response.xpath('//div[@id="tab01"]//li/a/@href').extract()

        # 爬取所有大类
        for i in range(0, len(level1_titles)):
            # 指定大类目录的路径和目录名
            level1_filename = './Data/' + level1_titles[i]

            # 如果目录不存在，则创建目录
            if (not os.path.exists(level1_filename)):
                os.makedirs(level1_filename)

            item = SinaItem()

            # 保存大类的 title 和 urls
            item['level1_title'] = level1_titles[i]
            item['level1_url'] = level1_urls[i]

            # 爬取所有小类
            for j in range(0, len(level2_titles)):
                # 检查小类的 URL 是否以同类别大类的 URL 开头，如果是返回 True
                # (sports.sina.com.cn 和 sports.sina.com.cn/nba)
                is_belong = level2_urls[j].startswith(item['level1_url'])

                # 如果属于本大类，将存储目录放在本大类目录下
                if (is_belong):
                    level2_filename = level1_filename + '/' + level2_titles[j]

                    # 如果目录不存在，则创建目录
                    if (not os.path.exists(level2_filename)):
                        os.makedirs(level2_filename)

                    # 存储小类 URL、title 和 filename 字段数据
                    item['level2_title'] = level2_titles[j]
                    item['level2_url'] = level2_urls[j]
                    item['level2_filename'] = level2_filename

                    items.append(item)

            # 发送每个小类 URL 的 Request 请求，得到 Response
            # 将 Response 和 meta 数据 一同交给回调函数 second_parse 处理
            for item in items:
                yield scrapy.Request(url=item['level2_url'], meta={'meta_1': item}, callback=self.second_parse)

    # 对于返回的小类的 URL，再进行递归请求
    def second_parse(self, response):
        # 提取每次 Response 的 meta 数据
        meta_1 = response.meta['meta_1']

        # 取出小类里所有的子链接
        level3_urls = response.xpath('//a/@href').extract()

        items = []
        for i in range(0, len(level3_urls)):
            # 检查每个链接是否以大类 URL 开头、以 .shtml 结尾，如果是，返回 True
            is_belong = level3_urls[i].endswith('.shtml') and level3_urls[i].startswith(meta_1['level1_url'])

            # 如果属于本大类，获取字段值放在同一个 item 下便于传输
            if (is_belong):
                item = SinaItem()
                item['level1_title'] = meta_1['level1_title']
                item['level1_url'] = meta_1['level1_url']
                item['level2_title'] = meta_1['level2_title']
                item['level2_url'] = meta_1['level2_url']
                item['level2_filename'] = meta_1['level2_filename']
                item['level3_url'] = level3_urls[i]
                items.append(item)

        # 发送每个小类下的子链接 URL 的 Request 请求，得到 Response
        # 将 Response 和 meta 数据交给回调函数 detail_parse 处理
        for item in items:
            yield scrapy.Request(url=item['level3_url'], meta={'meta_2': item}, callback=self.detail_parse)

    # 数据解析方法，获取文章标题和内容
    def detail_parse(self, response):
        item = response.meta['meta_2']
        content = ''
        head = response.xpath('//h1/text()')
        content_list = response.xpath('//div[@id="artibody"]/p/text()').extract()

        # 将 p 标签里的文本内容合并到一起
        for p in content_list:
            content += p

        item['head'] = head
        item['content'] = content

        yield item
