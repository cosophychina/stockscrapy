# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StockPipeline(object):
    def process_item(self, item, spider):
        return item

class StockMysqlPipeline():
	"""docstring for StockMysqlPipelime"""
	def process_item(self, item, spider):
		sqlinfo = ""
		sqlquotes = ""
		sqldailys = ""
		print(item)
		# super().process_item(item, spider, [sqlinfo, sqlquotes, sqldailys])


class MysqlPipeline(object):
    ''' MySQL数据处理类 '''
    def __init__(self,host,database,user,password,port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.db=None
        self.cursor=None

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
        self.db = pymysql.connect(self.host,self.user,self.password,self.database,charset='utf8',port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider, sqlList = []):
        try:
	        for sql in sqlList:
	        	self.cursor.execute(sql)
	        self.db.commit()
        except:
        	self.db.rollback()
        
        return item

    def close_spider(self,spider):
        self.db.close()