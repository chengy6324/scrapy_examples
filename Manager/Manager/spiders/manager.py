# -*- coding: utf-8 -*-

import scrapy
from ..items import ManagerItem
from ..items import PersonItem
from ..items import WorkhistoryItem
from ..items import FundItem
import json
from datetime import datetime


class ManagerSpider(scrapy.Spider):
    name = 'manager'  # 爬虫名称
    headers = {  # 请求头
        "Host": "gs.amac.org.cn",
        "Accept": "application/json,text/javascript, */*; q=0.01",
        "Origin": "http://gs.amac.org.cn",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        "Content-Type": "application/json",
        "Referer": 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html',
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    # 基金管理人页面url地址控制翻页
    urls = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.03238375864053089&page='
    urls_tail = '&size=100'
    # 基金管理人内页url地址
    base_url2 = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/'
    # 基金页面内页url地址
    base_url3 = 'http://gs.amac.org.cn/amac-infodisc/res/pof/'

    # 发送post请求得到response
    def start_requests(self):
        yield scrapy.Request(
            self.urls + str(0) + self.urls_tail,
            method="POST",
            headers=self.headers,
            body="{}",
            callback=self.parse,
            dont_filter=True,
        )

    # 进入基金管理人页面
    def parse(self, response):
        response = json.loads(response.body_as_unicode())
        for num in range(len(response.get('content'))):
            url2 = self.base_url2 + response.get('content')[num].get('url')
            yield scrapy.Request(url2, callback=self.info_parse)  # 请求访问基金管理人内页

        num_page = int(response.get('number'))  # 得到基金管理人页面当前页码
        num_page += 1

        max_page = int(response.get('totalPages'))  # 基金管理人页面总页数

        if num_page < max_page:  # 访问基金管理人页面的所有页码
            yield scrapy.Request(
                self.urls + str(num_page) + self.urls_tail,
                method="POST",
                headers=self.headers,
                body="{}",
                callback=self.parse,
                dont_filter=True,
            )

    # 保存基金管理人内页信息
    def info_parse(self, response):
        item_Manager = ManagerItem()
        item_Manager['integrityinformation'] = response.xpath('//tr[contains(td[1]/text(),"机构诚信信息")]').xpath(
            'td[2]/table/text()').extract_first()
        item_Manager['nameChinese'] = response.xpath('//tr[contains(td[1]/text(),"基金管理人全称(中文)")]').xpath(
            'td[2]/div[@id="complaint1"]/text()').extract_first()[:-5]
        item_Manager['nameEnglish'] = response.xpath('//tr[contains(td[1]/text(),"基金管理人全称(英文)")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['registernumber'] = response.xpath('//tr[contains(td[1]/text(),"登记编号")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['organizationalcode'] = response.xpath('//tr[contains(td[1]/text(),"组织机构代码")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['registerdate'] = response.xpath('//tr[contains(td[1]/text(),"登记时间")]').xpath(
            'td[2]/text()').extract_first().replace(' ', '')
        item_Manager['foundingdate'] = response.xpath('//tr[contains(td[3]/text(),"成立时间")]').xpath(
            'td[4]/text()').extract_first().replace(' ', '')
        item_Manager['registeraddress'] = response.xpath('//tr[contains(td[1]/text(),"注册地址")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['officeaddress'] = response.xpath('//tr[contains(td[1]/text(),"办公地址")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['registeredcapital'] = response.xpath('//tr[contains(td[1]/text(),"注册资本(万元)(人民币)")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['paidincapital'] = response.xpath('//tr[contains(td[3]/text(),"实缴资本(万元)(人民币)")]').xpath(
            'td[4]/text()').extract_first()
        item_Manager['natureofenterprise'] = response.xpath('//tr[contains(td[1]/text(),"企业性质")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['capitalproportion'] = response.xpath('//tr[contains(td[3]/text(),"注册资本实缴比例")]').xpath(
            'td[4]/text()').extract_first().replace(' ', '')
        item_Manager['typeor'] = response.xpath('//tr[contains(td[1]/text(),"机构类型")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['businesstype'] = response.xpath('//tr[contains(td[3]/text(),"业务类型")]').xpath(
            'td[4]/text()').extract_first()
        item_Manager['employeesnumber'] = response.xpath('//tr[contains(td[1]/text(),"员工人数")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['institutionalwebsite'] = response.xpath('//tr[contains(td[3]/text(),"机构网址")]').xpath(
            'td[4]/text()').extract_first()
        item_Manager['investmentsuggestion'] = response.xpath(
            '//tr[contains(td[1]/text(),"是否为符合提供投资建议条件的第三方机构")]').xpath('td[2]/text()').extract_first()
        item_Manager['ismember'] = response.xpath('//tr[contains(td[1]/text(),"是否为会员")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['memberrepresentative'] = response.xpath('//tr[contains(td[3]/text(),"会员代表")]').xpath(
            'td[4]/text()').extract_first()
        item_Manager['membershiptype'] = response.xpath('//tr[contains(td[1]/text(),"当前会员类型")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['admissiondate'] = response.xpath('//tr[contains(td[3]/text(),"入会时间")]').xpath(
            'td[4]/text()').extract_first()
        item_Manager['legalopinionstatus'] = response.xpath('//tr[contains(td[1]/text(),"法律意见书状态")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['nameoflawfirm'] = response.xpath('//tr[contains(td[1]/text(),"律师事务所名称")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['nameoflawyer'] = response.xpath('//tr[contains(td[1]/text(),"律师姓名")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['managerupdatedate'] = response.xpath('//tr[contains(td[1]/text(),"机构信息最后更新时间")]').xpath(
            'td[2]/text()').extract_first()
        item_Manager['specialpromptinformation'] = response.xpath('//tr[contains(td[1]/text(),"特别提示信息")]').xpath(
            'td[2]/text()').extract_first()
        yield item_Manager

        links_person = response.xpath('//tr[contains(td[1]/text(),"高管情况")]').xpath('td[2]/table/tbody/tr')
        for index, link in enumerate(links_person):
            item_Person = PersonItem()
            item_Person['personname'] = link.xpath('td[1]/text()').extract_first()
            item_Person['job'] = link.xpath('td[2]/text()').extract_first()
            item_Person['fundqualification'] = link.xpath('td[3]/text()').extract_first().replace(' ', '')
            item_Person['managernumber'] = response.xpath('//tr[contains(td[1]/text(),"登记编号")]').xpath(
                'td[2]/text()').extract_first()
            yield item_Person

        links_workhistory = response.xpath('//tr[contains(td[1]/text(),"法定代表人/执行事务合伙人(委派代表)工作履历")]').xpath(
            'td[2]/table/tbody/tr')
        for index, link in enumerate(links_workhistory):
            item_Workhistory = WorkhistoryItem()
            item_Workhistory['intervall'] = link.xpath('td[1]/text()').extract_first().replace(' ', '')
            item_Workhistory['tenureunit'] = link.xpath('td[2]/text()').extract_first()
            item_Workhistory['department'] = link.xpath('td[3]/text()').extract_first()
            item_Workhistory['jobb'] = link.xpath('td[4]/text()').extract_first()
            item_Workhistory['personname'] = response.xpath(
                '//tr[contains(td[1]/text(),"法定代表人/执行事务合伙人(委派代表)姓名")]').xpath('td[2]/text()').extract_first()
            yield item_Workhistory

        links_fundfor = response.xpath('//tr[contains(td[1]/text(),"暂行办法实施前成立的基金")]').xpath('td[2]/p/a')
        links_fundback = response.xpath('//tr[contains(td[1]/text(),"暂行办法实施后成立的基金")]').xpath('td[2]/p/a')
        for index, link in enumerate(links_fundfor):
            url3 = self.base_url3 + link.xpath('@href').extract_first()[3:]
            yield scrapy.Request(url3, callback=self.info_fund_parse)
        for index, link in enumerate(links_fundback):
            url3 = self.base_url3 + link.xpath('@href').extract_first()[3:]
            yield scrapy.Request(url3, callback=self.info_fund_parse)

    # 根据基金管理人内页访问并保存基金内页信息
    def info_fund_parse(self, response):
        item_Fund = FundItem()
        item_Fund['fundname'] = response.xpath('//tr[contains(td[1]/text(),"基金名称")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['fundnumber'] = response.xpath('//tr[contains(td[1]/text(),"基金编号")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['foundingdate'] = response.xpath('//tr[contains(td[1]/text(),"成立时间")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['filingdate'] = response.xpath('//tr[contains(td[1]/text(),"备案时间")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['filingstage'] = response.xpath('//tr[contains(td[1]/text(),"基金备案阶段")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['fundtype'] = response.xpath('//tr[contains(td[1]/text(),"基金类型")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['currency'] = response.xpath('//tr[contains(td[1]/text(),"币种")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['managername'] = response.xpath('//tr[contains(td[1]/text(),"基金管理人名称")]').xpath(
            'td[2]/a/text()').extract_first()
        item_Fund['managementtype'] = response.xpath('//tr[contains(td[1]/text(),"管理类型")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['trusteename'] = response.xpath('//tr[contains(td[1]/text(),"托管人名称")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['operationstate'] = response.xpath('//tr[contains(td[1]/text(),"运作状态")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['fundupdatedate'] = response.xpath('//tr[contains(td[1]/text(),"基金信息最后更新时间")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['specialtips'] = response.xpath('//tr[contains(td[1]/text(),"基金协会特别提示（针对基金）")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['monthlyreport'] = response.xpath('//tr[contains(td[1]/text(),"当月月报")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['semiannualreport'] = response.xpath('//tr[contains(td[1]/text(),"半年报")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['annualreport'] = response.xpath('//tr[contains(td[1]/text(),"年报")]').xpath(
            'td[2]/text()').extract_first()
        item_Fund['quarterlyreport'] = response.xpath('//tr[contains(td[1]/text(),"季报")]').xpath(
            'td[2]/text()').extract_first()
        yield item_Fund
