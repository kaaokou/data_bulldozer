# coding=utf-8
"""
@author: kaaokou
"""

import time
import json
import urllib
import random

from bs4 import BeautifulSoup
from jsonpath import jsonpath
import requests

from proxy_list import PROXY_LIST, USER_AGENT_LIST


# 统计被发现的链接个数
CNT = 0


class LagouSpider(object):
    """拉钩网站爬取信息"""

    def __init__(self):
        self.city = raw_input('[INFO]请输入你需要查询职位的城市：')
        self.kd = raw_input("[INFO]请输入你要查询的岗位名称：")
        self.end_page = int(raw_input("[INFO]请输入你要爬取的最大页面：")) + 1
        # https://www.lagou.com/jobs/list_web%E5%BC%80%E5%8F%91?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=
        self.base_referer = "https://www.lagou.com/jobs/list_"
        self.base_url = "https://www.lagou.com/jobs/positionAjax.json?"
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            # "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "40",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "JSESSIONID=ABAAABAAADEAAFI213B7B9B46B7DB8063765DD4B30F3A95; _ga=GA1.2.1971318618.1531380175; user_trace_token=20180712152255-652c0d21-85a4-11e8-95cc-525400f775ce; LGUID=20180712152255-652c1017-85a4-11e8-95cc-525400f775ce; index_location_city=%E6%B7%B1%E5%9C%B3; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531380181; TG-TRACK-CODE=search_code; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531381374; LGRID=20180712154255-3077f107-85a7-11e8-9d42-5254005c3644; SEARCH_ID=359523a3f9bf440e848f895196eafa30",
            "Host": "www.lagou.com",
            "Origin": "https://www.lagou.com",
            "Pragma": "no-cache",
            "Referer": self.base_referer + self.kd + '?' + urllib.urlencode({'city': self.city}),
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "X-Anit-Forge-Code": "0",
            "X-Anit-Forge-Token": "None",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.query_string = {
            "px": "default",
            "city": self.city,
            "needAddtionalResult": "false",
            # "cl": "false",
            # "fromSearch": "true",
            # "labelWords": "",
            # "suginput": "",
        }
        self.form_data = {
            "first": "true",
            "pn": "1",
            "kd": self.kd,
        }

        self.item_list = []

    def send_post_request(self, url):
        """发送请求，返回html"""
        print('[INFO]:正在请求<{}>'.format(url))
        # 发送POST请求
        proxies = random.choice(PROXY_LIST)
        try:
            python_obj = requests.post(url, params=self.query_string, data=self.form_data,
                                       headers=self.headers, proxies=proxies).json()
        except Exception as e:
            print('[ERROR]:请求<{}>失败'.format(url))
            return None

        return python_obj

    def send_get_request(self, url):
        """get请求"""
        print('[INFO]:正在请求<{}>'.format(url))
        # 发送get请求
        proxies = random.choice(PROXY_LIST)
        headers = {
            "User-Agent": random.choice(USER_AGENT_LIST),
        }
        try:
            html = requests.get(url, headers=headers, proxies=proxies).content
        except Exception as e:
            print('[ERROR]:请求<{}>失败'.format(url))
            return None
        return html

    def parse_page(self, python_obj):
        """处理json字典数据"""
        # $表示根节点
        position_list = jsonpath(python_obj, "$..result")[0]
        for position in position_list:
            item = {}
            # 职位、公司名称、发布时间、薪资、招聘人数、学历要求、融资情况
            item['companySize'] = position['companySize']
            item['positionName'] = position['positionName']
            item['subwayline'] = position['subwayline']
            item['education'] = position['education']
            item['financeStage'] = position['financeStage']
            item['city'] = position['city']
            item['district'] = position['district']
            item['createTime'] = position['createTime']
            item['salary'] = position['salary']
            item['workYear'] = position['workYear']
            item['secondType'] = position['secondType']
            item['companyFullName'] = position['companyFullName']
            # 获取的是列表，不好提取
            # item['companyLabelList'] = position['companyLabelList']
            item['positionAdvantage'] = position['positionAdvantage']

            # 位置信息，进一步爬取要求，更换User-Agent
            item['positionId'] = position['positionId']
            detail_url = "https://www.lagou.com/jobs/" + str(item['positionId']) + '.html'
            html = self.send_get_request(detail_url)
            item['positionDetail'] = self.parse_detail(html)
            time.sleep(random.randint(3, 6))

            # 追加至列表
            self.item_list.append(item)

    def parse_detail(self, html):
        """提取详情页面的岗位职责"""
        soup_obj = BeautifulSoup(html, 'lxml')
        detail_list = soup_obj.select('.job_bt > div')
        if len(detail_list) == 0:
            # print(html)
            global CNT
            CNT += 1
            return '被拉钩发现了'
        position_detail = ''
        for detail in detail_list[0].select('p'):
            position_detail += detail.get_text()
        return position_detail

    def save_data(self):
        """保存数据"""
        print("[INFO]正在写入<lagou.json>数据")
        json.dump(self.item_list, open('lagou.json', 'w'))

    def help_message(self):
        """帮助信息显示"""
        print('==========================')
        print('==========================')

    def main(self):
        """类启动方法"""
        # 1.发送请求
        page = 1
        while page < self.end_page:
            self.form_data['pn'] = page
            python_obj = self.send_post_request(self.base_url)
            self.parse_page(python_obj)
            page += 1
            time.sleep(random.randint(3, 6))

        # 2.写入文件
        self.save_data()
        print('[INFO]:一共被发现<{}>次请求'.format(CNT))


if __name__ == '__main__':
    spider = LagouSpider()
    spider.main()
