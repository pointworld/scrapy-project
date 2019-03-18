import re
from copy import deepcopy

import scrapy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 大分类列表
        b_lists = response.xpath("//div[@class='menu-list']//div[@class='menu-item']")

        for b_type in b_lists:
            item = {}
            # 大分类类型
            item['b_type'] = b_type.xpath("./dl//h3/a/text()").extract_first()
            # 小分类列表
            s_lists = b_type.xpath("./dl/dd/a")
            for s_type in s_lists:
                # 小分类类型
                item['s_type'] = s_type.xpath("./text()").extract_first()
                # 小分类链接
                item['s_href'] = s_type.xpath("./@href").extract_first()
                if item['s_href'] != None:
                    yield scrapy.Request(
                        item['s_href'],
                        meta={"item": deepcopy(item)},
                        callback=self.parse_book_list,
                    )

    # 图书列表详情
    def parse_book_list(self, response):
        item = response.meta["item"]
        # 图书列表
        book_list = response.xpath("//div[@id='filter-results']//ul/li")
        for book in book_list:
            book_title = book.xpath("//div[@class='res-info']/p[2]/a/text()").extract_first().replace("\n", "")
            book_href = 'https:' + book.xpath(
                "//div[@class='res-img']/div[@class='img-block']/a/@href"
            ).extract_first()
            item['book_title'] = book_title
            item['book_href'] = book_href

            yield scrapy.Request(
                item['book_href'],
                meta={"item": deepcopy(item)},
                callback=self.parse_book_detail,
            )

        cur_page_re = r'currentPage = "(\d+)"'
        page_nums_re = r'pageNumbers = "(\d+)"'
        cur_page_match = re.findall(cur_page_re, response.body.decode())
        page_nums_match = re.findall(page_nums_re, response.body.decode())

        next_href = "https://list.suning.com/1-502320-{}-0-0-0-0-14-0-4.html"
        if cur_page_match and page_nums_match:
            # 当前页
            cur_page = int(cur_page_match[0])
            # 总页数
            page_nums = int(page_nums_match[0])
            if cur_page < page_nums:
                next_href = next_href.format(cur_page + 1)
                yield scrapy.Request(
                    next_href,
                    meta={'item': response.meta['item']},
                    callback=self.parse_book_list,
                )

    # 每本图书的详细情况
    def parse_book_detail(self, response):
        item = response.meta['item']
        item['book_img'] = 'https:' + response.xpath("//a[@id='bigImg']/img/@src").extract_first()
        item['book_writer'] = response.xpath("//div[@class='proinfo-main']/ul/li[1]/text()").extract_first()
        if item['book_writer']:
            item['book_writer'] = re.sub('\r*\t*\n*', '', item['book_writer']).replace(' ', '')
        # 将数据写入到 book.txt 文件
        with open("book.txt", 'a') as f:
            f.write(str(item))
            f.write("\n")
