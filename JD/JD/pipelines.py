# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
import json

import redis
from pymongo import MongoClient
from scrapy.exporters import CsvItemExporter


class JDPipeline(object):
    def process_item(self, item, spider):
        # 添加spider_name 以及 抓取时间
        item['time'] = str(datetime.now())
        item['spider'] = spider.name
        return item


# class JDRedisPipeline(object):
#     """存入本地redis"""
#
#     def open_spider(self, spider):
#         self.redis_cli = redis.Redis(host='127.0.0.1', db=2)
#
#     def process_item(self, item, spider):
#         """
#         处理字段
#         """
#         content = json.dumps(dict(item))
#         self.redis_cli.lpush("jd_item", content)
#         return item


class JDMongoDBPipeline(object):
    """存入本地MongoDB"""

    def open_spider(self, spider):
        """爬虫开启的时候执行"""
        self.client = MongoClient(host="localhost", port=27017)
        self.collection = self.client.jd.classify

    def process_item(self, item, spider):
        if not item:
            print('[INFO]:', item)
            return item
        self.collection.insert(dict(item))
        return item


class JDCsvPipeline(object):
    """
    将数据写入本地csv文件
    """
    def open_spider(self, spider):
        self.csv_file = open('jd.csv', 'w')
        self.csv_exporter = CsvItemExporter(self.csv_file)
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        self.csv_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.csv_exporter.finish_exporting()
        self.csv_file.close()
