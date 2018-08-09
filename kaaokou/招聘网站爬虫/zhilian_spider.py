# coding:utf-8
import json
import random

from bs4 import BeautifulSoup
from lxml import etree

import chardet
import time
from jsonpath import jsonpath
import requests

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class zhilian_spider():
    def __init__(self):
        self.url = "https://fe-api.zhaopin.com/c/i/sou?"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,en-US;q=0.8,en;q=0.6,zh;q=0.4",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "sts_deviceid=164915843953c9-0dae8d73f259c1-3f63440c-1440000-164915843961fb; sts_sg=1; ZP_OLD_FLAG=false; LastCity=%E6%B7%B1%E5%9C%B3; LastCity%5Fid=765; GUID=4447beb510f44de4bc6f964dc0392236; ZL_REPORT_GLOBAL={%22sou%22:{%22actionIdFromSou%22:%22cd28cbf5-6d33-4e1b-a78c-9c6b617821ff-sou%22%2C%22funczone%22:%22smart_matching%22}}; sts_evtseq=4; sts_sid=1649158517e656-004243b0aafbd4-3f63440c-1440000-1649158517f710; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1531446842; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1531446847",
            "Host": "fe-api.zhaopin.com",
            "Upgrade-Insecure-Requests": "1",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"

        }
        self.dHeaders = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,en-US;q=0.8,en;q=0.6,zh;q=0.4",
            "cookie": "sts_deviceid=164915843953c9-0dae8d73f259c1-3f63440c-1440000-164915843961fb; sts_sg=1; ZP_OLD_FLAG=false; LastCity=%E6%B7%B1%E5%9C%B3; LastCity%5Fid=765; GUID=62933ea1af5543c7b849f4876d01259c; ZL_REPORT_GLOBAL={%22sou%22:{%22actionIdFromSou%22:%224f774d6f-3b37-4df7-8c90-0e030d052513-sou%22%2C%22funczone%22:%22smart_matching%22}}; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1531446842; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1531459739; zp_src_url=https%3A%2F%2Ffe-api.zhaopin.com%2Fc%2Fi%2Fsou%3FpageSize%3D60%26cityId%3D765%26workExperience%3D-1%26education%3D-1%26companyType%3D-1%26employmentType%3D-1%26jobWelfareTag%3D-1%26kw%3DPython%26kt%3D3%26lastUrlQuery%3D%257B%2522jl%2522%3A%2522765%2522%2C%2522kw%2522%3A%2522Python%2522%2C%2522kt%2522%3A%25223%2522%257D; dywez=95841923.1531472521.1.1.dywecsr=sou.zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; BLACKSTRIP=yes; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; dywea=95841923.3176157796715989500.1531472521.1531528026.1531532662.4; dywec=95841923; Hm_lvt_80e552e101e24fe607597e5f45c8d2a2=1531473797,1531473810,1531473863,1531473949; Hm_lpvt_80e552e101e24fe607597e5f45c8d2a2=1531532662; referrerUrl=; stayTimeCookie=1531532682376",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        }
        self.page = 1
        self.item_list = []
        self.url_switch = 0


    def create_url(self):
        self.url_switch = 0
        page = self.page * 60
        querystring = {
            "pageSize": page,
            "cityId": "765",
            "workExperience": "-1",
            "education": "-1",
            "companyType": "-1",
            "employmentType": "-1",
            "jobWelfareTag": "-1",
            "kw": "Python",
            "kt": "3",
            "lastUrlQuery": '{"jl":"765","kw":"Python","kt":"3"}',
        }
        return querystring



    def send_request(self,url = None,querystring=None,headers=None):
        if self.url_switch == 0:
            url = self.url
            headers =self.headers
            print("[INFO]: 正在发送第 {} 页请求".format(self.page))
        # elif self.url_switch == 1:
        #     print("[INFO]: 正在发送第 {} 页详情页请求".format(self.page))

        html = requests.get(url = url,params=querystring,headers=headers)

        if self.url_switch == 0:
            html = html.json()
        elif self.url_switch == 1:
            html = html.content


        return html



    def positionURL(self, position_url):
        self.url_switch = 1

        xxpage = self.send_request(url=position_url,headers = self.dHeaders)
        # print xxpage
        detail_txt = self.parse_page2(xxpage)

        self.url_switch = 0
        return detail_txt


    def parse_page(self, python_obj):
        position_list = jsonpath(python_obj,"$..results")[0]

        for position in position_list:
            item = {}
            item["salary"] = position["salary"]
            item["city"] = position["city"]['items'][0]["name"]
            item["positionName"] = position["jobName"]
            item["district"] = position["city"]['display']
            item["companyFullName"] = position["company"]["name"]
            item["createTime"] = position["createDate"]



            position_url = position["positionURL"]
            detail = self.positionURL(position_url)
            # 将列表detail转换成str文本
            txt = ""
            for text in detail:
                txt = txt + str(text)

            item["detail"] = txt
            # print (txt)

            self.item_list.append(item)

        return position_list

    def parse_page2(self, python_obj):

        html_obj = etree.HTML(python_obj)
        detail = html_obj.xpath('//div[@class="pos-ul"]/p//text()')


        print ("detail:  ",detail)


        return detail



    def save_data(self):
        # html = json.loads(html)
        json.dump(self.item_list, open("zhilian.json", "w"))


    def main(self):
        while self.page <= 2:
            querystring = self.create_url()
            html = self.send_request(querystring=querystring)
            # time.sleep(random.randint(1, 3))
            self.parse_page(html)
            self.page += 1

        self.save_data()
        print len(self.item_list)


if __name__ == '__main__':
    spider = zhilian_spider()
    spider.main()
