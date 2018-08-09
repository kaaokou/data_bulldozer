# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Taobao1Item(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    comment_num = scrapy.Field()
    shop_name = scrapy.Field()
    volume = scrapy.Field()
    first_category = scrapy.Field()
    second_category = scrapy.Field()
    itemId = scrapy.Field()
    sellerId = scrapy.Field()


class CommentItem(scrapy.Item):
    rateContent = scrapy.Field()
    reply = scrapy.Field()
    content = scrapy.Field()
    sellerId = scrapy.Field()
    _id = scrapy.Field()


class FaileCommentItem(scrapy.Item):
    _id = scrapy.Field()
    itemId = scrapy.Field()
    sellerId = scrapy.Field()
    page = scrapy.Field()