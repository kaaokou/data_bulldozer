# encoding:utf-8
import requests
from lxml import etree
import sys
import random
import time
import redis

reload(sys)
sys.setdefaultencoding('utf-8')

# user_agent池
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
# 代理池
PROXYS = {
    "http": "http://183.167.217.152:63000",
    "http": "http://114.223.174.171:8118",
    "http": "http://61.157.136.105:808",
    "http": "http://118.190.95.35:9001",
    "http": "http://118.190.95.43:9001",
    "http": "http://101.37.79.125:3128",
    "http": "http://218.60.8.99:3129",
}


class JDSpider(object):
    def __init__(self, keyword):
        self.base_url = "https://search.jd.com/Search?"
        self.keyword = keyword
        self.page = 1
        self.query_params = {
            "keyword": self.keyword,
            "enc": "utf-8",
            "qrst": 1,
            "rt": 1,
            "stop": 1,
            "vt": 2,
            "wq": self.keyword,
            "click": 0,
            "scrolling": "y",
            "tpl": "3_M",
            # page=17(每次加2)
        }
        self.headers = {
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            # "cookie":"xtest=9504.cf6b6759; qrsc=3; __jdu=174844899; shshshfpa=6ee6aaf4-78ff-86d5-2957-133b783f96cf-1532233730; shshshfpb=0e1d9af95c0de127817c90536159d4976aad67bd741413f465b17b039b; ipLoc-djd=1-72-2799-0; PCSYCityID=1607; __jdc=122270672; user-key=7f0f427b-6970-45de-b0a7-a7f2bfb66ee0; cn=0; shshshfp=6a6b267ad4f50f296155fec8b9e647df; 3AB9D23F7A4B3C9B=4ZNQLGQKY26FMTYMB4D6GSJFCMN724BK3KGRR5LQCRUCUJDYG6BWT5S22TVK76NOL3O64ZWWJL6CDRGJI3JDJWEVDU; unpl=V2_ZzNtbUpWRxYnABJdchkIUmIKFgoSABFHfFhEA3oaVAM0ABFUclRCFXwUR11nGF4UZwcZXkdcRxxFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VH0cVQBiChpVcmdEJUU4RFF%2bGlgHVwIiXHIVF0l2CkNcfBwRBWEGG1hHXksdRQl2Vw%3d%3d; CCC_SE=ADC_7%2fbDYYmu4gHzHOqqIr44FTLj3Kcap%2bCN87n%2f2LRZb2FfVe1u1doCyqQw9F1ihpZgCQ6B01ShPsxycl1YVQZGzbEcCkRoZ3RbM9Py2RTLKhNNIM0VgjUUtw4dqK5yYohcbI2r1nByhzdW31veBLDPJOpyERkNuIXifOGUun0cVAONRVmUHzf8SgFhl8O%2bMdU5%2bu4SbC6jirDhyMN28Kts5a%2bqDXDb%2bzF%2bHE5cS%2b%2fT5MOyFX%2bi%2fdNR6j3ueQw10dBwGWdYWlWWN5X3dWlic3BT8nxBvjzlkqQW%2bpoY4eFC8d5z56N7%2fZVAe4eScz6iGTkUpbt8CtNKKeDf6CPBx%2bawTDhWYOfYRIZ55UOmuerdYiiw7gjEHiowBF9hujWEC3Cxlg4HgVPTsCrV1QHiT3csq%2bQIOGOeLrBFmW6HJJYfxGqykTy6QTs8hDwynu2zxGED5TTI98ZZLU768JQcIXzb6HDmkiHhQujtWHivWDye5837pQp5%2b6hB98%2foVhdJACn6KJV%2bQE1v7AlNIksnylXcmn4qoCl6TRVJlccLGyx8sfhaSe5yfRPnRL%2fEDPnxSWqjHYr%2b4WTuWLDH%2f3e0KTHqqApEFZs%2fh5tBacMs%2fDPCZ2WDffey1RhtMReyt7KZWYXMkpVUubye9AGezPHgypcSu0izvK5c%2bBBEgxqWv2V%2f1erX2PR801nLYSQNN5crg6I5sBRwG5bq7mN7xnMeV5OL2iuMGhSn1khzoJb0fhPZTxqumQCU2lu56ISmlxTJ5xsg; __jda=122270672.174844899.1524140070.1533267952.1533281101.18; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_9052c9e881ef485fafcc8a3f0297b228|1533281101014; rkv=V0400; mt_xid=V2_52007VwMUV1RdV1MXQSleUmVQQQdcC05aHx4YQABhCxFOVAoAXQNOGVsGYAUWBQpaUAovShhcDHsCG05cWkNaG0IaVA5mAiJQbVhiWRxPHlQAZAMUYl1dVF0%3D; __jdb=122270672.13.174844899|18.1533281101; shshshsID=8cc6ee504a1241febbc018fc47b8ea4d_10_1533281831506",
            "pragma": "no-cache",
            # referer -->车载
            "referer": "https://search.jd.com/Search?keyword=%E8%BD%A6%E8%BD%BD&enc=utf-8&wq=%E8%BD%A6%E8%BD%BD",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

    def send_request_top(self, page):
        """上方加载"""
        self.query_params["page"] = page
        data = requests.get(self.base_url, params=self.query_params, headers=self.headers, proxies=PROXYS)
        return data

    def send_request_buttom(self, sku, query_params, headers, page, referer_url):
        """下方加载"""
        # 补充log_id后面的时间戳，3位
        i = random.randint(100, 999)
        log_id = ""
        query_params["log_id"] = log_id.join([str(time.time()), str(i)])
        query_params["page"] = page + 1
        query_params['show_items'] = sku
        headers['referer'] = referer_url
        headers['User-Agent'] = random.choice(USER_AGENT_LIST)
        url = "https://search.jd.com/s_new.php?"
        data = requests.get(url, params=query_params, headers=headers, proxies=PROXYS).content
        return data

    def parse(self, data):
        """解析，提取商品sku"""
        html_obj = etree.HTML(data)
        sku = html_obj.xpath('//li[@class="gl-item"]/@data-sku')
        print(sku)
        return sku

    def save(self, sku):
        """将sku存储在redis"""
        r = redis.Redis(host="111.230.135.89", port=6379, db=1)
        r.sadd("jd_sku2", *sku)

    def main(self):
        while True:
            print(self.page)
            if self.page >= 200:
                break
            # 获取上方加载的商品sku
            data_top = self.send_request_top(self.page)
            sku = self.parse(data_top.content)
            # 获取下方加载的商品的sku
            data_buttom = self.send_request_buttom(sku, self.query_params, self.headers, self.page, data_top.url)
            sku2 = self.parse(data_buttom)
            self.save(sku + sku2)
            self.page += 2


if __name__ == '__main__':
    # keyword = input("请输入你要爬取的商品信息名字")
    spider = JDSpider("车载")
    spider.main()
