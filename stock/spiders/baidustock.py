# -*- coding: utf-8 -*-
import scrapy
from stock.items import StockItem


class BaidustockSpider(scrapy.Spider):
    name = 'baidustock'
    #start_urls = ['http://quote.eastmoney.com/stocklist.html']
    start_urls = ['http://gupiao.baidu.com/stock/sz002292.html',
    	'http://gupiao.baidu.com/stock/sz002786.html',
    	'http://gupiao.baidu.com/stock/sz000520.html',
    	'http://gupiao.baidu.com/stock/sh603901.html']

    def parse(self, response):
    	return self.parse_stock(response)
    	# for i in range(5):
    	# 	yield scrapy.Request(self.start_urls[0]+'?s='+str(i), callback = self.parse_stock)

    def parse_stock(self, response):
        sItem = StockItem()
        try:
	        stockInfo = response.css('.stock-bets')
	        betsname = stockInfo.css('.bets-name')
	        sItem['code'] = betsname.css('span::text').extract_first()
	        sItem['name'] = betsname.css('::text').extract_first()[1:-1].strip()
	        state = stockInfo.css('span')[1]
	        sItem['trade_date'] = state.re_first("\d{4}-\d{2}-\d{2}")
	        sItem['time'] = state.re_first("\d{2}:\d{2}:\d{2}")
	        sItem['close'] = float(stockInfo.css('._close::text').extract_first())
	        sItem['last'] = float(stockInfo.css('strong::text').extract_first())
	        valueList = stockInfo.css('dd')
	        sItem['open'] = float(valueList[0].css('::text').extract_first())
	        sItem['volume'] = float(valueList[1].css('::text').extract_first()[0:-2])
	        sItem['high'] = float(valueList[2].css('::text').extract_first())
	        sItem['limit_up'] = float(valueList[3].css('::text').extract_first())
	        sItem['turnover'] = float(valueList[5].css('::text').extract_first()[0:-1])
	        sItem['total_equity'] = float(valueList[10].css('::text').extract_first()[0:-1])
	        sItem['preclose'] = float(valueList[11].css('::text').extract_first())
	        sItem['turnover_rate'] = float(valueList[12].css('::text').extract_first()[0:-1])
	        sItem['low'] = float(valueList[13].css('::text').extract_first())
	        sItem['limit_down'] = float(valueList[14].css('::text').extract_first()[1:].lstrip())
	        sItem['volume_ratio'] = float(valueList[17].css('::text').extract_first()[0:-1])
	        sItem['flow_equity']= float(valueList[21].css('::text').extract_first()[0:-1])
        except:
        	pass

        yield sItem
