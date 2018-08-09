# coding=utf-8
"""
@author: kaaokou
"""
import re
import time
import json
import urllib
import random

from bs4 import BeautifulSoup
from jsonpath import jsonpath

import requests

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

PROXY_LIST = [
    # 添加代理
    # {"http": "http://maozhaojun:ntkn0npx@115.28.141.184:16816"}
]

CNT = 0


class LiePinSpider(object):
    """猎聘网网站爬取信息"""

    def __init__(self):
        self.dqs = raw_input('[INFO]请输入你需要查询职位的城市:广州[050020]深圳[050090]北京[010]上海[020]：')
        self.key = raw_input("[INFO]请输入你要查询的岗位名称：")
        self.end_page = int(raw_input("[INFO]请输入你要爬取的最大页面："))
        # https://www.lagou.com/jobs/list_web%E5%BC%80%E5%8F%91?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=
        self.base_referer = "https://www.lagou.com/jobs/list_"
        self.base_url = "https://www.liepin.com/zhaopin/?"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "subscribe_guide=1; abtest=0; _fecdn_=1; __uuid=1531396548780.97; _uuid=8E58EA68FFA842183324CA967E9FAF7D; 72101d64=a70b69fceaee2473177d28855fc89e85; user_kind=0; is_lp_user=true; user_vip=0; need_bind_tel=false; __tlog=1531396548781.55%7C00000000%7C00000000%7Cs_00_pz0%7CC_c_0015; _mscid=C_c_0015; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1531396549,1531396691; c6e713e1=716f247816e08cc94bbd1aa708af5498; dc81f4b2=fc4dcf8e8872c2d97c192199024f9d8f; user_name=%E5%91%A8%E5%86%9B; lt_auth=6bsMPXEBmV6qsSTbjTNXsf1Oho%2F5A2zP9S8NgRxVgte8XKW24PzmSwyGqbEGxBMhkRl2f8ULNLP%2F%0D%0ANuH4znJD60cXwGmulICyvvyk13seSORccfih0f%2BqkMrUF5QskHBSnSJipy1IxBj1tEZ3MY7qwFzI%0D%0Ap6HH7ral8vvE%0D%0A; UniqueKey=450d37cf296381bf1a667e00ad0d9493; verifycode=6da1347784ea4bcab4c93365e3e97982; user_photo=55557f3b28ee44a8919620ce01a.gif; c_flag=cdc26610a397b135a6a56c8e1534d681; new_user=false; login_temp=islogin; gr_user_id=e2847ebd-23e0-4273-b024-fe4b17fb1eb9; gr_session_id_bad1b2d9162fab1f80dde1897f7a2972=6fbb78b5-b789-4ffc-ab21-502101e3d7c6; gr_cs1_6fbb78b5-b789-4ffc-ab21-502101e3d7c6=UniqueKey%3A450d37cf296381bf1a667e00ad0d9493; imClientId=99f51fb236d1796ee246fff844942afd; imId=99f51fb236d1796ee4818c8f4811ed0a; fe_work_exp_add=true; JSESSIONID=C3B23B053CEF94717D0588BBEDCDE06D; __session_seq=40; __uv_seq=40; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1531398507",
            "Host": "www.liepin.com",
            "Pragma": "no-cache",
            "Referer": "https://www.liepin.com/zhaopin/?dqs=" + self.dqs + "&key=" + self.key,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",L, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.query_string = {
            "industries": "",
            "dqs": self.dqs,
            "salary": "",
            "jobKind": "",
            "pubTime": "",
            "compkind": "",
            "compscale": "",
            "industryType": "",
            "searchType": "1",
            "clean_condition": "",
            "isAnalysis": "",
            "init": "1",
            "sortFlag": "15",
            "flushckid": "0",
            "fromSearchBtn": "1",
            "headckid": "0b66b71c68ba35d0",
            "d_headId": "03bec3e08bfb796330ea15a9d4fce7d3",
            "d_ckId": "03bec3e08bfb796330ea15a9d4fce7d3",
            "d_sfrom": "search_unknown",
            "d_curPage": 0,
            "d_pageSize": "40",
            "siTag": "I-7rQ0e90mv8a37po7dV3Q~F5FSJAXvyHmQyODXqGxdVw",
            "key": self.key,
        }
        self.file_name = 'liepin_' + self.key + '.json'
        self.item_list = []

    def parse_html(self, html):
        """将可能被注释掉的html解注释"""
        pattern = re.compile(r'<!--|-->')
        html = pattern.sub('', html)
        return html

    def send_get_request(self, url):
        """get请求"""
        print('[INFO]:正在请求<{}>'.format(url))
        # 发送get请求
        proxies = random.choice(PROXY_LIST)
        headers = {
            "User-Agent": random.choice(USER_AGENT_LIST),
        }
        try:
            html = requests.get(url, headers=headers, proxies=proxies, params=self.query_string).content
        except Exception as e:
            print('[ERROR]:请求<{}>失败'.format(url))
            return ''

        html = self.parse_html(html)
        return html

    def parse_page(self, html):
        """处理json字典数据"""
        soup_obj = BeautifulSoup(html, 'lxml')
        position_list = soup_obj.select('.sojob-item-main')
        print(len(position_list))
        for position in position_list:
            item = {}
            item['name'] = position.select('h3')[0].get('title')
            href = position.select('h3 > a')[0].get('href')
            # 有可能出现链接不全的情况
            if href.startswith('http'):
                item['url'] = href
            else:
                item['url'] = 'https://www.liepin.com' + href
            item['salary'] = position.select('.text-warning')[0].get_text()
            item['site'] = position.select('.area')[0].get_text()
            item['education'] = position.select('.edu')[0].get_text()
            item['company_name'] = position.select('.company-name > a')[0].get_text()
            item['work_year'] = position.select('.condition > span')[2].get_text()
            item['create_time'] = position.select('.time-info > time')[0].get('title')
            item['summary'] = ''
            for tmp in position.select('.temptation > span'):
                item['summary'] += tmp.get_text() + ';'

            print(item['name'])
            # 开始处理详细页
            html = self.send_get_request(item['url'])

            item['detail'] = self.parse_detail(html)

            self.item_list.append(item)
            # TODO 添加延迟
            time.sleep(1)

    def parse_detail(self, html):
        """提取详情页面的岗位职责"""
        soup_obj = BeautifulSoup(html, 'lxml')
        try:
            detail = soup_obj.select('.job-description')[0].get_text()
        except Exception:
            print('[INFO]:解析详细页失败')
            global CNT
            CNT += 1
            return '解析详细页失败'

        detail = detail.strip()
        return detail

    def save_data(self):
        """保存数据"""
        print("[INFO]正在写入<{}>数据".format(self.file_name))
        json.dump(self.item_list, open(self.file_name, 'w'))

    def main(self):
        """类启动方法"""
        # 1.发送请求
        page = 0
        while page < self.end_page:
            if page != 0:
                # 比page小1
                self.query_string['d_curPage'] = page - 1
            if page != 0:
                # 0的时候不显示这个值
                self.query_string['curPage'] = page
            html = self.send_get_request(self.base_url)
            self.parse_page(html)
            page += 1
            time.sleep(random.randint(3, 6))

        # 2.写入文件
        self.save_data()
        print('[INFO]:一共被发现<{}>次请求'.format(CNT))

        # 3.抬头，望天。。。
        print('[INFO]: 抬头，望天。。。')


if __name__ == '__main__':
    spider = LiePinSpider()
    spider.main()
