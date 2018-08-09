# coding=utf-8

"""协程版本抓取酷狗音乐的歌曲"""

import os
import requests
import json
import random
import gevent
from gevent import monkey

# 打个补丁
monkey.patch_all()


class KuGouSpider(object):
    __cnt = 0  # 初始计数，判定协程是否结束
    __target_num = 0  # 下载文件数

    def __init__(self):

        self.search_song = "http://songsearch.kugou.com/song_search_v2?"
        self.search_music = raw_input('[INFO]:请输入你要搜索的歌曲名称：')
        self.music_url = "http://www.kugou.com/yy/index.php?r=play/getdata&"
        self.path = "kugou_musics"
        if not os.path.exists(self.path):  # 不存在文件夹，则新建文件夹
            os.mkdir(self.path)
        self.headers = [
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"},
            {"User-Agent": "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"},
            {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3"},
            {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"},
            {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"},
            {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8"},
            {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"},
            {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 "},
            {"User-Agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"},
        ]

    def send_request(self, url, params=None, down_name=None):
        """发送请求"""
        print('[INFO]:正在请求<{}>'.format(url))
        response = requests.get(url, params=params, headers=random.choice(self.headers))  # 随机User-Agent
        data = response.content  # 直接读取内容
        # print(response.url)
        if down_name:  # 是要下载的话
            self.download_music(data, down_name)
        else:
            return data

    def download_music(self, music, music_name):
        music_name += ".mp3"
        with open(self.path + '/' + music_name, "wb") as f:
            f.write(music)
            print(u"[INFO]:%s下载成功" % music_name)

    def handle_json_data(self, json_data, flag):
        """
        处理json数据,json是一种数据格式，有点像python中的字典，
        通过json模块可以把json格式数据转换成dict(字典)，方便提取我们想要的数据
        """
        json_to_dict = json.loads(json_data)  # 转换成字典
        musics_info = json_to_dict['data']

        if flag == 1:  # 默认为1，显示30个
            # 获取歌曲的详细信息
            musics_info = musics_info['lists']
            musics_list = list()
            for music_info in musics_info:
                music_info_dict = {}  # 创建字典
                music_info_dict['music_name'] = music_info['FileName']
                music_info_dict['FileHash'] = music_info['FileHash']
                music_info_dict['HQFileHash'] = music_info['HQFileHash']
                music_info_dict['AlbumID'] = music_info['AlbumID']
                musics_list.append(music_info_dict)
            return musics_list
        elif flag == 2:  # 直接获取链接
            # 获取歌曲的下载链接
            download_url_list = list()
            download_url_list.append(musics_info['play_url'])  # important
            print("[INFO]:播放链接是<{}>".format(musics_info['play_url']))
            return download_url_list

    def download_mange(self, musics_lists):
        """下载管理"""
        download_list = list()
        for index, music in enumerate(musics_lists):
            index += 1
            print("%d %s" % (index, music['music_name']))

        try:
            download_choice = raw_input("[INFO]:请选择你要下载的歌曲[如：1，2，3或输入all全部下载]: ")
            if download_choice == "all":
                return musics_lists
            else:
                download_choice_list = download_choice.split(",")  # 一次多个下载，切分字符串
                print("[INFO]:你选中的歌曲：")
                for download_index in download_choice_list:
                    music_info = musics_lists[int(download_index) - 1]
                    download_list.append(music_info)
                    print(music_info['music_name'])
                return download_list
        except Exception as ret:
            print(ret)

    def main(self):
        # 发送搜索歌曲请求
        params = {
            'keyword': self.search_music,
            'page': 1,
            'pagesize': 20,  # 修改这个可以获取更多的歌曲
            'platform': "WebFilter",
            # 'tag': "em",
            'iscorrection': 1
        }
        search_result = self.send_request(self.search_song, params)

        # 歌曲列表
        musics_list = self.handle_json_data(search_result, 1)

        # 把需要下载的歌曲加入到下载列表
        download_list = self.download_mange(musics_list)

        # hash = 718567D263C17BB3945B596CDD887C27 & album_id = 8308163 & _ = 1517146077031
        spawn_list = []
        for music in download_list:
            params = {
                'hash': music['FileHash'],
                # 'hash': music['HQFileHash'],
                'album_id': music['AlbumID']
            }
            music_play = self.send_request(self.music_url, params)
            # 获取搜索出来的歌曲下载链接
            download_url_list = self.handle_json_data(music_play, 2)  # 标志为2
            for download_url in download_url_list:
                music_name = music['music_name']
                if not download_url:
                    print('[INFO]:歌曲受到版权保护，无法下载...')
                    continue
                spawn = gevent.spawn(self.send_request, download_url, down_name=music_name)
                spawn_list.append(spawn)

        # 统一添加到任务队列，执行所有的协程
        gevent.joinall(spawn_list)


if __name__ == '__main__':
    spider = KuGouSpider()
    spider.main()
