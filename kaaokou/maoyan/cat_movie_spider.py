# -*- coding:utf-8 -*-
"""
@author: kaaokou
参考文章：https://darknode.in/font/font-tools-guide/
https://zhuanlan.zhihu.com/p/33112359
使用woff2otf下载：https://github.com/hanikesn/woff2otf
"""
import json
import re
import requests

from fontTools.ttLib import TTFont

from bs4 import BeautifulSoup

import woff2otf


def generate_base_woff(url):
    """解析猫眼电影的woff文件"""
    font_maoyan = TTFont('base.woff')
    font_maoyan.saveXML('base.xml')


class CatMovieSpider(object):
    """
    爬取猫眼电影票房 v1.0  http://maoyan.com/board/1
    @author: kaaokou
    """

    def __init__(self):
        # 爬取之前的字体基本处理
        self.base_font = TTFont('base.otf')
        self.base_num_list = ['.', '9', '2', '8', '6', '3', '0', '5', '4', '1', '7']
        self.base_unicode = ['x', "uniE136", "uniE2CF", "uniE693", "uniE759", "uniEB60", "uniED12", "uniEFEE",
                             "uniEFFE", "uniF489", "uniF6B8"]
        self.base_url = "http://maoyan.com/board/1"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "uuid=1A6E888B4A4B29B16FBA1299108DBE9C3587DA91FBF3AB123680CEFB8DA24B9E; _lxsdk_cuid=1648bd21e375-07b6c53512ae62-163e6952-fa000-1648bd21e38c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9C3587DA91FBF3AB123680CEFB8DA24B9E; _csrf=ea31121ac86563baaaf1bc8cba0948f7aae15035dadc232c9c9272662d28634e; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=215398952.1531354160868.1531454335016.1531454550707.73; _lxsdk_s=1649160f1e4-4dd-e0e-7e8%7C%7C30",
            "Host": "maoyan.com",
            "Pragma": "no-cache",
            "Referer": "http://maoyan.com/board",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        # 保存的文件名
        self.file_name = 'cat_movie.json'
        # 提取woff字体url链接的正则表达式以及提取字体的表达式
        self.font_url_pattern = re.compile("'(//vfile.meituan.net/colorstone/([0-9a-f]{36}).+?woff)'")
        self.font_pattern = re.compile('&#x[0-9a-f]{4};')
        # 将字体的值对应到替换规则，maps缓存woff字体内容
        self.maps = {}
        # 列表，保存爬取的信息，然后写入json
        self.item_list = []

    def parse_html(self, html):
        """将可能被注释掉的html解注释"""
        pattern = re.compile(r'<!--|-->')
        html = pattern.sub('', html)
        return html

    def send_request(self, url, params={}):
        """发送url请求，得到html"""
        print('[INFO]:正在请求<{}>'.format(url))
        try:
            html = requests.get(url, params=params, headers=self.headers).content
        except Exception as e:
            print('[ERROR]:请求<{}>失败'.format(url))
            return None
        # 处理html，防止html中被注释的可能
        html = self.parse_html(html)
        return html

    def parse_stonefont(self, html):
        """将原html中的stonefont替换为正常数字"""
        # 1.得到woff的url以及提取的随机woff码值(用于记录缓存)
        url, digest = self.font_url_pattern.search(html).groups()

        # 2.获取font字体
        font_url = 'http:' + url
        callback = self.get_font_regx(digest, font_url)

        # 3.将原html中的font字体替换
        html = self.font_pattern.sub(callback, html)
        return html

    def get_font_regx(self, digest, font_url):
        """解析当次请求的woff"""
        if digest in self.maps:  # 缓存
            print("[INFO]:该文件已有缓存，坐等！！！")
            return self.maps[digest]
        # attention:这个请求不要添加任何的请求头
        html = requests.get(font_url).content

        # 1.将请求得到的woff保存为本地文件
        with open('cat_movie.woff', 'w') as fw:
            fw.write(html)
        # 转换woff字体为otf字体
        woff2otf.convert('cat_movie.woff', 'cat_movie.otf')

        # 2.对比此次请求的otf与本地的otf，提取有效数据
        maoyan_font = TTFont('cat_movie.otf')
        uni_list = maoyan_font['cmap'].tables[0].ttFont.getGlyphOrder()
        num_list = []

        for i in range(1, 12):
            # 获取当前页面的字体
            maoyan_glyph = maoyan_font['glyf'][uni_list[i]]
            # 与数据库中的进行比对，查看是否一致
            for j in range(11):
                base_glyph = self.base_font['glyf'][self.base_unicode[j]]
                if maoyan_glyph == base_glyph:
                    num_list.append(self.base_num_list[j])
                    break
        # uni_list[1] = 'uni0078'
        # 3.将font编码与对应的值记录字典
        mappings = {}
        for index in range(1, 11):
            mappings['&#x{};'.format(uni_list[index + 1][3:].lower())] = num_list[index]

        # 4.闭包，也可以返回记录的字典，遍历替换
        def callback(regx):
            # 取font_pattern匹配到的内容
            return mappings.get(regx.group(0), regx.group(0))

        self.maps[digest] = callback
        return callback

    def parse_page(self, html):
        """处理替换成可识别数据之后的html"""
        soup_obj = BeautifulSoup(html, 'lxml')
        film_list = soup_obj.select('.board-item-content')
        for film in film_list:
            item = {}
            item['name'] = film.select('.name')[0].get_text()
            item['star'] = film.select('.star')[0].get_text()
            item['releasetime'] = film.select('.releasetime')[0].get_text()
            item['realtime'] = film.select('.name')[0].get_text()
            # 处理实时票房
            item['realtime'] = film.select('.realtime')[0].get_text().strip()
            # 处理总票房
            item['totaltime'] = film.select('.total-boxoffice')[0].get_text().strip()

            self.item_list.append(item)

    def save_data(self):
        """保存爬取下来的数据文件"""
        print("[INFO]:正在保存数据<{}>".format(self.file_name))
        json.dump(self.item_list, open(self.file_name, 'w'))

    def main(self):
        """程序入口，主逻辑控制"""
        html = self.send_request(self.base_url)
        html = self.parse_stonefont(html)
        # 提取处理之后html中的内容
        self.parse_page(html)
        self.save_data()
        print('[INFO]:抬头，望天。。。')


if __name__ == "__main__":
    spider = CatMovieSpider()
    spider.main()
