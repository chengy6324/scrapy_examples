# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 18:34:23 2018

@author: asus
"""

from scrapy import cmdline
 
crawl_name = 'fund'
cmd = 'scrapy crawl {0}'.format(crawl_name)
cmdline.execute(cmd.split())