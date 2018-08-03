# coding:utf-8

import scrapy
import json

from ..items import Taobao1Item


class Taobao_fruits(scrapy.Spider):
    name = "taobao"
    base_url = "https://list.tmall.com/search_product.htm"

    def start_requests(self):
        """爬取其他类型水果的类型"""
        url = "https://list.tmall.com/search_product.htm?cat=54444001"
        yield scrapy.Request(url, callback=self.parse_list)
        # 爬取所有类型的水果类型的url地址
        url = "https://list.tmall.com/ajax/getAllBrotherCats.htm?cat=54444001"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """解析每种水果类型的url地址"""
        results = response.body.decode("gbk")
        print results
        list_urls = json.loads(results)
        for list_url in list_urls:
            list_url = list_url['href'].encode("utf-8")
            url = self.base_url + list_url
            # print "[INFO]: BASE_URL={}".format(url)
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        """对每一个列表页的数据进行提取"""
        # 获取当前水果的下一页数据
        next_link = response.xpath('//a[@class="ui-page-next"]/@href').extract_first()
        results = response.xpath('//div[@class="product  "]')
        # 判断xpath有没有取到数据，如果没有把该url地址返回重新请求
        if not results:
            fail_url = response.url
            yield scrapy.Request(fail_url)
        category = response.xpath('//div[@class="crumbDrop j_CrumbDrop"]/a/@title').extract()
        for result in results:
            item = Taobao1Item()
            item["itemId"] = result.xpath('./@data-id')
            sellerId = result.xpath('.//div[@class="productImg-wrap"]/a/@href').extract()[0]

            # item["sellerId"]
            item['price'] = result.xpath('.//p/em/@title').extract()[0]
            item["name"] = result.xpath('.//p[@class="productTitle"]/a/@title').extract()[0]
            item["comment_num"] = result.xpath('.//span/a/text()').extract()[0]
            item["shop_name"] = result.xpath('.//div/a[@class="productShop-name"]/text()').extract()[0].strip()
            item["volume"] = result.xpath('.//p/span/em/text()').extract()[0]
            item["first_category"] = category[0]
            item["second_category"] = category[1]
            yield item
        if next_link:
            next_link = self.base_url + next_link
        yield scrapy.Request(next_link, callback=self.parse_list)
