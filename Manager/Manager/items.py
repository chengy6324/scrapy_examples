# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 基金管理人类
class ManagerItem(scrapy.Item):
    integrityinformation = scrapy.Field()  # 机构诚信信息
    nameChinese = scrapy.Field()  # 基金管理人全称（中文）
    nameEnglish = scrapy.Field()  # 基金管理人全称（英文）
    registernumber = scrapy.Field()  # 登记编号
    organizationalcode = scrapy.Field()  # 组织机构代码
    registerdate = scrapy.Field()  # 登记日期
    foundingdate = scrapy.Field()  # 成立日期
    registeraddress = scrapy.Field()  # 注册地址
    officeaddress = scrapy.Field()  # 办公地址
    registeredcapital = scrapy.Field()  # 注册资本（万元）（人民币）
    paidincapital = scrapy.Field()  # 实缴资本（万元）（人民币）
    natureofenterprise = scrapy.Field()  # 企业性质
    capitalproportion = scrapy.Field()  # 注册资本实缴比例
    typeor = scrapy.Field()  # 机构类型
    businesstype = scrapy.Field()  # 业务类型
    employeesnumber = scrapy.Field()  # 员工人数
    institutionalwebsite = scrapy.Field()  # 机构网址
    investmentsuggestion = scrapy.Field()  # 是否为符合提供投资建议条件的第三方机构
    ismember = scrapy.Field()  # 是否为会员
    memberrepresentative = scrapy.Field()  # 会员代表
    membershiptype = scrapy.Field()  # 当前会员类型
    admissiondate = scrapy.Field()  # 入会时间
    legalopinionstatus = scrapy.Field()  # 法律意见书状态
    nameoflawfirm = scrapy.Field()  # 律师事务所名称
    nameoflawyer = scrapy.Field()  # 律师姓名
    managerupdatedate = scrapy.Field()  # 机构信息最后更新时间
    specialpromptinformation = scrapy.Field()  # 特别提示信息


# 高管类
class PersonItem(scrapy.Item):
    personname = scrapy.Field()  # 高管姓名
    job = scrapy.Field()  # 职务
    fundqualification = scrapy.Field()  # 是否具有基金从业资格
    managernumber = scrapy.Field()  # 基金管理人登记编号


# 法定代表人/执行事务合伙人(委派代表)工作履历类
class WorkhistoryItem(scrapy.Item):
    intervall = scrapy.Field()  # 时间
    tenureunit = scrapy.Field()  # 任职单位
    department = scrapy.Field()  # 任职部门
    jobb = scrapy.Field()  # 职务
    personname = scrapy.Field()  # 法定代表人/执行事务合伙人(委派代表)姓名


# 基金类
class FundItem(scrapy.Item):
    fundname = scrapy.Field()  # 基金名称
    fundnumber = scrapy.Field()  # 基金编号
    foundingdate = scrapy.Field()  # 成立时间
    filingdate = scrapy.Field()  # 备案时间
    filingstage = scrapy.Field()  # 基金备案阶段
    fundtype = scrapy.Field()  # 基金类型
    currency = scrapy.Field()  # 币种
    managername = scrapy.Field()  # 基金管理人名称
    managementtype = scrapy.Field()  # 管理类型
    trusteename = scrapy.Field()  # 托管人名称
    operationstate = scrapy.Field()  # 运作状态
    fundupdatedate = scrapy.Field()  # 基金信息最后更新时间
    specialtips = scrapy.Field()  # 基金协会特别提示（针对基金）
    monthlyreport = scrapy.Field()  # 当月月报
    semiannualreport = scrapy.Field()  # 半年报
    annualreport = scrapy.Field()  # 年报
    quarterlyreport = scrapy.Field()  # 季报
