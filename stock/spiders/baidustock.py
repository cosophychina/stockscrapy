# -*- coding: utf-8 -*-
import scrapy
from stock.items import StockItem


class BaidustockSpider(scrapy.Spider):
    name = 'baidustock'
    #start_urls = ['http://quote.eastmoney.com/stocklist.html']
    start_urls = ['http://gupiao.baidu.com/stock/sz002292.html']

    def parse(self, response):
        sItem = StockItem()
        try:
	        stockInfo = response.css('.stock-bets')
	        betsname = stockInfo.css('.bets-name')
	        sItem['code'] = betsname.css('span::text').extract_first()
	        sItem['name'] = betsname.css('::text').extract_first()[1:-1].strip()
	        state = stockInfo.css('span')[1]
	        sItem['trade_date'] = state.re_first("\d{4}-\d{2}-\d{2}")
	        sItem['time'] = state.re_first("\d{2}:\d{2}:\d{2}")
	        sItem['close'] = stockInfo.css('._close::text').extract_first()
	        sItem['last'] = stockInfo.css('strong::text').extract_first()
	        valueList = stockInfo.css('dd')
	        sItem['open'] = valueList[0].css('::text').extract_first()
	        sItem['volume'] = valueList[1].css('::text').extract_first()[0:-2]
	        sItem['high'] = valueList[2].css('::text').extract_first()
	        sItem['limit_up'] = valueList[3].css('::text').extract_first()
	        sItem['turnover'] = valueList[5].css('::text').extract_first()[0:-1]
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
