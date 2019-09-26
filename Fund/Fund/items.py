# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#基金类
class FundItem(scrapy.Item):
    fundnumber = scrapy.Field() #基金代码
    fundname = scrapy.Field() #基金简称
    fundtype = scrapy.Field() #基金类型
    fundsize = scrapy.Field() #基金规模
    fundmanagement = scrapy.Field() #基金经理
    fundfoundingdate = scrapy.Field() #成立日
    fundmanager = scrapy.Field() #管理人
    fundranking = scrapy.Field() #基金评级
    fundservice = scrapy.Field() #手续费
#历史净值类
class HistoricalnetworthItem(scrapy.Item):
    networthdate = scrapy.Field() #净值日期
    unitnetworth = scrapy.Field() #单位净值
    accumulatednetworth = scrapy.Field() #累计净值
    dailygrowthrate = scrapy.Field() #日增长率
    purchasestatus = scrapy.Field() #申购状态
    redemptionstatus = scrapy.Field() #赎回状态
    bonus = scrapy.Field() #分红送配
    fundcode = scrapy.Field() #所属基金代码