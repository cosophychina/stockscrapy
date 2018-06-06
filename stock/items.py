# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    # define the fields for your item here like:
    code = scrapy.Field()
    name = scrapy.Field()
    trade_date = scrapy.Field()
    time = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    last = scrapy.Field()
    close = scrapy.Field()
    volume = scrapy.Field()
    turnover = scrapy.Field()
    turnover_rate = scrapy.Field()
    volume_ratio = scrapy.Field()
    limit_up = scrapy.Field()
    limit_down = scrapy.Field()
    preclose = scrapy.Field()
    flow_equity = scrapy.Field()
    total_equity = scrapy.Field()
    pe = scrapy.Field()

