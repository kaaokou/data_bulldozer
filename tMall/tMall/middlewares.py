# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals

from tMall.settings import USER_AGENT_LIST, PROXY_LIST


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        # print(user_agent)
        request.headers["User-Agent"] = user_agent


class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXY_LIST)
        # request.meta['proxy'] = "http://maozhaojun:ntkn0npx@115.28.141.184:16816"
        print(proxy)
        request.meta['proxy'] = proxy


class TmallSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TmallDownloaderMiddleware(object):
    """设置登录后cookie"""
    def process_request(self, request, spider):
        cookies = {
            "tk_trace": "1",
            " cna": "Gq3ME7xS+kYCAbfpWd6Fiedm",
            " t": "ed7900ff27e9ce9e9e5b7fe35c42f12f",
            " _tb_token_": "e7b13b1543117",
            " cookie2": "13a4a1c64ae1d31a0d09b975cc2bd6ad",
            " hng": "",
            " tracknick": "%5Cu653E%5Cu725B%5Cu7684%5Cu738B%5Cu4E8C%5Cu4E8C%5Cu5C0F",
            " ck1": "",
            " lgc": "%5Cu653E%5Cu725B%5Cu7684%5Cu738B%5Cu4E8C%5Cu4E8C%5Cu5C0F",
            " enc": "vB0K2Mt%2BVjut%2FV51u8J0mi1nPULio20%2FTaTQC%2FdnfX2zybR81qYoBPV3r6K7la7Van4j2SV7ipJJzuskeeXeiQ%3D%3D",
            " dnk": "%5Cu653E%5Cu725B%5Cu7684%5Cu738B%5Cu4E8C%5Cu4E8C%5Cu5C0F",
            " lid": "%E6%94%BE%E7%89%9B%E7%9A%84%E7%8E%8B%E4%BA%8C%E4%BA%8C%E5%B0%8F",
            " OZ_SI_2061": "sTime=1533273497&sIndex=8",
            " OZ_1U_2061": "vid=vb63e5996ea03a.0&ctime=1533284150&ltime=1533276944",
            " OZ_1Y_2061": "erefer=-&eurl=https%3A//detail.tmall.com/item.htm%3Fspm%3Da220m.1000858.1000725.1.7f5a65a9xe7EuE%26id%3D566004018072%26skuId%3D3589195972568%26areaId%3D440300%26user_id%3D196993935%26cat_id%3D2%26is_b%3D1%26rn%3D298c080489f0438c240c620fdd1aef14&etime=1533273497&ctime=1533284150&ltime=1533276944&compid=2061",
            " _m_h5_tk": "f9307e6a860fef3ecbe6004633373432_1533298512218",
            " _m_h5_tk_enc": "89694870c5dd20453f4fb69160942093",
            " uc1": "cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=UIHiLt3xThH8t7YQoFNq&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=false&pas=0&cookie14=UoTfKLJAPYolVA%3D%3D&tag=8&lng=zh_CN",
            " uc3": "vt3=F8dBzrpColnpQA9V%2Fxk%3D&id2=UNDXnNdSrdi8Bg%3D%3D&nk2=1AJJNZw6NloHbhvtgRA%3D&lg2=UtASsssmOIJ0bQ%3D%3D",
            " _l_g_": "Ug%3D%3D",
            " unb": "3031529327",
            " cookie1": "UoYWOT2KMVJUdTCbSqyeZSYLQm6zLbgJO231dyjrXAA%3D",
            " login": "true",
            " cookie17": "UNDXnNdSrdi8Bg%3D%3D",
            " _nk_": "%5Cu653E%5Cu725B%5Cu7684%5Cu738B%5Cu4E8C%5Cu4E8C%5Cu5C0F",
            " uss": "",
            " csg": "4ff185f6",
        }
        request.cookies = cookies
