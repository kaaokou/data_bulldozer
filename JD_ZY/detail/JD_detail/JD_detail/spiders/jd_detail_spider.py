# -*- coding: utf-8 -*-
import re
from urllib import urlencode
import json
import jsonpath

import scrapy
import redis
from lxml import etree

from ..items import JdItem, SkuDetailItem, SkuCommentItem


class JdDetailSpiderSpider(scrapy.Spider):
    name = 'jd_detail_spider'
    allowed_domains = ['*', 'c0.3.cn', 'club.jd.com']
    r = redis.Redis(host="111.230.135.89", port=6379, db=1)
    # 获取redis中存储的入口sku，构建url
    sku_list = r.smembers("jd_sku2")
    # start_urls = ["https://item.jd.com/" + sku + ".html" for sku in sku_list]
    start_urls = ["https://item.jd.com/24870195900.html"]
    print("start_urls is ok !")

    def parse(self, response):
        print(response.url)
        html_obj = etree.HTML(response.body)
        # 提取商品名，默认为为入口sku的商品名
        commodity_name = html_obj.xpath('//div[@class="sku-name"]')[0].text.strip()
        print("commodity_name:" + commodity_name)

        # 提取cat ，以及单个sku的字符串，样板如下
        # clothing cat-1-6728 cat-2-6745 cat-3-13988 item-25354615436 POP POP-2
        s = html_obj.xpath('//body/@class')[0]
        pattern = re.compile(r"cat-\d-\d+")
        result = pattern.findall(s)
        cat = ",".join([r.split("-")[2] for r in result])
        # 提取sku
        pattern2 = re.compile(r"item-\d+")
        result2 = pattern2.findall(s)
        sku = result2[0].split("-")[1]

        # 获取其他规格信息（可能存在没有其他规格）
        sku_list = []
        obj_list = html_obj.xpath('//div[@class="dd"]/div[@data-sku]')
        if len(obj_list) > 0:
            # 存在商品其他的规格选项
            for obj in obj_list:
                sku_id = obj.xpath("./@data-sku")[0]
                print(sku_id)
                msg = obj.xpath("./@data-value")[0]
                print(msg)
                sku_list.append({sku_id: msg})
        else:
            # 不存在商品其他的规格选项
            sku_list = [{sku: "not other option"}]

        # 构建第一轮存储，返回对应的item
        item = JdItem()
        item["sku"] = sku
        item["name"] = commodity_name
        item["option"] = [sku_dict.keys()[0] for sku_dict in sku_list]  # 该列表存储所有的选项sku

        for sku_dict in sku_list:
            # 构建查询价格请求
            yield self.get_price_request(sku_dict, cat, sku)
            # 构建查询评论请求
            yield self.get_comment_request(sku_dict.keys()[0])
        yield item

    def get_price_request(self, sku_dict, cat, sku_pre):
        """构建查询价格请求，并且返回scrapy.Requset实例"""
        sku_id = sku_dict.keys()[0]
        name = sku_dict.values()[0]
        detail_query_params = {
            # 查询商品价格接口
            "skuId": sku_id,
            "area": "1_72_2799_0",
            # "venderId":"696623",
            # "cat": "6728,6745,6785",
            "buyNum": "1",
            # "choseSuitSkuIds":"",
            # "extraParam":{"originid":"1"},
            "ch": "1",
            "fqsp": "0",
            "pduid": "174844899",
        }
        url = ''.join(
            ["https://c0.3.cn/stock?&extraParam={%22originid%22:%221%22}&", urlencode(detail_query_params), "&cat=",
             cat])
        return scrapy.Request(url, meta={"name": name, "sku_pre": sku_pre}, callback=self.price_parse)

    def price_parse(self, response):
        item = SkuDetailItem()
        name = response.meta["name"]
        sku_pre = response.meta['sku_pre']
        item['sku_pre'] = sku_pre
        item["name"] = name
        data = response.body
        # 使用正则表达式提取sku_id 以及 price
        pattern = re.compile(r'"realSkuId":\d+')
        sku_id = pattern.findall(data)[0].split(":")[1]
        pattern2 = re.compile(r'"op":.*?,')
        price = pattern2.findall(data)[0].split(":")[1][:-1]
        item["price"] = price
        item["sku_id"] = sku_id
        print(sku_id, name, price)
        yield item

    def get_comment_request(self, sku_id, page=0):
        """构建查询评论请求，并且返回对应的scrapy.Requset实例"""
        # 评论接口：https://club.jd.com/comment/skuProductPageComments.action?productId=24870207202&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&fold=1
        # 可更改参数：productId=4207732(商品ID)、page=0(第几页评价)、pageSize=10(每页显示的条数)
        # 评论最多100页
        url = "https://club.jd.com/comment/skuProductPageComments.action?score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&"
        query_params = {
            "productId": sku_id,
            "page": page
        }
        # 合并url
        url = "".join([url, urlencode(query_params)])
        print("-----------comment_url---------")
        print(url)
        return scrapy.Request(url, meta={"sku_id": sku_id, "page": page}, callback=self.comment_parse)

    def comment_parse(self, response):
        """解析评论，假如含有下一页，则继续请求"""
        item = SkuCommentItem()
        sku_id = response.meta["sku_id"]
        page = response.meta["page"]
        print("-------comment_parse--------")
        print(sku_id)
        print(page)
        data = json.loads(response.body.decode("gbk"))
        content = jsonpath.jsonpath(data, '$..comments[*].content')
        print(content)
        print("-------comment_parse_end--------")
        # 若该页评论数不足10条，则该sku对应的评论爬取完毕
        if 0 < len(content) < 10:
            item["sku_id"] = sku_id
            item['page'] = page
            item['comment'] = content
            yield item
        elif len(content) == 10:
            # 下一页评论数为0，有可能为10,如果为0，不做任何处理
            item["sku_id"] = sku_id
            item['page'] = page
            item['comment'] = content
            yield item
            page += 1
            yield self.get_comment_request(sku_id, page=page)
        else:
            print("this sku comment is over")
