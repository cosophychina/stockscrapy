# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class StockPipeline(object):
    def process_item(self, item, spider):
        return item

class StockConsolePipeline(object):
	"""docstring for StockMysqlPipelime"""
	def process_item(self, item, spider):
		print(item)
		

class MysqlPipeline(object):
    ''' Base MysqlPipeline to store stock data. '''
    def __init__(self,host,database,user,password,port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.db=None

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get("MYSQL_HOST"),
            database = crawler.settings.get("MYSQL_DATABASE"),
            user = crawler.settings.get("MYSQL_USER"),
            password = crawler.settings.get("MYSQL_PASS"),
            port = crawler.settings.get("MYSQL_PORT")
        )

    def open_spider(self,spider):
        try:
            self.db = pymysql.connect(self.host,self.user,self.password,self.database,charset='utf8',port=self.port)
        except:
            pass

    def process_item(self, item, spider, sqlList = [], oneTransactionSqls = []):
        if self.db:
            if len(sqlList) > 0:
                #not a transaction's sqls
                with self.db.cursor() as cursor:
                    for sql in sqlList:
                        print(sql)
                        try:
                            cursor.execute(sql)
                        except:
                            continue #if error, continue next.
                self.db.commit()

            if len(oneTransactionSqls) > 0:
                #execute all opers within one transaction
                with self.db.cursor() as cursor:             
                    try:
                        for sql in oneTransactionSqls:
                            cursor.execute(sql)
                    except:
                        self.db.rollback() #if error, rollback all.

                self.db.commit()      
        
        return item

    def close_spider(self,spider):
        if self.db:
            self.db.close()

''' transform string to float type '''
def getFloat(s, default):
    try:
        return float(s)
    except:
        return default

"""
pipeline to preproc the item's fields before storing
"""
class StockPreProcPipeline(object):
    #process
    def process_item(self, item, spider):
        
        item['code'] = item.get('code', None)
        item['name'] = item.get('name', '')
        item['trade_date'] = item.get('trade_date', '')
        item['time'] = item.get('time', '')

        item['open'] = getFloat(item['open'], 'NULL')
        item['high'] = getFloat(item['high'], 'NULL')
        item['low'] = getFloat(item['low'], 'NULL')
        item['close'] = getFloat(item['close'], 'NULL')
        item['pe'] = getFloat(item['pe'], 'NULL')
        item['volume'] = getFloat(item['volume'], 'NULL')
        item['last'] = getFloat(item['last'], 'NULL')
        item['turnover'] = getFloat(item['turnover'], 'NULL')
        item['turnover_rate'] = getFloat(item['turnover_rate'], 'NULL')
        item['volume_ratio'] = getFloat(item['volume_ratio'], 'NULL')
        item['limit_up'] = getFloat(item['limit_up'], 'NULL')
        item['limit_down'] = getFloat(item['limit_down'], 'NULL')
        item['preclose'] = getFloat(item['preclose'], 'NULL')
        item['flow_equity'] = getFloat(item['flow_equity'], 'NULL')
        item['total_equity'] = getFloat(item['total_equity'], 'NULL')

        if item['code']:
            if(item['code'][0] == '6'):
                item['market'] = 'SH'
            else:
                item['market'] = 'SZ'

        return item

class StockMysqlPipeline(MysqlPipeline):
    """store stock data to mysql database, including StockInfo, StockQuotes and StockDailys."""
    """StockQuotes and StockDailys data to be updated at each crawl."""
    def process_item(self, item, spider):
        if not (item['code'] and item['code'].isdigit()):
            return item

        sqlinfo = "INSERT INTO StockInfo(code, name, market, symbol) VALUES('%s','%s','%s','%s')" \
                        % (item['code'], item['name'], item['market'], item['code'] + '.' + item['market'])

        sqlquotes = "INSERT INTO StockQuotes(code,trade_date,time,open,high,low,last,close,volume," + \
                    "turnover,turnover_rate,volume_ratio,limit_up,limit_down,preclose,flow_equity,total_equity,pe) " + \
                    "VALUES('%s','%s','%s',{},{},{},%.2f,{},%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,{}) ON DUPLICATE KEY UPDATE " + \
                    "trade_date=VALUES(trade_date),time=VALUES(time),open=VALUES(open),high=VALUES(high),low=VALUES(low),last=VALUES(last)," + \
                    "close=VALUES(close),volume=VALUES(volume),turnover=VALUES(turnover),turnover_rate=VALUES(turnover_rate)," + \
                    "volume_ratio=VALUES(volume_ratio),limit_up=VALUES(limit_up),limit_down=VALUES(limit_down),preclose=VALUES(preclose)," + \
                    "flow_equity=VALUES(flow_equity),total_equity=VALUES(total_equity),pe=VALUES(pe)"
        #if has value, format normally; else format 'NULL'
        sqlquotes = sqlquotes.format(('%.2f' if item['open'] != 'NULL' else '%s'),('%.2f' if item['high'] != 'NULL' else '%s'),
                                        ('%.2f' if item['low'] != 'NULL' else '%s'),('%.2f' if item['close'] != 'NULL' else '%s'),
                                        ('%.2f' if item['pe'] != 'NULL' else '%s')) 


        sqldailys = "INSERT INTO StockDailys(code,open,high,low,close,volume,turnover,pe,total_equity,trade_date) " + \
                    "VALUES('%s',{},{},{},{},%.2f,%.2f,{},%.2f,'%s') " + \
                    "ON DUPLICATE KEY UPDATE open=VALUES(open),high=VALUES(high),low=VALUES(low),close=VALUES(close),volume=VALUES(volume)," + \
                    "turnover=VALUES(turnover),pe=VALUES(pe),total_equity=VALUES(total_equity)" 
        sqldailys = sqldailys.format(('%.2f' if item['open'] != 'NULL' else '%s'),('%.2f' if item['high'] != 'NULL' else '%s'),
                                        ('%.2f' if item['low'] != 'NULL' else '%s'),('%.2f' if item['close'] != 'NULL' else '%s'),
                                        ('%.2f' if item['pe'] != 'NULL' else '%s'))  


        sqlquotes = sqlquotes % (item['code'], item['trade_date'], item['time'], item['open'], item['high'], item['low'], item['last'], 
                    item['close'], item['volume'], item['turnover'], item['turnover_rate'], item['volume_ratio'], item['limit_up'], 
                    item['limit_down'], item['preclose'], item['flow_equity'], item['total_equity'], item['pe'])              
        sqldailys = sqldailys % (item['code'], item['open'], item['high'], item['low'], item['close'], item['volume'], 
                    item['turnover'], item['pe'], item['total_equity'], item['trade_date'])
        
        super().process_item(item, spider, [sqlinfo, sqlquotes, sqldailys])