# coding=utf-8
"""
@author: kaaokou
"""

import scrapy

from scrapy.spiders import Spider


class TaobaoSpider(Spider):
    """
    淘宝爬虫
    """
    name = 'taobao'
    allowed_domains = []
    start_urls = []

