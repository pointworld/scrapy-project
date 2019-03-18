# -*- coding: utf-8 -*-
import scrapy
from ..items import TencentItem


class TencentpositionSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    url = 'https://hr.tencent.com/position.php?&start=0'
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        for each in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
            # 初始化模型对象
            item = TencentItem()

            # 职位名
            item['position_name'] = each.xpath('./td[1]/a/text()').extract()[0]
            # 详情链接
            item['position_link'] = each.xpath('./td[1]/a/@href').extract()[0]
            # 职位类别
            item['position_type'] = each.xpath('./td[2]/text()').extract()[0] if each.xpath('./td[2]/text()') else ''
            # 招聘人数
            item['recruit_num'] = each.xpath('./td[3]/text()').extract()[0]
            # 工作地点
            item['work_location'] = each.xpath('./td[4]/text()').extract()[0]
            # 发布时间
            item['pub_time'] = each.xpath('./td[5]/text()').extract()[0]

            yield item

        if self.offset < 1680:
            self.offset += 10

        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)


