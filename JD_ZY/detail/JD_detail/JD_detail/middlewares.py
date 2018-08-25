# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import base64

from scrapy import signals

from settings import USER_AGENT_LIST, PROXIES


class UserAgentRandom(object):
    """随机选择useragent"""

    def process_request(self, request, spider):
        # print("*************useragent!****************")
        useragent = random.choice(USER_AGENT_LIST)
        # print(useragent)
        request.headers.setdefault("User-Agent", useragent)


class RandomProxy(object):
    def process_request(self, request, spider):
        # print("***********proxy***************!")
        proxy = random.choice(PROXIES)
        # print(proxy)
        # request.meta['proxy'] ="http://115.28.141.184:16816"
        request.meta['proxy'] = proxy

