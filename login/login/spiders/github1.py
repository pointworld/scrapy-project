# -*- coding: utf-8 -*-
import re

import scrapy


class Github1Spider(scrapy.Spider):
    name = 'github1'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            # 会自动从 response 中寻找 from 表单
            response,
            formdata={'login': '', 'password': ''},
            callback=self.after_login,
        )

    def after_login(self, response):
        match = re.findall(r'point', response.body.decode())
        print(match)
        print('*'*30)
