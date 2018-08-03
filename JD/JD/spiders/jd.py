# coding=utf-8
"""
@author: kaaokou
"""
import random
import os

import requests
import time
from lxml import etree
from pymongo import MongoClient
import gevent
from gevent import monkey

# 打补丁
monkey.patch_all()

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


class JDSpider(object):
    """JD商品子类爬取"""

    def __init__(self):
        # 查询参数
        self.key = raw_input('[INFO]:请输入你要查询的分类商品信息：')
        # 将字符串转为url编码

        # 奇数url
        self.odd_url = 'https://search.jd.com/Search?'
        # 偶数页面
        self.even_url = 'https://search.jd.com/s_new.php?'
        # self.search_url = 'https://search.jd.com/s_new.php?'
        # 请求头
        self.headers = {
            "accept": "*/*",
            # "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            # "cookie": "__jdu=1067015182; xtest=1818.cf6b6759; ipLoc-djd=1-72-2799-0; shshshfpa=f683791a-6bd6-e53d-4454-fa92ba27ab7d-1532738258; shshshfpb=003a70d60a31b2479622bb4fec77a4a0a9892ae99b174638f5b5083f68; qrsc=3; ipLocation=%u5317%u4EAC; areaId=1; __jdc=122270672; PCSYCityID=1607; user-key=064c465a-3f3a-4aec-99e3-cf74229526be; cn=0; rkv=V0200; mt_xid=V2_52007VwMTVVtZUl4fQBpsVmBRGwJfXFtGHUBJCBliVBACQQgFU01VTl9VZlMWVV0KUF0eeRpdBW4fE1tBWVJLHEkSXwZsABFiX2hSahxKGloEYwUXUW1YV1wY; unpl=V2_ZzNtbRYFRhV9AURcekkJUmJXE1USABNAIAsWXHsYVQJlBhdbclRCFXwUR11nGF8UZwcZXUVcQhBFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VHoeWgRnBxJUQWdzEkU4dlNyHVkMZzMTbUNnAUEpDUFdfhxbSGcCFVtDV0cVfAt2VUsa; __jda=122270672.1067015182.1531405169.1533124605.1533194167.11; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_ec4198390adf4e09afadd2a910863447|1533194166549; shshshfp=ec948d424d9f9617517b91a4cf596ccf; 3AB9D23F7A4B3C9B=CAFVI6YER64TGNHZW6ICHZIWBLF72BKCNP74QRJVOU6E2AVP5ABOFX7WRZ3OLQSIYAOARR4OJKICGXHA74AHKSH6QU; __jdb=122270672.10.1067015182|11.1533194167; shshshsID=9e4d723e532088c7e4cd85fb23ab566f_7_1533195240821",
            "pragma": "no-cache",
            # 从指定页面过来的
            "referer": "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        self.query_params = {
            "keyword": self.key,
            "enc": "utf-8",
            "qrst": "1",
            "rt": "1",
            "stop": "1",
            "vt": "2",
            "wq": self.key,
            "cid2": "653",
            "cid3": "655",
            "page": "1",
            "s": "",
            "scrolling": "y",
            # 时间戳
            "log_id": "1533195232924",
            "tpl": "3_M",
            "show_items": "",

        }
        # 保存数据到MongoDB
        self.client = MongoClient()
        self.collections = self.client.jd.goods
        # 错误统计
        self.error_cnt = 0
        self.html_head = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>'
        self.html_tail = 'self.html_tail'

    def process_query_params(self, page, skus=''):
        """
        处理查询参数
        """
        self.query_params['show_items'] = skus
        self.query_params['page'] = page
        log_id = str((time.time() * 1000))[:-1]
        self.query_params['log_id'] = log_id
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
        response = etree.HTML(html)
        if model:
            node_list = response.xpath("//li[@class='gl-item']")
        else:
            node_list = response.xpath("//div[@id='J_goodsList']/ul/li")
        items = []
        skus = ''
        for node in node_list:
            item = {}
            try:
                item['spu_id'] = node.xpath("./@data-spu")[0]
                item['sku_id'] = node.xpath("./@data-sku")[0]
                item['name'] = node.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()[1]")[0]
                price = node.xpath(".//div[@class='p-price']/strong/i/text()")
                item['price'] = price[0] if price else '预购商品'
                detail_url = node.xpath(".//div[@class='p-img']/a/@href")[0]
                item['detail_url'] = 'https:' + detail_url if detail_url else ''
                default_url = node.xpath(".//div[@class='p-img']/a/img/@source-data-lazy-img")[0]
                item['default_url'] = 'https:' + default_url if default_url else ''
                item['comment'] = node.xpath(".//div[@class='p-commit']/strong/a/text()")[0]
                # 如果是广告的话没有shop
                shop = node.xpath(".//div[@class='p-shop']/span/a/text()")
                item['shop'] = shop[0] if shop else '广告'
                is_self = node.xpath(".//div[@class='p-icons']/i[1]/text()")
                item['is_self'] = is_self[0] if is_self else '广告'
                skus += item['sku_id'] + ','
                print(item['name'][:16])
            except:
                self.error_cnt += 1
                print('[ERROR]：错误的li')
            finally:
                items.append(item)

        return items, skus

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
        page, skus = 1, ''
        # 使用协程
        spawn_list = []
        while page < 201:
            # 1. 发送奇数页面请求
            self.process_query_params(page, skus)
            html = self.send_get_request(self.odd_url, self.query_params)
            # 解析参数
            items, skus = self.parse_page(html)
            # 存储数据
            self.save_data(items)

            page += 1
            # 2. 发送偶数页面请求
            self.process_query_params(page, skus)
            html = self.send_get_request(self.even_url, self.query_params)
            html = self.html_head + html + self.html_tail
            # 解析参数
            items, skus = self.parse_page(html, model=1)
            # 存储数据
            items, skus = self.parse_page(html, model=1)
            self.save_data(items)

            page += 1
            # 延迟
            time.sleep(1)

        # 错误的个数
        print(self.error_cnt)
        # 2. 抬头，望天
        print('[INFO]:抬头，望天...')


if __name__ == '__main__':
    spider = JDSpider()
    spider.main()
