# coding=utf-8
"""
@author: kaaokou
"""
import json
import random
import time
import re
from lxml import etree

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


class TianmaoSpider(object):
    """天猫商品子类爬取"""

    def __init__(self):
        # 查询关键字
        self.key = raw_input('[INFO]:请输入你要查询的分类商品信息：')
        # 搜索url
        self.search_url = 'https://list.tmall.com/search_product.htm?'
        self.comment_search_url = 'https://rate.tmall.com/list_detail_rate.htm?'

        # 请求头
        self.headers = {
            "cookie": "cna=9oHHE/ZxfFQCAbfpWd4CKRkA; sm4=440300; hng=CN%7Czh-CN%7CCNY%7C156; t=c103b3bfe361ddc07bc03a608dfb62b0; _tb_token_=fe99e7db6b5ab; cookie2=14cc98a958b5ac73a3907a7bff0d2003; _med=dw:1280&dh:800&pw:2560&ph:1600&ist:0; tk_trace=1; _m_h5_tk=e0dc5bc8ccda55ab6366322e989fbb4a_1533298706857; _m_h5_tk_enc=70c19cf89ab8c1f701c81ab7f56071af; csg=76193f1b; skt=07dd13510341596b; enc=oOUEubTf1SsWnUuBfRSgiT9ZZoprQ80OsqOFeBxA9KMd36Jj%2BZttfE82PeIqIWtTxrn50eg6gv1%2Fy8PC1eWcUA%3D%3D; tt=tmall-main; cq=ccp%3D1; res=scroll%3A1232*5350-client%3A1232*259-offset%3A1232*5350-screen%3A1280*800;",
            # 安卓手机的头
            # "user-agent": "Mozilla/5.0 (Linux; Android 4.4.4; HTC D820u Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.89 Mobile Safari/537.36",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            # "upgrade-insecure-requests": "1"
            # "referer": "https://www.baidu.com/",
            "upgrade-insecure-requests": "0"
        }
        self.query_params = {
            "q": self.key,
            "s": "0",
        }
        self.comment_query_params = {
            "itemId": "571241567992",
            # "spuId": "spu",
            "sellerId": "spu",
            "order": "3",
            "currentPage": "2",
            "append": "0",
            "content": "1",
            "_ksTS": "1533301298838_3336",
            "callback": "jsonp3337",
        }

        self.client = MongoClient()
        self.collections = self.client.sofa.goods
        self.collections_comments = self.client.sofa.comments
        # 错误统计
        self.id_pattern = re.compile(r'\?id=(\d+)')
        self.user_id_pattern = re.compile(r'user_id=(\d+)')
        self.josn_pattern = re.compile(r'jsonp\d{4}\((.*)\)')
        self.error_cnt = 0

    def process_query_params(self, page):
        """
        处理查询参数
        """
        self.query_params['s'] = page * 60
        self.headers['User-Agent'] = random.choice(USER_AGENT_LIST)

    def process_comment_query_params(self, page, id, user_id):
        """
        处理评论查询参数
        """
        self.comment_query_params['currentPage'] = page
        self.comment_query_params['itemId'] = id
        self.comment_query_params['sellerId'] = user_id
        self.comment_query_params['callback'] = 'jsonp' + str(random.randint(1000, 9999))
        ksts = str(time.time() * 1000)
        ksts = '_'.join(ksts.split('.'))
        self.comment_query_params['_ksTS'] = ksts
        self.headers['User-Agent'] = random.choice(USER_AGENT_LIST)

    def send_get_request(self, url, query_params={}):
        """
        发送get请求
        """
        print('[INFO]:正在请求<{}>'.format(url))
        html = requests.get(url, params=query_params, headers=self.headers).content
        return html

    def request_comment(self, item):
        """
        请求评论
        """
        num = item['comment_count'] // 20 + 1
        page = 0
        num = 100 if num > 100 else num
        while page < num:
            # 处理请求
            page += 1
            time.sleep(1)
            self.process_comment_query_params(page, item['id'], item['user_id'])
            # 发送请求
            try:
                html = self.send_get_request(self.comment_search_url, self.comment_query_params)
                comment_items = self.parse_comment(html.decode('gbk').encode('utf-8'), item['id'])
            except:
                continue
            # 保存评论
            if comment_items:
                self.save_comments(comment_items)

    def parse_page(self, html, model=0):
        """
        解析字段，返回items
        """
        html_obj = etree.HTML(html)
        node_list = html_obj.xpath("//div[@id='J_ItemList']/div[@class='product  ']")
        items = []
        print(len(node_list))
        for node in node_list:
            item = {}
            try:
                item['detail_url'] = node.xpath(".//p[@class='productTitle']/a/@href")[0]
                url = item['detail_url']
                item['id'] = self.id_pattern.findall(url)[0]
                item['user_id'] = self.user_id_pattern.findall(url)[0]
                item['name'] = node.xpath(".//p[@class='productTitle']/a/text()")[0].strip()
                item['price'] = node.xpath(".//p[@class='productPrice']/em/text()")[0].strip()
                item['shop'] = node.xpath(".//div[@class='productShop']/a/text()")[0].strip()
                sales = node.xpath(".//p[@class='productStatus']/span[1]/em/text()")
                item['sales'] = sales[0].strip() if sales else 'null'
                comment_count = node.xpath(".//p[@class='productStatus']/span[2]/a/text()")
                item['comment_count'] = self.count_comment(comment_count)
                # 进入详情页爬取评论数
                # comment_count = self.
                items.append(item)
            except:
                self.error_cnt += 1

        return items

    def count_comment(self, comment_count):
        """
        计算评论
        """
        # 将评论转为整数
        if comment_count:
            comment_count = comment_count[0].strip()
            print(comment_count)
            if comment_count.endswith(u'万'):
                comment_count = comment_count.split(u'万')[0]
                comment_count = int(float(comment_count) * 10000)
            else:
                comment_count = int(comment_count)
        else:
            comment_count = 0
        return comment_count

    def parse_comment(self, html, id):
        """
        请求处理评论
        """
        html = self.josn_pattern.findall(html)
        html = json.loads(html[0])
        json_obj = jsonpath(html, '$..rateList')
        comment_items = []
        if not json_obj:
            return []
        for node in json_obj[0]:
            comment_item = {}
            comment_item['id'] = str(id)
            comment_item['comment'] = node.get('rateContent')
            comment_items.append(comment_item)
            print(comment_item['comment'])
        return comment_items

    def save_items(self, items):
        """
        保存数据
        """
        # 1. 写入MongoDB
        self.collections.insert_many(items)

    def save_comments(self, items):
        """
        保存数据
        """
        # 1. 写入MongoDB
        self.collections_comments.insert_many(items)

    def main(self):
        """
        类启动方法
        """
        # 1. 请求页码
        page = 0
        while page < 10:
            # 1.1 处理查询请求
            self.process_query_params(page)
            # 1.2 发送请求
            html = self.send_get_request(self.search_url, self.query_params)
            items = self.parse_page(html)
            self.save_items(items)
            # 1.3 请求评论
            for item in items:
                self.request_comment(item)

            page += 1
            time.sleep(1)

        # 请求评论
        # page = 1
        # while page < 3:
        #     # self.process_comment_query_params(page)
        #     # html = self.send_get_request(self.comment_search_url, self.comment_query_params)
        #     with open('com' + str(page) + 'taobao.html', 'r') as fw:
        #         html = fw.read()
        #
        #     comment_items = self.parse_comment(html)
        #     page += 1
        #     time.sleep(1)

        # 错误的个数
        print(self.error_cnt)
        # 2. 抬头，望天
        print('[INFO]:抬头，望天...')


if __name__ == '__main__':
    spider = TianmaoSpider()
    spider.main()
