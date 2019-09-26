# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 17:31:53 2018

@author: asus
"""

from scrapy import cmdline
 
crawl_name = 'manager'
cmd = 'scrapy crawl {0}'.format(crawl_name)
cmdline.execute(cmd.split())