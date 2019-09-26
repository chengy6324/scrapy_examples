# -*- coding: utf-8 -*-
import scrapy
# import time
import json
from ..items import FundItem
from ..items import HistoricalnetworthItem
import time
import re


class FundSpider(scrapy.Spider):
    name = 'fund'  # 爬虫名称
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "fund.eastmoney.com",
        "Referer": "http://fund.eastmoney.com/fund.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    headers_2 = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "st_pvi=89134369150701; qgqp_b_id=c3beb531aabc12b6ca376b53a3a4f839; st_si=46658484905433; st_sn=1; st_psi=20181218183555754-111000300841-9702661269; st_asi=delete; EMFUND0=12-16%2023%3A42%3A51@%23%24%u56FD%u6295%u745E%u94F6%u65B0%u6D3B%u529B%u5B9A%u5F00%u6DF7%u5408A@%23%24001584; EMFUND1=12-17%2019%3A16%3A11@%23%24%u9E4F%u534E%u524D%u6D77%u4E07%u79D1REITS@%23%24184801; EMFUND2=12-17%2019%3A26%3A50@%23%24%u5174%u5168%u6CAA%u6DF1300%u6307%u6570%28LOF%29@%23%24163407; EMFUND3=12-17%2019%3A41%3A45@%23%24%u4E0A%u6295%u6469%u6839%u5168%u7403%u5929%u7136%u8D44%u6E90%u6DF7%u5408@%23%24378546; EMFUND4=12-18%2015%3A23%3A46@%23%24%u6C47%u5B89%u4E30%u5229%u6DF7%u5408C@%23%24003887; EMFUND5=12-17%2022%3A54%3A06@%23%24%u4E2D%u878D%u946B%u601D%u8DEF%u6DF7%u5408A@%23%24004008; EMFUND6=12-18%2011%3A26%3A06@%23%24%u5E7F%u53D1%u4E2D%u8BC1%u57FA%u5EFA%u5DE5%u7A0B%u6307%u6570C@%23%24005224; EMFUND7=12-18%2017%3A24%3A03@%23%24%u5EFA%u4FE1%u6539%u9769%u7EA2%u5229%u80A1%u7968@%23%24000592; EMFUND8=12-18%2017%3A32%3A08@%23%24%u666F%u987A%u957F%u57CE%u54C1%u8D28%u6295%u8D44%u6DF7%u5408@%23%24000020; EMFUND9=12-18 18:36:09@#$%u878D%u901A%u589E%u76CA%u503A%u5238A/B@%23%24002342",
        "Host": "api.fund.eastmoney.com",
        "Referer": "http://fundf10.eastmoney.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    # 开放式基金净值表页面
    urls = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page='
    urls_tail = ',200&dt=1545044153559&atfc=&onlySale=0'
    # 基金内页url地址
    base_url2 = 'http://fund.eastmoney.com/'
    base_url2_tail = '.html'
    # 基金历史净值内页url地址
    base_url3 = 'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery183049938394940756714_'
    base_url3_tail1 = '&fundCode='
    base_url3_tail2 = '&pageIndex='
    base_url3_tail3 = '&pageSize=1000&startDate=&endDate=&_='

    # 发送post请求访问基金净值表页面
    def start_requests(self):
        yield scrapy.Request(
            self.urls + str(0) + self.urls_tail,
            method="GET",
            headers=self.headers,
            body="{}",
            callback=self.parse,
            dont_filter=True,
        )

    # 得到基金内页url地址
    def parse(self, response):
        str_ = response.body_as_unicode()[7:]
        str_2 = re.sub('{c', '{"c', str_)
        str_3 = re.sub(',[a-z]', ',"d', str_2)
        str_4 = re.sub('[a-z]:', 'd":', str_3)
        str_5 = re.sub(',]', ']', str_4)
        response = json.loads(str_5)
        for num in range(len(response.get('datad'))):
            url2 = self.base_url2 + response.get('datad')[num][0] + self.base_url2_tail
            yield scrapy.Request(url2, callback=self.info_parse)

        base_num_page = int(response.get('durpagd'))  # 当前页码
        base_num_page = base_num_page + 1

        base_max_page = int(response.get('daged'))  # 总页码
        if base_num_page <= base_max_page:
            yield scrapy.Request(
                self.urls + str(base_num_page) + self.urls_tail,
                method="GET",
                headers=self.headers,
                body="{}",
                callback=self.parse,
                dont_filter=True,
            )

    # 访问并保存基金基础信息，进入历史净值页面
    def info_parse(self, response):
        item_Fund = FundItem()
        item_Fund['fundnumber'] = response.xpath('//span[contains(@class,"ui-num")]').xpath('text()').extract_first()
        item_Fund['fundname'] = response.xpath('//div[contains(@class,"fundDetail-tit")]').xpath(
            'div[1]/text()').extract_first()
        temp = response.xpath('//td[contains(text(),"基金类型")]').xpath('text()').extract()
        if len(temp) >= 2:
            item_Fund['fundtype'] = response.xpath('//td[contains(text(),"基金类型")]').xpath('a/text()').extract_first() + \
                                    temp[1]
        else:
            item_Fund['fundtype'] = response.xpath('//td[contains(text(),"基金类型")]').xpath('a/text()').extract_first()
        item_Fund['fundsize'] = response.xpath('//td[contains(a/text(),"基金规模")]').xpath('text()').extract_first()[1:]
        item_Fund['fundmanagement'] = response.xpath('//td[contains(text(),"基金经理")]').xpath('a/text()').extract_first()
        item_Fund['fundfoundingdate'] = response.xpath('//td[contains(span/text(),"成 立 日")]').xpath(
            'text()').extract_first()[1:]
        item_Fund['fundmanager'] = response.xpath('//td[contains(span/text(),"管 理 人")]').xpath(
            'a/text()').extract_first()

        temp_fundranking = response.xpath('//td[contains(a/text(),"基金评级")]').xpath('div').xpath(
            '@class').extract_first()
        if temp_fundranking == 'jjpj':
            item_Fund['fundranking'] = '暂无评级'
        else:
            item_Fund['fundranking'] = \
            response.xpath('//td[contains(a/text(),"基金评级")]').xpath('div').xpath('@class').extract_first()[-1]
        item_Fund['fundservice'] = response.xpath(
            '//*[@id="body"]/div[12]/div/div/div[2]/div[2]/div[2]/div[2]/div[4]/span[2]/span[2]/text()').extract_first()
        yield item_Fund

        fundcode = response.xpath('//span[contains(@class,"ui-num")]').xpath('text()').extract_first()
        time_str = str(round(time.time() * 1000))
        url3 = self.base_url3 + time_str + self.base_url3_tail1 + fundcode + self.base_url3_tail2 + str(
            1) + self.base_url3_tail3 + str(round(time.time() * 1000))
        yield scrapy.Request(url3, method="GET", headers=self.headers_2, callback=self.info_fund_jjjz,
                             meta={'fundcode': fundcode, 'time_str': time_str})

    # 访问并保存基金历史净值信息
    def info_fund_jjjz(self, response):
        fundcode = response.meta['fundcode']
        time_str = response.meta['time_str']
        str_ = response.body_as_unicode()
        index = str_.find('{')
        str_2 = str_[index:-1]
        response = json.loads(str_2)

        for i in range(len(response.get('Data').get('LSJZList'))):
            item_Historicalnetworth = HistoricalnetworthItem()
            item_Historicalnetworth['networthdate'] = response.get('Data').get('LSJZList')[i].get('FSRQ')
            item_Historicalnetworth['unitnetworth'] = response.get('Data').get('LSJZList')[i].get('DWJZ')
            item_Historicalnetworth['accumulatednetworth'] = response.get('Data').get('LSJZList')[i].get('LJJZ')
            item_Historicalnetworth['dailygrowthrate'] = response.get('Data').get('LSJZList')[i].get('JZZZL')
            item_Historicalnetworth['purchasestatus'] = response.get('Data').get('LSJZList')[i].get('SGZT')
            item_Historicalnetworth['redemptionstatus'] = response.get('Data').get('LSJZList')[i].get('SHZT')
            item_Historicalnetworth['bonus'] = response.get('Data').get('LSJZList')[i].get('FHSP')
            item_Historicalnetworth['fundcode'] = fundcode
            yield item_Historicalnetworth

        int_totalcount = int(response.get('TotalCount'))
        max_page = int_totalcount // 1000 + 1  # 总页码

        num_page = int(response.get('PageIndex'))  # 当前页码
        num_page = num_page + 1
        url4 = self.base_url3 + time_str + self.base_url3_tail1 + fundcode + self.base_url3_tail2 + str(
            num_page) + self.base_url3_tail3 + str(round(time.time() * 1000))
        if num_page <= max_page:
            yield scrapy.Request(
                url4,
                method="GET",
                headers=self.headers_2,
                callback=self.info_fund_jjjz,
                meta={'fundcode': fundcode, 'time_str': time_str}
            )
