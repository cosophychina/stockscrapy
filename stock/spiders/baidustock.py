# -*- coding: utf-8 -*-
import scrapy


class BaidustockSpider(scrapy.Spider):
    name = 'baidustock'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass
