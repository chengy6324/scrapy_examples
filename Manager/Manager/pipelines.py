# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from . import settings
from .items import ManagerItem
from .items import PersonItem
from .items import FundItem
from .items import WorkhistoryItem


class ManagerPipeline(object):
    fundlist = []
    managerlist = []
    personlist = []
    workhistorylist = []

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWORD,
                                    db=settings.MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()
        # 存入数据之前清空表：
        self.cursor.execute("truncate table fund")
        self.cursor.execute("truncate table manager")
        self.cursor.execute("truncate table person")
        self.cursor.execute("truncate table workhistory")
        self.conn.commit()

    def bulk_insert_to_mysql_fund(self, bulkdata):
        try:
            print("the length of the data-------", len(self.fundlist))
            sql = "insert into fund(fundname,fundnumber,foundingdate,filingdate,filingstage,fundtype,currency,managername,managementtype,trusteename,operationstate,fundupdatedate,specialtips,monthlyreport,semiannualreport,annualreport,quarterlyreport) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            self.cursor.executemany(sql, bulkdata)
            self.conn.commit()
        except:
            self.conn.rollback()

    def bulk_insert_to_mysql_manager(self, bulkdata):
        try:
            print("the length of the data-------", len(self.managerlist))
            sql = "insert into manager(integrityinformation,nameChinese,nameEnglish,registernumber,organizationalcode,registerdate,foundingdate,registeraddress,officeaddress,registeredcapital,paidincapital,natureofenterprise,capitalproportion,typeor,businesstype,employeesnumber,institutionalwebsite,investmentsuggestion,ismember,memberrepresentative,membershiptype,admissiondate,legalopinionstatus,nameoflawfirm,nameoflawyer,managerupdatedate,specialpromptinformation) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            self.cursor.executemany(sql, bulkdata)
            self.conn.commit()
        except:
            self.conn.rollback()

    def bulk_insert_to_mysql_person(self, bulkdata):
        try:
            print("the length of the data-------", len(self.personlist))
            sql = "insert into person(personname,job,fundqualification,managernumber) VALUES (%s,%s,%s,%s);"
            self.cursor.executemany(sql, bulkdata)
            self.conn.commit()
        except:
            self.conn.rollback()

    def bulk_insert_to_mysql_workhistory(self, bulkdata):
        try:
            print("the length of the data-------", len(self.workhistorylist))
            sql = "insert into workhistory(intervall,tenureunit,department,jobb,personname) VALUES (%s,%s,%s,%s,%s);"
            self.cursor.executemany(sql, bulkdata)
            self.conn.commit()
        except:
            self.conn.rollback()

    def process_item(self, item, spider):
        if isinstance(item, ManagerItem):
            self.managerlist.append(
                [item['integrityinformation'], item['nameChinese'], item['nameEnglish'], item['registernumber'],
                 item['organizationalcode'], item['registerdate'], item['foundingdate'], item['registeraddress'],
                 item['officeaddress'], item['registeredcapital'], item['paidincapital'], item['natureofenterprise'],
                 item['capitalproportion'], item['typeor'], item['businesstype'], item['employeesnumber'],
                 item['institutionalwebsite'], item['investmentsuggestion'], item['ismember'],
                 item['memberrepresentative'], item['membershiptype'], item['admissiondate'],
                 item['legalopinionstatus'], item['nameoflawfirm'], item['nameoflawyer'], item['managerupdatedate'],
                 item['specialpromptinformation']])
        elif isinstance(item, PersonItem):
            self.personlist.append([item['personname'], item['job'], item['fundqualification'], item['managernumber']])
        elif isinstance(item, FundItem):
            self.fundlist.append(
                [item['fundname'], item['fundnumber'], item['foundingdate'], item['filingdate'], item['filingstage'],
                 item['fundtype'], item['currency'], item['managername'], item['managementtype'], item['trusteename'],
                 item['operationstate'], item['fundupdatedate'], item['specialtips'], item['monthlyreport'],
                 item['semiannualreport'], item['annualreport'], item['quarterlyreport']])
        elif isinstance(item, WorkhistoryItem):
            self.workhistorylist.append(
                [item['intervall'], item['tenureunit'], item['department'], item['jobb'], item['personname']])
        if len(self.fundlist) == 1000:
            self.bulk_insert_to_mysql_fund(self.fundlist)
            # 清空缓冲区
            del self.fundlist[:]
        if len(self.managerlist) == 1000:
            self.bulk_insert_to_mysql_manager(self.managerlist)
            # 清空缓冲区
            del self.managerlist[:]
        if len(self.personlist) == 1000:
            self.bulk_insert_to_mysql_person(self.personlist)
            # 清空缓冲区
            del self.personlist[:]
        if len(self.workhistorylist) == 1000:
            self.bulk_insert_to_mysql_workhistory(self.workhistorylist)
            # 清空缓冲区
            del self.workhistorylist[:]
        return item

    # 关闭时保存最后未满的list
    def close_spider(self, spider):
        print("closing spider,last commit", len(self.fundlist))
        print("closing spider,last commit", len(self.managerlist))
        print("closing spider,last commit", len(self.personlist))
        print("closing spider,last commit", len(self.workhistorylist))
        self.bulk_insert_to_mysql_fund(self.fundlist)
        self.bulk_insert_to_mysql_manager(self.managerlist)
        self.bulk_insert_to_mysql_person(self.personlist)
        self.bulk_insert_to_mysql_workhistory(self.workhistorylist)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
