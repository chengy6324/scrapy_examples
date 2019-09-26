create database crawl_fund;
use crawl_fund;
CREATE TABLE fund (
  fundnumber varchar(100),
  fundname varchar(100),
  fundtype varchar(100),
  fundsize varchar(100),
  fundmanagement varchar(100),
  fundfoundingdate varchar(100),
  fundmanager varchar(100),
  fundranking varchar(100),
  fundservice varchar(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE historicalnetworth (
  networthdate varchar(100),
  unitnetworth varchar(100),
  accumulatednetworth varchar(100),
  dailygrowthrate varchar(100),
  purchasestatus varchar(100),
  redemptionstatus varchar(100),
  bonus varchar(100),
  fundcode varchar(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;