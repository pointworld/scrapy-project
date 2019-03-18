# -*- coding: utf-8 -*-
import re

import scrapy


class Github2Spider(scrapy.Spider):
    name = 'github2'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/']

    def start_requests(self):
        # 登录后的 cookies
        cookies = 'yourcookies=yourcookies; yourcookies=yourcookies'
        # 将 cookies 字符串转换为字典的形式
        cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}

        for url in self.start_urls:
            yield scrapy.Request(
                url,
                cookies=cookies_dict,
                callback=self.after_login,
            )

    def parse(self, response):
        pass

    def after_login(self, response):
        match = re.findall(r'point', response.body.decode())
        print(match)
        print('*'*30)
