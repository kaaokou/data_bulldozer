# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianmaoZItem(scrapy.Item):
    # define the fields for your item here like:

    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    detail_url = scrapy.Field()
    comment_count = scrapy.Field()
    sales_count = scrapy.Field()
    shop_name = scrapy.Field()
    # volume = scrapy.Field()
    # first_category = scrapy.Field()
    # second_category = scrapy.Field()
    item_id = scrapy.Field()
    seller_id = scrapy.Field()

    # 设定时间和爬虫名
    time = scrapy.Field()
    spider = scrapy.Field()