# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

class TbSpiderPipeline(object):
	def open_spider(self, spider):
		self.csv_file = open("taobao.csv", "w")
		self.csv_exporter = CsvItemExporter(self.csv_file)
		self.csv_exporter.start_exporting()

	def process_item(self, item, spider):
		self.csv_exporter.export_item(item)
		return item

	def close_spider(self, spider):
		self.csv_exporter.finish_exporting()
		self.csv_file.close()
				
