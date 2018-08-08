# -*- coding: utf-8 -*-

# Scrapy settings for taobao1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'taobao1'

SPIDER_MODULES = ['taobao1.spiders']
NEWSPIDER_MODULE = 'taobao1.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobao1 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 3
# CONCURRENT_REQUESTS_PER_IP = 3

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    # 'taobao1.middlewares.Taobao1SpiderMiddleware': 543,
#     'taobao1.middlewares.Taobao1DownloaderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'taobao1.middlewares.Taobao1DownloaderMiddleware': 543,
    # 'taobao1.middlewares.TaobaoDownLoaderCommentMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'taobao1.pipelines.Taobao1Pipeline': 300,
    'taobao1.pipelines.CommentPipeline': 200,
    'taobao1.pipelines.FaileCommentPipeline': 300,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
LOG_FILE = "comment3000_6000.log"
LOG_LEVEL = "INFO"

COOKIES = [
    {
        "cna": "rv+bE/OZOQoCAbftQEbTh+fL",
        "hng": "CN%7Czh-CN%7CCNY%7C156",
        "sm4": "440300",
        "_med": "dw:1920&dh:1080&pw:1920&ph:1080&ist:0",
        "enc": "6PjSwZMveE%2ByVSz2pxQFyaM%2FolMj%2Fy3%2FHA6c%2BUVPPybt%2FjMYB0Dp9bsMM6JkscBzOlRQFD7zY4lBthTpQ8R74A%3D%3D",
        "otherx": "e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0",
        "x": "__ll%3D-1%26_ato%3D0",
        "cq": "ccp%3D1",
        "_uab_collina": "153320182237888040416277",
        "_umdata": "0823A424438F76ABD039B4341E0156DE0DCA1AAC194E561115C56658F80B214523F992ACB728E355CD43AD3E795C914C2F7460A391105DF5975F40427594EBDA",
        "lid": "wangyiweishiye",
        "t": "16e8210a22e487cc9300c01663e7a01a",
        "tracknick": "wangyiweishiye",
        "lgc": "wangyiweishiye",
        "_tb_token_": "7031eaae7e635",
        "cookie2": "3e7cbdab2d5880557fb0166874ee4bfd",
        "swfstore": "106351",
        "_m_h5_tk": "1342e747b73bdeb78d2bfb462cec0c5c_1533461469310",
        "_m_h5_tk_enc": "45345ddb9dcc14bb7f3952adcbf7aa10",
        "tt": "nvzhuang.tmall.com",
        "res": "scroll%3A1459*5580-client%3A1459*889-offset%3A1459*5580-screen%3A1920*1080",
        "uc1": "cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=V32FPkk%2FgihF%2FS5nr3O5&cookie15=URm48syIIVrSKA%3D%3D&existShop=false&pas=0&cookie14=UoTfKLJAPYz5wA%3D%3D&tag=8&lng=zh_CN",
        "uc3": "vt3=F8dBzrpColnvczMYweI%3D&id2=UUjTSIEXEtWCtQ%3D%3D&nk2=FPjangLFzOsaaOLWZMI%3D&lg2=UtASsssmOIJ0bQ%3D%3D",
        "_l_g_": "Ug%3D%3D",
        "ck1": "",
        "unb": "2022427346",
        "cookie1": "UIYySqNXvcR7xNhLguXaIYI0Ux5C5ZZaSSLA6m%2BbEUY%3D",
        "login": "true",
        "cookie17": "UUjTSIEXEtWCtQ%3D%3D",
        "_nk_": "wangyiweishiye",
        "uss": "",
        "csg": "5cf7dc22",
        "skt": "6ab7dbef8c977ecb",
        "isg": "BIWF1mvXcmI0u1ZHQnBCKB7WlMG1vDt_oG-cbYfrwLzbHqeQXpD_pC48LAJNXlGM"
     },

]

HEADERS = [
    {
        ":authority": "list.tmall.com",
        ":method": "GET",
        ":path": "/search_product.htm?q=%D0%C2%CF%CA%CB%AE%B9%FB&user_id=725677994&type=p&cat=50514008&spm=1.1.a2227oh.d100&from=chaoshi..pc_1_searchbutton",
        ":scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml",
        "accept-encoding": "gzip, deflate, br",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://chaoshi.detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.84de318d4lfndV&id=520940005154&areaId=440300&user_id=1910146537&cat_id=55116014&is_b=1&rn=8706da0410c2ff917725095d9275e7c8",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"},

]

PROXIES = [
    # {'ip_port': '122.114.69.82:16817', 'user_passwd': '307076311:44uobgq1'},
    {'ip_port': '122.114.247.216:16817', 'user_passwd': '1805082925:xb9qcv7o'},
]

PROXY_LIST = [
    # "http://HER2V93W49LSO85D:D27CF41D61F179C1@http-dyn.abuyun.com:9020"
    "http://1805082925:xb9qcv7o@122.114.247.216:16817"
]


USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
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
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
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
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
]
