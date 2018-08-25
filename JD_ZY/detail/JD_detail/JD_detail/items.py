# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 用作_id,存在mongodb中的product集合
    sku = scrapy.Field()
    # 该商品名字
    name = scrapy.Field()
    # 可选规格参数选项，主要为mongodb中的sku_detail集合的_id
    option = scrapy.Field()


class SkuDetailItem(scrapy.Item):
    """对应的sku中的价格，规格选项名"""
    sku_pre = scrapy.Field()
    sku_id = scrapy.Field()
    # 规格选项名
    name = scrapy.Field()
    # 评论 ，主要为列表
    price = scrapy.Field()


class SkuCommentItem(scrapy.Item):
    """对应sku的评论"""
    sku_id = scrapy.Field()
    comment = scrapy.Field()
    page = scrapy.Field()  # 评论页数
