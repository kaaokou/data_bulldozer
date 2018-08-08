# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import *
from items import CommentItem, FaileCommentItem


class Taobao1Pipeline(object):

    def open_spider(self, spider):
        client = MongoClient("118.24.39.177", 27017)
        db = client.taobao
        self.collections = db.taobao

    def process_item(self, item, spider):
        content = dict(item)
        self.collections.insert(content)
        return item


class CommentPipeline(object):
    def open_spider(self, spider):
        client = MongoClient("118.24.39.177", 27017)
        db = client.taobao
        self.collections = db.comment

    def process_item(self, item, spider):
        if isinstance(item, CommentItem):
            content = dict(item)
            self.collections.insert(content)
        return item


class FaileCommentPipeline(object):
    def open_spider(self, spider):
        client = MongoClient("118.24.39.177", 27017)
        db = client.taobao
        self.collections = db.faile_comment

    def process_item(self, item, spider):
        if isinstance(item, FaileCommentItem):
            content = dict(item)
            self.collections.insert(content)
        return item