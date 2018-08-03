# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import sys

import time

reload(sys)
sys.setdefaultencoding('utf-8')

from scrapy.http import HtmlResponse
from scrapy import signals
from selenium import webdriver
from retrying import retry


class JDSeleniumMiddleware(object):
    """模拟浏览器下载中间件"""

    def __init__(self):
        self.driver = webdriver.Chrome()
        # 设置浏览器宽高
        self.driver.set_window_size(1232, 8392)

    @retry(stop_max_attempt_number=30, wait_fixed=200)
    def retry_load_page(self, request, num, spider):
        """尝试加载页面"""
        # 如果没有找到会抛出异常
        try:
            xpath_pattern = "//div[@id='J_goodsList']/ul/li[%d]" % ((num - 1) * 4 + 1)
            self.driver.find_element_by_xpath(xpath_pattern)
        except Exception:
            spider.logger.debug('Retry<{}>(<{}>)'.format(request.url, self.cnt))
            self.cnt += 1
            raise Exception("<{}> page loading failed.".format(request.url))

    def process_request(self, request, spider):
        """处理请求，不再通过直接请求，通过selenium自己渲染浏览器"""
        if not request.url.startswith('https://www.jd.com'):
            self.cnt = 1
            self.is_slide = False
            self.driver.get(request.url)
            num = 1
            while num < 16:
                try:
                    # 开始尝试加载页面
                    print('****' * 30)
                    self.retry_load_page(request, num, spider)
                except Exception as e:
                    spider.logger.error(e)
                    return request
                # 往下滑动
                js = "window.scrollBy(0, %d);" % random.randint(450, 470)
                time.sleep(0.5)
                self.driver.execute_script(js)
                num += 1
            # 响应的页面
            html = self.driver.page_source
            spider.logger.info("Retry <{}> Successful".format(request.url))
            # 直接返回解析的对象，指定编码为utf-8，交给spider自动解析成unicode
            return HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8', request=request)

    def __del__(self):
        """析构函数，关闭浏览器"""
        self.driver.quit()
