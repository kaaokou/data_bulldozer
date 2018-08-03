from selenium import webdriver
from scrapy.http import HtmlResponse
from retrying import retry

class TbSeleniumMiddleware(object):
	def __init__(self):
		self.driver = webdriver.Chrome() 

		# self.options = webdriver.ChromeOptions()
		# self.options.add_argument("--headless")
		# self.driver = webdriver.Chrome(chrome_options=self.options)

	@retry(stop_max_attempt_number=25, wait_fixed=200)
	def retry_load_page(self, request, spider):
		try:
			self.driver.find_element_by_xpath("//title")
		except:
			spider.logger.debug("Retry<{}>({}times)".format(request.url,self.num))
			self.num += 1
			raise Exception("<{}>page loading failed".format(request.url))

	def process_request(self, request, spider):
		self.num = 1
		self.driver.get(request.url)
		try:
			self.retry_load_page(request, spider)
			html = self.driver.page_source
			spider.logger.info("Retry <{}> Successful".format(request.url))
			return HtmlResponse(url=request.url, body=html.encode("utf-8"),encoding="utf-8", request=request)
		
		except Exception as e:
			spider.logger.error(e)
			return request

	def __del__(self):
		self.driver.quit()





