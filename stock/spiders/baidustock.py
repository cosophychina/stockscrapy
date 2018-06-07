# -*- coding: utf-8 -*-
import scrapy
from stock.items import StockItem


class BaidustockSpider(scrapy.Spider):
    name = 'baidustock'
    #start_urls = ['http://quote.eastmoney.com/stocklist.html']
    # start_urls = ['http://gupiao.baidu.com/stock/sz002292.html',
    # 	'http://gupiao.baidu.com/stock/sz002786.html',
    # 	'http://gupiao.baidu.com/stock/sz000520.html',
    # 	'http://gupiao.baidu.com/stock/sh603901.html']
    start_urls = []
    base_url = "http://gupiao.baidu.com/stock/%s.html"

    def __init__(self, stocks = None, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	if stocks:
    		stocks = stocks.split(',')
    		for stk in stocks:
    			if not stk.startswith('s'):
    				if stk.startswith('6'):
    					stk = 'sh' + stk
    				else:
    					stk = 'sz' + stk
    			self.start_urls.append(self.base_url % stk)
    	

    def start_requests(self):
        stocks = self.settings.getlist('STOCK_LIST')
        if stocks:
        	for stk in stocks:
        		if stk.startswith('6'):
        			stk = 'sh' + stk
        		else:
        			stk = 'sz' + stk
        		yield scrapy.Request(self.base_url % stk, callback = self.parse)

        for url in self.start_urls:
        	yield scrapy.Request(url, callback = self.parse)

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
            txtState = state.re_first("\">(.*?) ")
            #print(txtState)
            sItem['close'] = stockInfo.css('._close::text').extract_first() if txtState.endswith('盘') else None #已收盘, 未开盘
            sItem['last'] = stockInfo.css('strong::text').extract_first()
            valueList = stockInfo.css('dd')
            sItem['open'] = valueList[0].css('::text').extract_first()
            sItem['volume'] = valueList[1].css('::text').extract_first()[0:-2]
            sItem['high'] = valueList[2].css('::text').extract_first()
            sItem['limit_up'] = valueList[3].css('::text').extract_first()
            sItem['turnover'] = valueList[5].css('::text').extract_first()[0:-1]
            sItem['pe'] = valueList[8].css('::text').extract_first()
            sItem['total_equity'] = valueList[10].css('::text').extract_first()[0:-1]
            sItem['preclose'] = valueList[11].css('::text').extract_first()
            sItem['turnover_rate'] = valueList[12].css('::text').extract_first()[0:-1]
            sItem['low'] = valueList[13].css('::text').extract_first()
            sItem['limit_down'] = valueList[14].css('::text').extract_first()[1:].lstrip()
            sItem['volume_ratio'] = valueList[17].css('::text').extract_first()[0:-1]
            sItem['flow_equity']= valueList[21].css('::text').extract_first()[0:-1]

        except:
        	pass

        yield sItem
