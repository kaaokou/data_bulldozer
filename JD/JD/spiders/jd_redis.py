# coding=utf-8
"""
@author: kaaokou
"""
import scrapy

from scrapy.http import response
from scrapy_redis.spiders import RedisSpider

from ..items import JdItem


class JdSpider(RedisSpider):
    name = 'jd_redis'
    allowed_domains = ['jd.com']

    # start_urls = ['https://book.douban.com/tag/']
    # 指定redis中存储的key
    redis_key = "jdspider:start_urls"

    base_url = 'https://search.jd.com/search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&click=0&page='
    urls = [base_url + str(page) for page in range(1, 150, 2)]

    def parse(self, response):
        """分发链接"""
        for url in self.urls:
            # 二级爬取详细页，发送一个请求给引擎
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        """提取内容"""
        node_list = response.xpath("//div[@id='J_goodsList']/ul/li")

        cnt = 0
        print(len(node_list))
        for node in node_list:
            item = JdItem()
            item['spu_id'] = node.xpath("./@data-spu").extract_first()
            item['sku_id'] = node.xpath("./@data-sku").extract_first()
            item['name'] = node.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()").extract_first()
            item['price'] = node.xpath(".//div[@class='p-price']/strong/i/text()").extract_first()
            detail_url = node.xpath(".//div[@class='p-img']/a/@href").extract_first()
            item['detail_url'] = 'https:' + detail_url if detail_url else ''
            default_url = node.xpath(".//div[@class='p-img']/a/img/@src").extract_first()
            item['default_url'] = 'https:' + default_url if default_url else ''
            item['comment'] = node.xpath(".//div[@class='p-commit']/strong/a/text()").extract_first()
            item['shop'] = node.xpath(".//div[@class='p-shop']/span/a/text()").extract_first()
            item['is_self'] = node.xpath(".//div[@class='p-icons']/i[1]/text()").extract_first()

            yield item
            # yield scrapy.Request(url=url)
        print('--' * 40)
        print(cnt)
