# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    spu_id = scrapy.Field()
    sku_id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    detail_url = scrapy.Field()
    default_url = scrapy.Field()
    comment = scrapy.Field()
    shop = scrapy.Field()
    is_self = scrapy.Field()

    # 添加爬虫名和时间
    time = scrapy.Field()
    spider = scrapy.Field()
