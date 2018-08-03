# coding=utf-8
"""
@author: kaaokou
"""
import json
import random
import time
import re

from jsonpath import jsonpath
import requests
from pymongo import MongoClient


USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
]


class TaoBaoSpider(object):
    """淘宝商品子类爬取"""

    def __init__(self):
        # 查询关键字
        self.key = raw_input('[INFO]:请输入你要查询的分类商品信息：')
        # 搜索url
        self.search_url = 'https://s.taobao.com/search?'
        # 请求头
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            # "upgrade-insecure-requests": "1"
        }
        self.query_params = {
            "q": self.key,
            "s": "0",
        }
        # json数据提取规则
        self.json_pattern = re.compile(r'g_page_config = (.*);')
        self.name_pattern = re.compile(r'<.*?>.*?</.*?>')
        # 保存数据到MongoDB
        self.client = MongoClient()
        self.collections = self.client.tb.goods
        # 错误统计
        self.error_cnt = 0

    def process_query_params(self, page):
        """
        处理查询参数
        """
        self.query_params['s'] = page * 44
        self.headers['User-Agent'] = random.choice(USER_AGENT_LIST)

    def send_get_request(self, url, query_params={}):
        """
        发送get请求
        """
        print('[INFO]:正在请求<{}>'.format(url))
        html = requests.get(url, params=query_params, headers=self.headers).content
        return html

    def parse_page(self, html, model=0):
        """
        解析字段，返回items和请求下一页的skus
        """
        html = self.json_pattern.findall(html, re.M)

        json_obj = jsonpath(json.loads(html[0]), '$..auctions')

        items = []
        for node in json_obj[0]:
            item = {}
            # item['spu_id'] = node.xpath("./@data-spu")[0]
            item['sku_id'] = node.get('nid')
            # 对name字段正则替换
            name = node.get('title')
            item['name'] = self.name_pattern.sub('-', name)
            item['price'] = node.get('view_price')
            item['detail_url'] = node.get('detail_url')
            sales = node.get('view_sales')
            item['sales'] = sales[:-3]
            item['comment_count'] = node.get('comment_count')
            items.append(item)
            print(item['name'])

        return items

    def save_data(self, items):
        """
        保存数据
        """
        # 1. 写入MongoDB
        self.collections.insert_many(items)

    def main(self):
        """
        类启动方法
        """

        # 1. 请求页码
        page = 0
        while page < 34:
            # 1. 发送奇数页面请求
            self.process_query_params(page)
            html = self.send_get_request(self.search_url, self.query_params)
            # with open(str(page) + 'taobao.html', 'r') as fr:
            #     html = fr.read()
            # 解析参数
            items = self.parse_page(html)
            # 存储数据
            self.save_data(items)
            page += 1
            time.sleep(1)

        # 错误的个数
        print(self.error_cnt)
        # 2. 抬头，望天
        print('[INFO]:抬头，望天...')


if __name__ == '__main__':
    spider = TaoBaoSpider()
    spider.main()
