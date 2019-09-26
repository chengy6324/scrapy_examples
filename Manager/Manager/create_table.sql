create database crawl;
use crawl;
CREATE TABLE manager (
  integrityinformation varchar(100),
  nameChinese varchar(100),
  nameEnglish varchar(100),
  registernumber varchar(100),
  organizationalcode varchar(100),
  registerdate varchar(100),
  foundingdate varchar(100),
  registeraddress varchar(100),
  officeaddress varchar(100),
  registeredcapital varchar(100),
  paidincapital varchar(100),
  natureofenterprise varchar(100),
  capitalproportion varchar(100),
  typeor varchar(100),
  businesstype varchar(100),
  employeesnumber varchar(100),
  institutionalwebsite varchar(100),
  investmentsuggestion varchar(100),
  ismember varchar(100),
  memberrepresentative varchar(100),
  membershiptype varchar(100),
  admissiondate varchar(100),
  legalopinionstatus varchar(100),
  nameoflawfirm varchar(100),
  nameoflawyer varchar(100),
  managerupdatedate varchar(100),
  specialpromptinformation varchar(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE person (
  personname varchar(100),
  job varchar(100),
  fundqualification varchar(100),
  managernumber varchar(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE workhistory (
  intervall varchar(100),
  tenureunit varchar(100),
  department varchar(100),
  jobb varchar(100),
  personname varchar(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE fund (
  fundname varchar(100),
  fundnumber varchar(100),
  foundingdate varchar(100),
  filingdate varchar(100),
  filingstage varchar(100),
  fundtype varchar(100),
  currency varchar(100),
  managername varchar(100),
  managementtype varchar(100),
  trusteename varchar(100),
  operationstate varchar(100),
  fundupdatedate varchar(100),
  specialtips varchar(100),
  monthlyreport varchar(100),
  semiannualreport varchar(100),
  annualreport varchar(100),
  quarterlyreport varchar(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;