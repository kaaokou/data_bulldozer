# coding:utf-8

import scrapy
import re
import json
from pymongo import *
from ..items import CommentItem, FaileCommentItem
import time


class TaobaoCommentSpider(scrapy.Spider):
    name = "comment"
    # 初始的url不需要默认就是第一页，只需要去中间件拼接2个id就行了
    first_url = "https://rate.tmall.com/list_detail_rate.htm?callback=jsonp1717&currentPage=1&order=3&"
    # 基础的url主要是为了能拼接页数，也就是能对评论进行翻页
    base_url = "https://rate.tmall.com/list_detail_rate.htm?callback=jsonp1717&order=3&"
    index = 1

    def __init__(self):
        super(TaobaoCommentSpider, self).__init__()
        client = MongoClient("118.24.39.177", 27017)
        db = client.taobao
        self.collections = db.taobao
        # 记录请求成功的存储id
        self.id = 204373
        # 记录请求失败的存储id
        self.Faile_id = 304

    def start_requests(self):
        """从MongoDB数据库中取出需要的itemId和sellerId"""
        for index in range(3000, 6000):
            index += 1
            list1 = self.collections.find({"_id": index})
            for i in list1:
                itemId = i["itemId"]
                sellerId = i["sellerId"]
                url = self.first_url + "itemId={}&sellerId={}".format(itemId, sellerId)
                page = 1
                print(u"[INFO]: 正在发起请求：{}".format(url))
                time.sleep(1)
                yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={"page": page, "itemId": itemId, "sellerId": sellerId})

    def parse(self, response):
        """解析请求的数据，数据为类json格式"""
        rule = re.compile(r"jsonp\d+\((.*)\)")
        results = rule.findall(response.body)[0]
        try:
            results_all = json.loads(results.decode("gbk").encode("utf-8"))
            lastpage = int(results_all["rateDetail"]["paginator"]["lastPage"])
        except:
            lastpage = 1
            results_all = None
        try:
            #  使用正则将数据中的json数据取出
            # 请求成功取出数据返回到管道保存到MongoDB
            for result in results_all["rateDetail"]["rateList"]:
                item = CommentItem()
                item["_id"] = self.id
                self.id += 1
                item["sellerId"] = result["sellerId"]
                item["rateContent"] = result["rateContent"]
                if result.get("appendComment"):
                    item["content"] = result["appendComment"].get("content", None)
                    item["reply"] = result["appendComment"].get("reply", None)
                else:
                    item["content"] = None
                    item["reply"] = None
                yield item
        except:
            # 请求失败将失败的itemId和sellerId还有page值保存到MongoDB
            item = FaileCommentItem()
            item["_id"] = self.Faile_id
            self.Faile_id += 1
            item["sellerId"] = response.meta["sellerId"]
            item["itemId"] = response.meta["itemId"]
            item["page"] = response.meta["page"]
            yield item
        response.meta["page"] += 1
        try:
            if response.meta["page"] <= lastpage:
                response.meta["lastpage"] = lastpage
                url = self.base_url + "currentPage={}".format(response.meta["page"]) + "&itemId={}&sellerId={}".format(response.meta["itemId"], response.meta["sellerId"])
                print(u"[INFO]: 正在发起请求：{}".format(url))
                yield scrapy.Request(url, callback=self.parse_second, dont_filter=True, meta=response.meta)
        except:
            pass

    def parse_second(self, response):
        """解析请求的数据，数据为类json格式"""
        lastpage = response.meta["lastpage"]
        try:
            #  使用正则将数据中的json数据取出
            rule = re.compile(r"jsonp\d+\((.*)\)")
            results = rule.findall(response.body)[0]
            results_all = json.loads(results.decode("gbk").encode("utf-8"))
            # 请求成功取出数据返回到管道保存到MongoDB
            for result in results_all["rateDetail"]["rateList"]:
                item = CommentItem()
                item["_id"] = self.id
                self.id += 1
                item["sellerId"] = result["sellerId"]
                item["rateContent"] = result["rateContent"]
                if result.get("appendComment"):
                    item["content"] = result["appendComment"].get("content", None)
                    item["reply"] = result["appendComment"].get("reply", None)
                else:
                    item["content"] = None
                    item["reply"] = None
                yield item
        except:
            # 请求失败将失败的itemId和sellerId还有page值保存到MongoDB
            item = FaileCommentItem()
            item["_id"] = self.Faile_id
            self.Faile_id += 1
            item["sellerId"] = response.meta["sellerId"]
            item["itemId"] = response.meta["itemId"]
            item["page"] = response.meta["page"]
            yield item
        response.meta["page"] += 1
        # 查看page数是否少于评论总页数，如果少于就将page+1继续发起请求
        if response.meta["page"] <= lastpage:
            url = self.base_url + "currentPage={}".format(response.meta["page"]) + "&itemId={}&sellerId={}".format(
                response.meta["itemId"], response.meta["sellerId"])
            print(u"[INFO]: 正在发起请求：{}".format(url))
            print(u"page : {}; lastpage : {}".format(response.meta["page"], response.meta["lastpage"]))
            yield scrapy.Request(url, callback=self.parse_second, dont_filter=True, meta=response.meta)

