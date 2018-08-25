# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import JdItem, SkuDetailItem, SkuCommentItem


class JdPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JdItem):
            print("------------JdItem JdPipeline------------")
            # { 'name': u'\u542f\u6377 \u6c7d\u8f66\u7eb8\u5dfe\u76d2\u6302\u5f0f\u8f66\u8f7d \u5e26\u955c\u7247\u5929\u7a97\u906e\u9633\u677f\u7eb8\u5dfe\u76d2\u8f66\u7528\u62bd\u7eb8\u76d2\u521b\u610f \u6c7d\u8f66\u7528\u54c1\u8d85\u5e02 \u68d5\u8272\u5e26\u955c\u7247\u906e\u9633\u677f\u7eb8\u5dfe\u76d2',
            #     'option': ['24870195900', '24870207201', '24870207202'],
            #     'sku': '24870195900'}

            # 需改写如下格式
            # a = {
            #     'name': u'\u542f\u6377 \u6c7d\u8f66\u7eb8\u5dfe\u76d2\u6302\u5f0f\u8f66\u8f7d \u5e26\u955c\u7247\u5929\u7a97\u906e\u9633\u677f\u7eb8\u5dfe\u76d2\u8f66\u7528\u62bd\u7eb8\u76d2\u521b\u610f \u6c7d\u8f66\u7528\u54c1\u8d85\u5e02 \u68d5\u8272\u5e26\u955c\u7247\u906e\u9633\u677f\u7eb8\u5dfe\u76d2',
            #     'option': [{'24870195900': "null"}, {"24870207201": "null"}, {'24870207202': "null"}],
            #     '_id': '24870195900'}
            print(item)
            print("------------JdItem  end------------")
        return item


class PricePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, SkuDetailItem):
            print("------------SkuDetailItem------------")
            # {'name': u'\u7c73\u8272\u5e26\u955c\u7247\u906e\u9633\u677f\u7eb8\u5dfe\u76d2',
            # 'price': '"88.00"',
            # 'sku_id': '24870207202',
            # 'sku_pre': '24870195900'}
            print(item)
            print("------------SkuDetailItem  end------------")
        return item


class CommentPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, SkuCommentItem):
            print("------------SkuCommentItem------------")
            print(item)
            print("------------SkuCommentItem  end------------")
        return item
