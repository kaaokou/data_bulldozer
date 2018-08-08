# -*- coding: utf-8 -*-
import json
import re
import time
import sys

from jsonpath import jsonpath

reload(sys)
sys.setdefaultencoding("utf-8")
import scrapy
from scrapy import Request

from tMall.items import TmallItem


class TmallSpider(scrapy.Spider):
    name = 'tmall'
    allowed_domains = ['tmall.com']
    base_url = "https://list.tmall.com/search_product.htm?sort=rq&q=%C5%AE%D7%B0"
    start_urls = [base_url + "&s=" + str(page) for page in range(0, 41, 60)]

    def parse(self, response):
        node_list = response.xpath("//div[@id='J_ItemList']/div")
        for node in node_list:
            item = TmallItem()
            item['id'] = node.xpath("./@data-id").extract_first()
            item['title'] = node.xpath(".//p[@class='productTitle']/a/@title").extract_first()
            item['shopname'] = node.xpath(".//a[@class='productShop-name']/text()").extract_first().strip()
            detail_url = "https://detail.tmall.com/item.htm?id=" + item['id']
            yield scrapy.Request(detail_url, meta={"item": item}, callback=self.parse_detail)
            time.sleep(1)

    def parse_detail(self, response):
        item = response.meta["item"]
        item['addr'] = response.xpath("//span[@id='J_deliveryAdd']/text()").extract_first()
        # item['month_sales'] = response.xpath("//li[@class='tm-ind-item tm-ind-sellCount']//span[@class='tm-count']").extract_first()

        print("***" * 30)
        print("商品id:{}".format(item["id"]))
        print("商品标题:{}".format(item['title']))
        print("商店名:{}".format(item['shopname']))
        # print("商品月销量:{}".format(item['month_sales']))
        print("***" * 30)
        # for url in urls:
        id = item["id"]
        headers = {"Referer": response.url}
        url = "https://mdskip.taobao.com/core/initItemDetail.htm?itemId=" + id
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_json, dont_filter=True)
        time.sleep(1)

    def parse_json(self, response):
        # item = response.meta["item"]
        json_data = response.body.decode("gbk")
        python_data = json.loads(json_data)
        # print(python_data)
        # print("--"*100)
        json_list = jsonpath(python_data, "$..promotionList")
        # print(price_list)
        price_list = [i[0].get("price") for i in json_list]
        price_li=[]
        for price in price_list:
            if price is None:
                price_list.remove(price)
            else:
                price_li.append(price.encode("utf-8"))

        if len(price_li) % 2 == 0:
            price =float(price_li[len(price_li) / 2 - 1]) + float(price_li[len(price_li) / 2])/2
            print(price)
        elif len(price_li) % 2 == 1:
            price = float(price_li[len(price_li) / 2])
            print(price)


