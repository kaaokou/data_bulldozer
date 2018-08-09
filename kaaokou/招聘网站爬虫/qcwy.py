# coding:utf-8
import requests
import json

from bs4 import BeautifulSoup
from lxml import etree


class QcwuSpider(object):
    def __init__(self):
        self.base_url = "https://search.51job.com/list/040000,000000,0000,01,9,99,python,2,"
        self.page = 1
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "guid=15314677797249220091; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fwww.baidu.com%252Fbaidu.php%253Fsc.0s0000KlmKuCTsdU2UX3nwvAh7_wVrcy2sDurO14YCZlG7kTdkDbQ9P63qLULr4tz0SM29YPckVHwooc5wrDM7ihhdHjiIU8ufXThw5-FcZJCgLAfubvcoiHd0JpC4NlQzdZkeINiduB4WUg7jx8Jd9GwMLvmidSTfz4h34dOWTsddvI_s.DY_NR2Ar5Od66CHnsGtVdXNdlc2D1n2xx81IZ76Y_NdSrHxvU8orgAs1SOOo_9OxOBI5lqAS61kO56OQS9qxuxbSSjO_uPqjqxZOg7SEWSyWxSrSrOFIqZO03OqWCOgGJ_EOU3c54DgSdq7Ol7UOSkSLweUEvOovqXdWujyhk5W_zggun-YPOub8LS2yThieGHYqhOkRdrYG4TXGmuCyrMW_vI26.U1Yk0ZDqdIjA8nL3dU30TA-W5HD0IjLNYnp31xWNE6KGUHYznWR0u1dBugK1n0KdpHdBmy-bIfKspyfqP0KWpyfqrHn0UgfqnH0kndtknjDLg1DsnH-xnH0YP7t1PW0k0AVG5H00TMfqrHms0ANGujYkPjRYg1cvPjnzg1cknj63g1cvn1Rsg1cznjTz0AFG5HcsP0KVm1YknHb4rHcvPHwxP1m1nj6vnHbvg1Dsnj7xnH0zg100TgKGujYs0Z7Wpyfqn0KzuLw9u1Ys0A7B5HKxn0K-ThTqn0KsTjYknHb4P1T4n1cz0A4vTjYsQW0snj0snj0s0AdYTjYs0AwbUL0qn0KzpWYs0Aw-IWdsmsKhIjYs0ZKC5H00ULnqn0KBI1Ykn0K8IjYs0ZPl5fKYIgnqnHnsrHnvnHRYnHn3PWD3PHfsnWc0ThNkIjYkPHnkPjmLP1m3nWfd0ZPGujdBmvDkn1nvuj0snj0sPvm40AP1UHY4rRRznWK7nHFawHfknH0Y0A7W5HD0TA3qn0KkUgfqn0KkUgnqn0KlIjYs0AdWgvuzUvYqn7tsg1KxnH0YP-ts0Aw9UMNBuNqsUA78pyw15HKxn7tsg1nkP16YnNts0ZK9I7qhUA7M5H00uAPGujYs0ANYpyfqQHD0mgPsmvnqn0KdTA-8mvnqn0KkUymqn0KhmLNY5H00uMGC5H00uh7Y5H00XMK_Ignqn0K9uAu_myTqnfK_uhnqn0KWThnqnHm1PjR%2526ck%253D9246.1.84.206.145.203.142.232%2526shh%253Dwww.baidu.com%2526sht%253Dbaiduhome_pg%2526us%253D1.0.1.0.1.300.0%2526wd%253D%2525E6%25258B%25259B%2525E8%252581%252598%2525E7%2525BD%252591%2525E7%2525AB%252599%2526issp%253D1%2526f%253D3%2526ie%253Dutf-8%2526rqlang%253Dcn%2526tn%253Dbaiduhome_pg%2526oq%253D58%252525E5%25252590%2525258C%252525E5%2525259F%2525258E%2526inputT%253D6871%2526prefixsug%253D%252525E6%2525258B%2525259B%252525E8%25252581%25252598%252525E7%252525BD%25252591%252525E7%252525AB%25252599%2526rsp%253D2%2526bc%253D110101%26%7C%26adsnum%3D1172945; partner=www_hao123_com; 51job=cenglish%3D0%26%7C%26; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60040000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA040000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA01%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1531468984%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA040000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1531468916%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21",
            "Host": "search.51job.com",
            "Pragma": "no-cache",
            "Referer": "https://search.51job.com/list/040000,000000,0000,01,9,99,python,2,8.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
        }
        self.infor_list = []

    def send_request(self, url):
        """发送请求"""
        # print("正在发送第 {} 页请求.".format(self.page))
        # print("正在发送...")
        format_data = {
            "lang": "c",
            "stype": "1",
            "postchannel": "0000",
            "workyear": "99",
            "cotype": "99",
            "degreefrom": "99",
            "jobterm": "99",
            "companysize": "99",
            "lonlat": "0,0",
            "radius": "-1",
            "ord_field": "0",
            "confirmdate": "9",
            "fromType": "",
            "dibiaoid": "0",
            "address": "",
            "line": "",
            "specialarea": "00",
            "from": "",
            "welfare": ""
        }
        print("[INFO]:正在请求<{}>".format(url))
        html = requests.get(url, params=format_data, headers=self.headers).content
        return html

    def parse_html(self, html):
        """提取html"""
        soup = BeautifulSoup(html, "lxml")
        # node_list = soup.select('div[id="resultList"]>div[class="el"]')
        node_list = soup.select('.dw_table > .el')
        node_list = node_list[1:]
        for node in node_list:
            infor_dict = {}
            infor_dict["detail_infor_link"] = node.select("a")[0].get("href")
            infor_dict["position_name"] = node.select("a")[0].string
            infor_dict["company_link"] = node.select("a")[1].get("href")
            infor_dict["company_name"] = node.select("a")[1].get_text()
            infor_dict["company_location"] = node.select('.t3')[0].get_text()
            infor_dict["position_salary"] = node.select("span")[2].string
            infor_dict["release_time"] = node.select("span")[3].string
            self.infor_list.append(infor_dict)

        # 判断是否最后一页
        # if soup.select('li[class="bk"] > a') is None:
        #     return False
        selector = etree.HTML(html)
        next_link = selector.xpath('//li[@class="bk"][2]/a/@href')
        print(next_link)
        if len(next_link) == 0:
            return False
        return next_link[0]

    def save_cont(self):
        print("正在保存..")
        json.dump(self.infor_list, open("tencent.json", "w"))

    def main(self):
        """调度器"""
        url = self.base_url + str(self.page) + ".html"
        html = self.send_request(url)

        a = 1
        while True:
            print("第%d次爬取.." % a)
            next_link = self.parse_html(html)
            if next_link == False:
                print("此处为最后一页..")
                break
            html = self.send_request(next_link)
            a += 1

        self.save_cont()
        print("已经保存到文件，请查收！")

if __name__ == '__main__':
    spider = QcwuSpider()
    spider.main()
