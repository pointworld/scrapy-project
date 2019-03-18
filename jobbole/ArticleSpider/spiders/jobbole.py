from urllib import parse

import scrapy
from scrapy.loader import ItemLoader

from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader


class JobboleSpider(scrapy.Spider):
    # 爬虫名
    name = 'jobbole'
    # 允许爬虫的作用范围
    allowed_domains = ['blog.jobbole.com']
    # 爬虫的起始 URL
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取当前文章列表页中的文章 URL，交给 scrapy 下载，由 self.parse_content 方法进行解析
        2. 获取下一页的 URL，交给 scrapy 进行下载，由 self.parse 方法继续解析
        :param response:
        :return:
        """

        # 获取当前列表页中所有的文章节点
        post_nodes = response.css('#archive .post-thumb a')
        for post_node in post_nodes:
            # 遍历当前列表页中所有文章节点，提取出每个文章详情的 URL
            # 交给 scrapy 下载，由 self.parse_content 方法进行解析

            # 列表页中每条文章数据左侧的小图 URL
            front_image_url = post_node.css('img::attr(src)').extract_first()
            # 列表页中每条文章数据的详情 URL
            article_url = post_node.css('::attr(href)').extract_first()
            # 处理可能出现相对 URL 的情况
            front_image_url = parse.urljoin(response.url, front_image_url)
            article_url = parse.urljoin(response.url, article_url)


            yield scrapy.Request(
                url=article_url,
                # meta 的作用是传递数据给回调函数中的 response
                meta={'front_image_url': front_image_url},
                callback=self.parse_content
            )

        # 获取下一个列表页的链接，交给 scrapy 下载，由 self.parse 方法解析
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            # 如果存在下一页 URL，就交给 self.parse 继续解析
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_content(self, response):
        front_image_url = response.meta.get('front_image_url', '')

        # 通过 ItemLoader 加载 Item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)

        item_loader.add_css('title', 'h1::text')
        item_loader.add_css('content', 'div.entry')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', response.url)
        item_loader.add_value('front_image_url', front_image_url)
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")

        # 调用原生 ItemLoader 的 load_item 方法对规则进行解析并生成 item 对象时
        # 存在两个问题：
        # 1. item 的所有值都是一个 list
        # 2. 不能做过滤处理
        # 要解决该问题，需要定制 Item, ItemLoader
        item = item_loader.load_item()

        # yield item 到 pipeline
        yield item
