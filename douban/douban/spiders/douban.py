import scrapy
from ..items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['movie.douban.com']
    url = "https://movie.douban.com/top250?start="
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        item = DoubanItem()
        movies = response.xpath('//div[@class="info"]')
        for movie in movies:
            name = movie.xpath('.//span[@class="title"][1]/text()').extract()
            quote = movie.xpath('.//span[@class="inq"][1]/text()').extract()
            if len(name) and len(quote):
                item['name'] = name[0]
                item['quote'] = quote[0]
            yield item

        if self.offset < 225:
            self.offset += 25
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
