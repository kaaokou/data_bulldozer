# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from settings import *
from scrapy.http.headers import Headers
from pymongo import *
import random
import base64
import time

class Taobao1DownloaderMiddleware(object):
    index = 0

    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENT_LIST)
        request.headers.setdefault("User-Agent", useragent)
        if self.index == 0:
            self.index = 1
            # time.sleep(1)
            print(U"[INFO]: 使用代理：{}".format(PROXY_LIST[0]))
            base64_userpasswd = base64.b64encode(PROXIES[0]['user_passwd'])
            # 对应到代理服务器的信令格式里
            request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd
            request.meta['proxy'] = "http://" + PROXIES[0]['ip_port']
            # request.meta["proxy"] = PROXY_LIST[1]
        else:
            print(U"[INFO]: 该请求并没有使用代理")
            # time.sleep(1)
            self.index = 0


        # 对账户密码进行base64编码转换
        # base64_userpasswd = base64.b64encode(proxy['user_passwd'])
        # # 对应到代理服务器的信令格式里
        # request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd
        # request.meta['proxy'] = "http://" + proxy['ip_port']


class TaobaoDownLoaderCommentMiddleware(object):
    def __init__(self):
        client = MongoClient("118.24.39.177", 27017)
        db = client.taobao
        self.collections = db.taobao
        self.index = 1
        self.itemId = ""
        self.sellerId = ""

    def process_request(self, request, spider):
        if request.meta["first"]:
            self.index += 1
            list1 = self.collections.find({"_id": self.index})
            for i in list1:
                self.itemId = i["itemId"]
                self.sellerId = i["sellerId"]
                url = request.url + "itemId={}&sellerId={}".format(self.itemId, self.sellerId)
        else:
            url = request.url + "itemId={}&sellerId={}".format(self.itemId, self.sellerId)