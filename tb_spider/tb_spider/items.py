# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TbSpiderItem(scrapy.Item):
	product_price = scrapy.Field()
	product_name = scrapy.Field()
	product_feature = scrapy.Field()
	product_count = scrapy.Field()
	comment_count = scrapy.Field()
	product_province = scrapy.Field()
	product_city = scrapy.Field()
