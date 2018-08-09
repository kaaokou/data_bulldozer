# coding=utf-8
"""
@author: kaaokou
"""
import base64
import re
import json
import os

import gevent
import requests
from Crypto.Cipher import AES
from jsonpath import jsonpath
from gevent import monkey
from proxy_list import PROXY_LIST, USER_AGENT_LIST
# 打补丁
monkey.patch_all()


class WangYiSpider(object):
    """网易音乐爬虫"""

    def __init__(self):
        self.search_url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        self.play_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        self.first_form_data = {
            's': raw_input('[INFO]:请输入你要查询的歌曲名称: '),
            'offset': 0,
            'limit': 10,
            'type': '1',
            "total": "true",
            "hlpretag": "",
            "hlposttag": "",
            'csrf_token': ''
        }
        # 三个常量
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pubKey = '010001'
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.headers = {
            "Accept": "*/*",
            # "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "592",
            "Content-Type": "application/x-www-form-urlencoded",
            # "Cookie": "usertrack=ezq0o1tEb6OZBSXPCDwbAg==; _ntes_nnid=67fdbde41dbb4375883a93df057e15ff,1531211690410; _ntes_nuid=67fdbde41dbb4375883a93df057e15ff; _iuqxldmzr_=32; __f_=1532268843641; vjuids=3627b59e6.164c6618779.0.a715e2f8dd624; vjlast=1532336638.1532412288.13; vinfo_n_f_l_n3=e6dfb93b77ddb1cc.1.1.1532336652227.1532415218782.1532430088253; WM_TID=j7w%2FOjXiPFhdivWqT1tCLppZCDB2Ided; __utmc=94650624; __utma=94650624.375537227.1531658149.1532515280.1532520093.5; __utmz=94650624.1532520093.5.4.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/lifeifei1245/article/details/75208748; WM_NI=nY3qDY4fsuO1wkqb2vX4M8f1RteXfxUithbBaVk9%2Fg%2FlS8mdr4eRWaCOt%2B2QAZ20XmwQ4AEYcB0lRPaP5b9g2gKgXtgs7t6IsWNV9F08q%2BbduxC%2FRJZXHo6lcbsfwJJCNWU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeaff84fa8ecbcdaec74fb8c9a8fce4fa8a8a0b3c54d8aa68595d17b93ebbdd0b42af0fea7c3b92aae87fd92c753f8babd96ce3bb5b5bf83b17e9cec83d9e53b92acabb9e57497b7bc89e14aa38aa5daae6dedb49dd9f070b2ecabb3d66b8191bcccb15b8386fed1db67b58ffca2c853a19e008dd15ca390fb83bc6df2b98588db80a5adf995b543b18982b7bc4ef4e8bfcce170b7a88dd0d1429a888890b568a1bebd87f6428a9d82b8d837e2a3; JSESSIONID-WYYY=cq%5C9Vgd7noxXj4Gb4JzdraAwx9Jloaw%2FPF5A6fzITY6wedsT5D4zDvYbDhYR%5CxG8ih5R9%2B8bThbBXXQHnBaFtTA6ShCu%2BQR2jpZicagT%2BHKJhjW9arApd1kjlIw7rhAmrRDdqM1F5okP9J3WaJm6wJlRUmTFIk%2ByMRssFjdC92bIGct4%3A1532523338362; __utmb=94650624.12.10.1532520093; playerid=19953584",
            "Host": "music.163.com",
            "Origin": "http://music.163.com",
            "Pragma": "no-cache",
            "Referer": "http://music.163.com/search/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        # 创建保存数据的文件夹
        self.path = 'wangyi_musics'
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def parse_html(self, html):
        """将可能被注释掉的html解注释"""
        pattern = re.compile(r'<!--|-->')
        html = pattern.sub('', html)
        return html

    def send_get_request(self, url):
        """发送get请求"""
        print('[INFO]:正在请求<{}>'.format(url))
        html = requests.get(url).content
        # print(html)
        return html

    def send_post_request(self, url, form_data):
        """post请求，获取歌曲数据"""
        print('[INFO]:正在请求<{}>'.format(url))
        # 生成加密的请求data
        post_data = self.generate_postdate(form_data)
        python_obj = requests.post(url, data=post_data, headers=self.headers).json()
        # print(python_obj)
        return python_obj

    def generate_postdate(self, form_data):
        """生成enc_text和enc_seckey，从而构建postdata"""
        json_data = json.dumps(form_data)
        sec_key = self.create_random_secrekey(16)
        enc_text = self.aes_encrypt(self.aes_encrypt(json_data, self.nonce), sec_key)
        enc_seckey = self.rsa_encrypt(sec_key, self.pubKey, self.modulus)
        # 开始发送
        post_data = {
            'params': enc_text,
            'encSecKey': enc_seckey,
        }
        return post_data

    def parse_data(self, python_obj):
        """显示结果"""
        song_list = jsonpath(python_obj, '$..songs')
        song_data_list = []
        for song in song_list[0]:
            song_data = {
                'form_data': {
                    # 歌曲id
                    'ids': '[' + str(song['id']) + ']',
                    # 歌曲品质
                    'br': 128000,
                    # 'br': 320000,
                    'csrf_token': '',
                },
                'name': song['name'].encode('utf-8'),
                'auth': song['ar'][0]['name'].encode('utf-8')
            }
            song_data_list.append(song_data)

        return song_data_list

    def parse_url(self, python_obj):
        """提取url地址"""
        url = ''
        if python_obj.get('code') == 200:
            try:
                url = python_obj['data'][0]['url'].encode('utf-8')
            except:
                pass
        return url

    def download_manage(self, song_list):
        """处理下载的歌曲"""
        download_list = []
        # 1.打印歌曲
        for index, song in enumerate(song_list):
            print("[INFO]:{}、歌手：[{}]--<{}>".format(index + 1, song['auth'], song['name']))
        # 2.等待用户选择
        download_choice = raw_input("[INFO]:请选择你要下载的歌曲[如：1,2,3或输入all全部下载]: ")
        if download_choice == "all":
            print("[INFO]:你选中的歌曲为全部。。。")
            download_list = song_list
        else:
            download_choice_list = download_choice.split(",")  # 一次多个下载，切分字符串
            print("[INFO]:你选中的歌曲：")
            for download_index in download_choice_list:
                song_info = song_list[int(download_index) - 1]
                print("[INFO]: 歌手：[{}]--<{}>".format(song_info['auth'], song_info['name']))
                download_list.append(song_info)
        return download_list

    def download_song(self, download):
        """获取download数据，下载"""
        # 1.发送请求
        print('[INFO]:正在下载[{}]'.format(download['name']))
        data = self.send_get_request(download['url'])
        # 2.保存数据
        file_name = self.path + '/' + download['name'] + '-' + download['auth'] + '.mp3'
        with open(file_name, 'wb') as fw:
            fw.write(data)
        print('[INFO]:歌曲<{}>下载完成'.format(download['name']))

    def create_random_secrekey(self, size):
        """生成随机长度的字符串"""
        sstr = (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]
        return sstr

    def aes_encrypt(self, text, sec_key):
        """由随机生成的sec_key生成encText"""
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(sec_key, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def rsa_encrypt(self, text, pubKey, modulus):
        """利用随机数加密生成encSecKey"""
        text = text[::-1]
        rs = int(text.encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def main(self):
        """类启动方法"""
        # 1.发送请求
        python_obj = self.send_post_request(self.search_url, self.first_form_data)

        # 2.解析得到的结果
        song_list = self.parse_data(python_obj)

        # 3.询问用户，需要下载哪些
        if len(song_list) == 0:
            print('[INFO]:查询的歌曲为空')
            return
        download_list = self.download_manage(song_list)

        # 4.发送链接，下载
        spawn_list = []
        for download in download_list:
            # 获取下载链接
            python_obj = self.send_post_request(self.play_url, download['form_data'])
            # 解析获得播放url
            url = self.parse_url(python_obj)
            if not url:
                print('[ERROR]:歌曲<{}>受到版权保护，无法获取链接...'.format(download['name']))
                continue
            download['url'] = url
            spawn = gevent.spawn(self.download_song, download)
            spawn_list.append(spawn)

        # 5.等待下载结束
        gevent.joinall(spawn_list)

        # 6.抬头，望天
        print('[INFO]:抬头，望天...')


if __name__ == '__main__':
    spider = WangYiSpider()
    spider.main()