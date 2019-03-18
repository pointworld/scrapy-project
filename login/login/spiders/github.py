import re

import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']

    def parse(self, response):
        commit = response.xpath('//div[@id="login"]//input[@name="commit"]/@value').extract_first()
        utf8 = response.xpath('//div[@id="login"]//input[@name="utf8"]/@value').extract_first()
        token = response.xpath('//div[@id="login"]//input[@name="authenticity_token"]/@value').extract_first()
        username = ''
        password = ''

        formdata = {
            'commit': commit,
            'utf8': utf8,
            'authenticity_token': token,
            'login': username,
            'password': password,
        }

        yield scrapy.FormRequest(
            url='https://github.com/session',
            formdata=formdata,
            callback=self.after_login,
        )

    def after_login(self, response):
        match = re.findall(r'point', response.body.decode())
        print(match)
        print('*'*50)
