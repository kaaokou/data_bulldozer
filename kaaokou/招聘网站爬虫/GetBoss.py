# encoding:utf-8

import time
import random
import re
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from lxml import etree
from bs4 import BeautifulSoup


class Recruit(object):
    def __init__(self):
        self.base_url = 'http://www.zhipin.com/c101280600/h_101280600/?'
        self.detail_url = 'http://www.zhipin.com'
        self.detail_url_list = []
        self.page = 1
        self.position_count = 1
        self.position = raw_input("请输入需要抓取的职位名:")
        self.headers = {
            "authority": "www.zhipin.com",
            "method": "GET",
            # "path": "/c101280600/h_101280600/?query=python&page=8&ka=page-8",
            # "scheme": "https",
            # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            # "cache-control": "no-cache",
            # "cookie": "JSESSIONID=""; __c=1531376930; sid=sem_pz_bdpc_dasou_sublink20; __g=sem_pz_bdpc_dasou_sublink20; __l=r=https%3A%2F%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&l=%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3Dpython%26scity%3D101280600%26industry%3D%26position%3D&g=%2Fwww.zhipin.com%2Fp100205%2F%3Fsid%3Dsem_pz_bdpc_dasou_sublink20; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1531376920,1531377976; lastCity=101280600; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fc101280600%2Fh_101280600%2F%3Fquery%3Dpython%26page%3D8%26ka%3Dpage-8; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1531383254; __a=84352633.1531376914.1531376914.1531376930.79.2.78.74",
            # "pragma": "no-cache",
            # "referer": "https://www.zhipin.com/c101280600/h_101280600/?query=python&page=10&ka=page-next",
            # "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
        }

    def send_request(self):
        query_dict = {
            "query": self.position,
            "page": str(self.page),
            "ka": "page-" + str(self.page),
        }
        time.sleep(random.randint(2, 4))
        base_html = requests.get(self.base_url, params=query_dict, headers=self.headers).content
        return base_html

    def base_parse(self, base_html):
        html_object = etree.HTML(base_html)
        url_list = html_object.xpath('//div[@class="info-primary"]/h3[@class="name"]/a/@href')
        self.detail_url_list.append(url_list)
        print('页数为:')
        print(self.page)
        print(url_list)
        # 判断下一页是否还能爬取,如果是next，则说明还可以继续下一页
        flag_str = html_object.xpath('//div[@class="page"]/a[@ka="page-next"]/@class')[0]
        if flag_str == 'next':
            return True
        else:
            return False

    def send_detail_request(self, url):
        time.sleep(random.randint(3, 6))
        detail_html = requests.get(url, headers=self.headers)
        print ('正在爬取详情页')
        print(url)
        return detail_html.content

    def detail_pase(self, html):
        soup = BeautifulSoup(html, 'lxml')
        # 发布时间
        release_time = soup.select('span[class="time"]')[0].string
        # 岗位名称
        position_name = soup.select('div[class="job-primary detail-box"] > div[class="pos-bread"] > a')[-1].string
        message = soup.select('div[class="job-primary detail-box"] > div[class="info-primary"] > p')[0].get_text()
        # message 为unicode的》》》》 城市：深圳经验：1-3年学历：本科
        pattern = re.compile(u'\u57ce\u5e02\uff1a(.*?)\u7ecf\u9a8c\uff1a(.*?)\u5b66\u5386\uff1a(.*)')
        m = pattern.match(message)
        # 城市，经验，学历
        city = m.group(1)
        experience = m.group(2)
        education = m.group(3)
        company = soup.select('a[ka="job-detail-company"]')[0].get('title')
        # 公司信息（融资，人数，类型）
        company_information = soup.select('div[class="job-primary detail-box"] > div[class="info-company"] > p')[
            0].get_text()
        # 职位描述
        job_description = soup.select('div[class="job-sec"] > div[class="text"]')[0].get_text().strip()
        # 薪资
        html_object = etree.HTML(html)
        salary = \
            html_object.xpath(
                ' //div[@class="job-primary detail-box"]/div[@class="info-primary"]/div[@class="name"]/span')[0].text
        # 地址
        address = html_object.xpath(' //div[@class="location-address"]')[0].text
        return [position_name, salary, city, experience, education, company, address, company_information,
                job_description, release_time]

    def save(self, detail_list):
        with open('boss.csv', 'ab') as csvfile:
            print('正在存储第%s岗位信息' % self.position_count)
            writer = csv.writer(csvfile)
            if self.position_count == 1:
                writer.writerow(['岗位', '薪资', '城市', '工作经验', '学历', '公司', '工作地点', '公司信息', '岗位描述', '发布时间'])
            writer.writerow(detail_list)
            self.position_count += 1

    def main(self):
        while True:
            base_html = self.send_request()
            flag = self.base_parse(base_html)
            if flag is False:
                break
            self.page += 1
        for items in self.detail_url_list:
            for item in items:
                url = self.detail_url + item
                try:
                    html = self.send_detail_request(url)
                    print("已完成爬取详情页" + url)
                    detail_list = self.detail_pase(html)
                    self.save(detail_list)
                except Exception as e:
                    print('爬取%s出错' % url)
                    print('错误信息为', e)


if __name__ == '__main__':
    recruit = Recruit()
    recruit.main()
