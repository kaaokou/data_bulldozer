#coding:utf-8
import scrapy
from scrapy.http import Request
from ..items import TbSpiderItem
import re

class TbSpider(scrapy.Spider):
	name = "tb_spider"
	start_urls = ["http://taobao.com"]

	def parse(self, response):
		key = "沙发"
		for i in range(0,1):
			url = 'https://s.taobao.com/search?q='+str(key)+'&s='+str(i*44)
			yield Request(url=url, callback=self.parse_page)

	def parse_page(self, response):
		# 通过response获取详情页面的url，需要使用正则表达式
		# 详情页面的网址为：https://detail.tmall.com/item.htm?id=560625291262
		# 需要提取所有的id,然后拼接，再次发出请求
		pattern = re.compile(r'"nid":"\d+?"')
		nid_list = pattern.findall(response.body)
		for nid in nid_list[0:1]:
			print(nid)
			id = nid.split(":")[1][1:-1]
			url = "https://detail.tmall.com/item.htm?id=" + str(id)
			yield Request(url=url, callback=self.parse_detail, dont_filter=True)

	def parse_detail(self, response):
		print(response)
		with open("taobao_detail.html", "w") as f:
			f.write(response.body.decode('gbk').encode('utf-8'))



