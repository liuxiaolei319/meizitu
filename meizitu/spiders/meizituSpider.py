# coding:utf-8
import scrapy
from meizitu.items import MeizituItem
import re
import time
from scrapy.http import Request
import urlparse


class meizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ["meizitu.com"]
    start_urls = ["http://www.meizitu.com/tag/banluo_5_1.html"]

    def parse(self, response):
        urls = response.xpath('//div[@class="pic"]/a/@href').extract()  # 得取所朋妹子的urls
        for url in urls:
            yield Request(url=urlparse.urljoin(response.url, url), callback=self.parse_body)
            # yield Request(url='http://www.meizitu.com/a/752.html', callback=self.parse_body)
        index = response.xpath('//div[@id="wp_page_numbers"]/ul/li/a/text()').extract()  # 提取下一页的集合
        dd = u'下一页'
        if dd in index:
            new_url = response.xpath('//div[@id="wp_page_numbers"]/ul/li/a/@href').extract()[-2]
            yield Request(url=urlparse.urljoin(response.url, new_url), callback=self.parse)

    def parse_body(self, response):
        item = MeizituItem()
        name = response.xpath('//div[@class="metaRight"]/h2/a/text()').extract_first()  # 提取出名称
        urls = response.xpath('//div[@id="picture"]/p/img/@src').extract()
        item['name'] = name
        if urls:
            urls = response.xpath('//div[@id="picture"]/p/img/@src').extract()  # 提取图片链接
            item['image_urls'] = urls
        else:
            urls = response.xpath('//img[@class="scrollLoading"]/@src').extract()  # 提取图片链接
            item['image_urls'] = urls
        yield item
