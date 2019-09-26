# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import FundItem
from . import settings
from .items import HistoricalnetworthItem
import pymysql


class FundPipeline(object):
    fundlist = []
    historicalnetworthlist = []

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWORD,
                                    db=settings.MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()
        # 存入数据之前清空表：
        self.cursor.execute("truncate table fund")
        self.cursor.execute("truncate table historicalnetworth")
        self.conn.commit()

    def bulk_insert_to_mysql_fund(self, bulkdata):
        try:
            print("the length of the data-------", len(self.fundlist))
            sql = "insert into fund(fundnumber, fundname, fundtype, fundsize, fundmanagement, fundfoundingdate, fundmanager, fundranking, fundservice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            self.cursor.executemany(sql, bulkdata)
            self.conn.commit()
        except:
            self.conn.rollback()

    def bulk_insert_to_mysql_historicalnetworth(self, bulkdata):
        try:
            print("the length of the data-------", len(self.historicalnetworthlist))
            sql = "insert into historicalnetworth(networthdate,unitnetworth,accumulatednetworth,dailygrowthrate,purchasestatus,redemptionstatus,bonus,fundcode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
            self.cursor.executemany(sql, bulkdata)
            self.conn.commit()
        except:
            self.conn.rollback()

    def process_item(self, item, spider):
        if isinstance(item, FundItem):
            self.fundlist.append(
                [item['fundnumber'], item['fundname'], item['fundtype'], item['fundsize'], item['fundmanagement'],
                 item['fundfoundingdate'], item['fundmanager'], item['fundranking'], item['fundservice']])
        elif isinstance(item, HistoricalnetworthItem):
            self.historicalnetworthlist.append(
                [item['networthdate'], item['unitnetworth'], item['accumulatednetworth'], item['dailygrowthrate'],
                 item['purchasestatus'], item['redemptionstatus'], item['bonus'], item['fundcode']])
        if len(self.fundlist) == 1000:
            self.bulk_insert_to_mysql_fund(self.fundlist)
            # 清空缓冲区
            del self.fundlist[:]
        if len(self.historicalnetworthlist) == 1000:
            self.bulk_insert_to_mysql_historicalnetworth(self.historicalnetworthlist)
            # 清空缓冲区
            del self.historicalnetworthlist[:]
        return item

    def close_spider(self, spider):
        print("closing spider,last commit", len(self.fundlist))
        print("closing spider,last commit", len(self.historicalnetworthlist))
        self.bulk_insert_to_mysql_fund(self.fundlist)
        self.bulk_insert_to_mysql_historicalnetworth(self.historicalnetworthlist)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

