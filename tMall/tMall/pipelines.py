# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

# import redis
from scrapy.exporters import CsvItemExporter


class TmallPipeline(object):
    def open_spider(self, spider):
        self.f = open("tmall.json", "a")

    def process_item(self, item, spider):
        content = json.dumps(dict(item)) + ",\n"
        self.f.write(content)

        return item

    def close_spider(self, spider):
        self.f.close()


class TmallCsvPipeline(object):
    def open_spider(self, spider):
        self.csv_file = open("tamll.csv", "w")
        self.csv_exporter = CsvItemExporter(self.csv_file)
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        self.csv_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.csv_exporter.finish_exporting()
        self.csv_file.close()

# class TmallRedisPipeline(object):
#     def open_spider(self, spider):
#         self.redis_cli = redis.Redis(host="139.199.160.42", port=6379, db=2)
#
#     def process_item(self, item, spider):
#         content = json.dumps(dict(item))
#         self.redis_cli.lpush("tmall_item", content)
#         return item

