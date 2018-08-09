# coding=utf-8
"""
@author: kaaokou
"""
import random
import json
import os
import urllib

import gevent
import requests
from gevent import monkey

from proxy_list import PROXY_LIST, USER_AGENT_LIST

# 打补丁
monkey.patch_all()


class QQSpider(object):
    """QQ音乐爬虫"""

    def __init__(self):
        # 搜索url
        self.search_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?'
        # 获取vkey的url
        self.vkey_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?'
        # 播放连接
        self.play_url = 'http://dl.stream.qqmusic.qq.com/'
        self.search_referer = "https://y.qq.com/portal/search.html"
        self.play_referer = 'https://y.qq.com/portal/player.html'
        # 请求头
        self.headers = {
            "accept": "*/*",
            # "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            # "cookie": "pgv_pvi=3687925760; ptui_loginuin=1512227073; pt2gguin=o1512227073; RK=BjJA1RxlSG; ptcz=208f2f54757494700de12ae49f28483b9c59faaa4c9df5ab6dfd1c4b0073f4a9; pgv_pvid=5677617016; ts_refer=www.baidu.com/link; ts_uid=9562069203; yq_index=0; yqq_stat=0; pgv_si=s5895376896; pgv_info=ssid=s5518822884; player_exist=1; qqmusic_fromtag=66; yplayer_open=0; ts_last=y.qq.com/portal/search.html",
            "pragma": "no-cache",
            "referer": "https://y.qq.com/portal/search.html",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        }
        # 查询参数
        self.query_params = {
            "w": raw_input('[INFO]:请输入你要查询的关键字: '),
            "ct": "24",
            # 版本
            "qqmusic_ver": "1298",
            "new_json": "1",
            "remoteplace": "txt.yqq.song",
            "searchid": "66261832087801237",
            "t": "0",
            "aggr": "1",
            "cr": "1",
            "catZhida": "1",
            "lossless": "0",
            "flag_qc": "0",
            "p": "1",
            "n": "20",
            "g_tk": "5381",
            "jsonpCallback": "MusicJsonCallback7914284737637065",
            "loginUin": "0",
            "hostUin": "0",
            "format": "jsonp",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": "0",
            "platform": "yqq",
            "needNewCode": "0",
        }
        # 获取vkey的参数
        self.vkey_params = {
            # 随机16位数字
            "jsonpCallback": "MusicJsonCallback703233127722865",
            "callback": "MusicJsonCallback703233127722865",
            # mid值
            "songmid": "003OUlho2HcRHC",
            # C400 + mid
            "filename": "C400003OUlho2HcRHC.m4a",
            "g_tk": "5381",
            "loginUin": "0",
            "hostUin": "0",
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": "0",
            "platform": "yqq",
            "needNewCode": "0",
            "cid": "205361747",
            "uin": "0",
            "guid": "5677617016",
        }
        # 获取播放链接的参数
        self.play_params = {
            "vkey": '',
            "guid": "5677617016",
            "uin": "0",
            "fromtag": "66",
        }
        self.num = '01234567890123456789'
        # 创建保存数据的文件夹
        self.path = 'qq_musics'
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def send_get_request(self, url, query_params={}):
        """发送get请求"""
        print('[INFO]:正在请求<{}>'.format(url))
        html = requests.get(url, params=query_params, headers=self.headers).content
        return html

    def parse_data(self, html):
        """解析歌曲列表"""
        html = html[html.find('(') + 1:html.rfind(')')]
        python_obj = json.loads(html)
        song_data_list = python_obj['data']['song']['list']
        song_list = []
        for song_data in song_data_list:
            song = {
                'name': song_data['name'].encode('utf-8'),
                'auth': song_data['singer'][0]['name'].encode('utf-8'),
                'songmid': song_data['mid'].encode('utf-8'),
                'filename': 'C400' + song_data['mid'].encode('utf-8') + '.m4a',
                'url': ''
            }
            song_list.append(song)
        return song_list

    def parse_url(self, html):
        """解析出播放地址"""
        # 字符串截取
        html = html[html.find('(') + 1:html.rfind(')')]
        python_obj = json.loads(html)
        filename = python_obj['data']['items'][0]['filename'].encode('utf-8')
        vkey = python_obj['data']['items'][0]['vkey'].encode('utf-8')
        # 如果获取不到vkey，则表示出错了
        if not vkey:
            return ''
        # 拼接url
        self.play_params['vkey'] = vkey
        url = self.play_url + filename + '?' + urllib.urlencode(self.play_params)
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
        file_name = self.path + '/' + download['name'] + '-' + download['auth'] + '.m4a'
        with open(file_name, 'wb') as fw:
            fw.write(data)
        print('[INFO]:歌曲<{}>下载完成'.format(download['name']))

    def create_random_num(self, size):
        """生成随机长度的字符串"""
        random_num = ''.join(random.sample(self.num, size))
        return random_num

    def process_vkey_params(self, download):
        """处理vkey的参数"""
        random_num = self.create_random_num(16)
        self.vkey_params['jsonpCallback'] = 'MusicJsonCallback' + random_num
        self.vkey_params['callback'] = 'MusicJsonCallback' + random_num
        self.vkey_params['songmid'] = download['songmid']
        self.vkey_params['filename'] = download['filename']

    def main(self):
        """类启动方法"""
        # 1.查询获取歌曲信息
        html = self.send_get_request(self.search_url, self.query_params)

        # 2.解析得到的歌曲
        song_list = self.parse_data(html)

        # 3.与用户交互，选择需要下载的值
        if len(song_list) == 0:
            print('[INFO]:查询的歌曲为空')
            return
        download_list = self.download_manage(song_list)

        # 4.发送链接，下载
        spawn_list = []
        for download in download_list:
            # 获取下载链接
            self.process_vkey_params(download)
            html = self.send_get_request(self.vkey_url, self.vkey_params)
            url = self.parse_url(html)
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
    spider = QQSpider()
    spider.main()
