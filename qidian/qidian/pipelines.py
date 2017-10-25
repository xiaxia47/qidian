# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from datetime import datetime
from datetime import date
from datetime import timedelta
from decimal import Decimal
import pymysql


class QidianPipeline(object):

    def process_item(self, item, spider):
        item['book_id'] = item['book_id']
        item['last_upload_date'] = self.process_upload_date(item['last_upload_date'])
        item['total_words'] = self.process_words_count(item['total_words'])
        item['click_count'] = self.process_count(item['click_count'])
        item['recommand_count'] = self.process_count(item['recommand_count'])
        item['rank_score'] = float(item['rank_score']) if item['rank_score'] >=0 else 0
        item['rank_ppl_involved'] = int(item['rank_ppl_involved'])
        return item

    def process_words_count(self, item):
        if '万' in item :
            item = Decimal(item.replace('万','')).quantize(Decimal("0.00")) * 10000
        return int(item)

    def process_count(self, item):
        if item is None:
            return None
        if '万' in item :
            item = Decimal(item[:-4]).quantize(Decimal("0.00")) * 10000
        else:
            item = Decimal(item[:-3]).quantize(Decimal("0.00"))
        return int(item.quantize(Decimal("0.00")))


    def process_upload_date(self, item):
        upload_date = None
        if '今天' in item:
            today = datetime.now()
            item = item.replace('今天','').replace('更新','')
            upload_date = datetime(year=today.year,month=today.month,
                                   day=today.day,hour=int(item[:2]),
                                   minute=int(item[-2:]))
        elif '昨日' in item:
            curdate = datetime.now() - timedelta(days=1) 
            item = item.replace('昨日','').replace('更新','')
            upload_date = datetime(year=curdate.year,month=curdate.month,
                                   day=curdate.day,hour=int(item[:2]),
                                   minute=int(item[-2:]))    
        else:
            return item

        return upload_date.strftime('%Y-%m-%d %H:%M:%S')


class DBWorkerPipeline(object):

    def __init__(self,dbparm):
        self.dbparm = dbparm

    @classmethod
    def from_crawler(cls,crawler):
        dbparm = crawler.settings.getdict('MYSQL_CONFIG')
        return cls(dbparm)
    
    def open_spider(self, spider):
        self.dbpool= adbapi.ConnectionPool('pymysql',**self.dbparm)

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        result = self.dbpool.runInteraction(self._do_insert, item)
        result.addErrback(self._handle_error, item, spider)

        return item

    def _do_insert(self,cursor, item):
        placeholder = ','.join(['%s'] * len(item))
        columns = ', '.join(item.keys())
        sql = "INSERT INTO {table} ({columns}) VALUES ({values});".format(
                            table='python.qidian',columns=columns,values=placeholder)
        cursor.execute(sql,list(item.values()))
        

    def _handle_error(self,failure, item, spider):
        print(failure)
