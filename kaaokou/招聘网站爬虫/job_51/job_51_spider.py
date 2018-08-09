# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-12 下午8:45
"""
通过下一页，爬取所有信息，基本无反爬
"""
import json

import requests
import urllib
from bs4 import BeautifulSoup


class JobSpider(object):
    def __init__(self):
        self.base_url = "https://search.51job.com/list/040000,000000,0000,00,9,99,"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
        self.position_list = []
        self.page = 1
        self.kword = urllib.quote(raw_input("查询岗位："))

    def send_request(self, url):
        """
        发送请求
        :param url: 地址
        :return: unicode
        """
        response = requests.get(url, headers=self.headers)
        print("[INFO]正在爬取第{}页的所有职位信息{}".format(self.page, url))
        return response.content

    def parse_page(self, html):
        """
        获取当前页的职位信息
        :param html: 列表页
        :return: 下一个列表页url
        """
        soup = BeautifulSoup(html, "lxml")
        node_list = soup.select(".dw_table .el")

        for node in node_list[1:]:
            item = {}
            detail_item = {"work_require": ""}
            item["detail_url"] = node.select("span")[0].a.get("href")
            try:
                detail_html = self.send_request(item["detail_url"])
                detail_item = self.parse_detail(detail_html)
            except Exception as e:
                print(item["detail_url"], "这一页不要了", e)
                return soup.select(".bk")[1].a.get("href")
            item["position_name"] = node.select("span")[0].a.get("title")
            item["company_name"] = node.select("span")[1].a.get("title")
            item["company_address"] = node.select("span")[2].string
            item["salary"] = node.select("span")[3].string
            item["create_time"] = node.select("span")[4].string
            item.update(detail_item)
            self.position_list.append(item)

        if soup.select(".bk")[1].find_all("a"):
            return soup.select(".bk")[1].a.get("href")
        return False

    def parse_detail(self, html):
        """
        获取详情页职位描述
        :param html:详情页html
        :return: 职位描述dict
        """
        soup = BeautifulSoup(html, "lxml")
        ul_list = soup.select(".bmsg, .job_msg, .inbox")
        item = {}
        require_str = ""
        for node in ul_list[0].select("p"):
            require_str += node.get_text() + "\n"
        item["work_require"] = require_str
        return item

    def save_file(self):
        """
        保存json数据格式
        :return: [{},{}...]
        """
        json.dump(self.position_list, open("position.json", "w"))

    def main(self):
        """
        调度器
        :return: ok
        """
        start_url = "https://search.51job.com/list/040000,000000,0000,00,9,99," + self.kword + ",2,1.html"
        html = self.send_request(start_url)

        while self.page <= 5:
            url = self.parse_page(html)
            if not url:
                break
            html = self.send_request(url)
            self.page += 1
        self.save_file()
        print("爬取完成")


if __name__ == '__main__':
    spider = JobSpider()
    spider.main()
