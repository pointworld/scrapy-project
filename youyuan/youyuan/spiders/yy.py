# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors import LinkExtractor

# from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from youyuan.items import YouyuanItem


# class YySpider(CrawlSpider):
class YySpider(RedisCrawlSpider):
    name = 'yy'

    allowed_domains = ['youyuan.com']
    # 动态获取域范围
    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(YySpider, self).__init__(*args, *kwargs)

    # start_urls = ['http://www.youyuan.com/find/guangdong/mm18-25/advance-0-0-0-0-0-0-0/p1/']
    redis_key = 'yyspider:start_urls'

    # 第一级别匹配规则：广东省 18-25 岁女性列表页链接的匹配规则
    page_links = LinkExtractor(allow=(r'youyuan.com/find/guangdong/mm18-25/advance-0-0-0-0-0-0-0/p\d+/'))
    # 第二级别匹配规则：每个女性个人主页链接的匹配规则
    homepage_links = LinkExtractor(allow=(r'youyuan.com/\d+-profile'))

    rules = (
        Rule(page_links),
        Rule(homepage_links, callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = YouyuanItem()

        # 用户名
        item['username'] = self.get_username(response)
        # 年龄
        item['age'] = self.get_age(response)
        # 头像
        item['avatar'] = self.get_avatar(response)
        # 相册
        item['album'] = self.get_album(response)
        # 内心独白
        item['monologue'] = self.get_monologue(response)
        # 籍贯
        item['birthplace'] = self.get_birthplace(response)
        # 学历
        item['degree'] = self.get_degree(response)
        # 爱好
        item['hobby'] = self.get_hobby(response)
        # 个人主页
        item['homepage'] = response.url
        # 数据来源
        item['data_source'] = 'youyuan'

        return item

    def get_username(self, response):
        ret = response.xpath('//dl[@class="personal_cen"]//div[@class="main"]/strong/text()').extract()
        if len(ret):
            username = ret[0]
        else:
            username = 'NULL'
        return username.strip()

    def get_age(self, response):
        ret = response.xpath('//dl[@class="personal_cen"]//dd/p/text()').extract()
        if len(ret):
            age = re.split(r'\s+', ret[0].strip())[1]
        else:
            age = 'NULL'
        return age.strip()

    def get_avatar(self, response):
        ret = response.xpath('//dl[@class="personal_cen"]/dt/img/@src').extract()
        if len(ret):
            avatar = ret[0]
        else:
            avatar = 'NULL'
        return avatar.strip()

    def get_album(self, response):
        ret = response.xpath('//div[@class="ph_show"]/ul/li/a/img/@src').extract()
        if len(ret):
            ablum = ', '.join(ret)
        else:
            ablum = 'NULL'
        return ablum

    def get_monologue(self, response):
        ret = response.xpath('//div[@class="pre_data"]/ul/li/p/text()').extract()
        if len(ret):
            monologue = ret[0]
        else:
            monologue = 'NULL'
        return monologue.strip()

    def get_birthplace(self, response):
        ret = response.xpath('//div[@class="pre_data"]/ul/li[2]/div/ol[1]/li[1]/span/text()').extract()
        if len(ret):
            birthplace = ret[0]
        else:
            birthplace = 'NULL'
        return birthplace.strip()

    def get_degree(self, response):
        ret = response.xpath('//div[@class="pre_data"]/ul/li[2]/div/ol[1]/li[3]/span/text()').extract()
        if len(ret):
            degree = ret[0]
        else:
            degree = 'NULL'
        return degree.strip()

    def get_hobby(self, response):
       ret = response.xpath('//dl[@class="personal_cen"]//ol/li/text()').extract()
       if len(ret):
           hobby = ','.join(ret).replace(' ', '')
       else:
           hobby = 'NULL'
       return hobby.strip()
