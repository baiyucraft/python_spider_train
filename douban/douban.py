# -*- coding: UTF-8 -*-
import requests
import json
import re
import random
from bs4 import BeautifulSoup
# from spider.spider import Spide
from spider import Spide

class Douban(Spide):
    def __init__(self):
        super().__init__()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69',
            # 'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
            'Connection': 'close'
        }
        self.dou_s = requests.session()
        self.dou_s.keep_alive = False  # 关闭多余连接

    # 登录
    def login(self):
        self.login_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69',
            # 'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
            'Connection': 'close'
        }
        self.login_url = 'https://accounts.douban.com/j/mobile/login/basic'
        self.login_data = {
            'name': '18767032478',
            'password': 'Hjj199911115.',
            'remember': 'true',
        }
        this = self.dou_s.post(self.login_url, headers=self.login_header, data=self.login_data)
    
    # 获取网页信息
    def get_html(self, url, param):
        # ip_p = [{'http': 'http://124.205.155.158:9090', 'https': 'http://124.205.155.158:9090'} ]
        # random.choice(self.ip_proxy)
        # rs = self.dou_s.get(url, headers=self.header, params=param, proxies=random.choice(ip_p)) # , timeout=10
        # rs = self.dou_s.get(url, headers=self.header, params=param, proxies=random.choice(self.ip_proxy))
        rs = self.dou_s.get(url, headers=self.header, params=param)
        # print(rs.raw._connection.sock.getpeername()[0])
        rs.encoding = 'utf-8'
        bs = BeautifulSoup(rs.text, 'html5lib')
        return bs

    # 获取单页信息
    def get_info(self, url):
        # url = 'https://movie.douban.com/subject/1293182/'
        bs = self.get_html(url, None)
        info = bs.select('script[type="application/ld+json"]')[0].string
        info_js = json.loads(info, strict=False)
        # 筛选时间
        time = info_js['duration']
        info_js['duration'] = str(int(re.findall('\d+', time)[0]) * 60 + int(re.findall('\d+', time)[1]))
        # 筛选简介
        if bs.select('.all') == []:
            if list(bs.select('#link-report')[0].stripped_strings)[-1] =='©豆瓣':
                description = list(bs.select('#link-report')[0].stripped_strings)[:-1]
            else:
                description = list(bs.select('#link-report')[0].stripped_strings)
        else:
            description = list(bs.select('.all')[0].stripped_strings)
        info_js['description'] = description
        return info_js
    
    def main(self):
        # self.login()
        self.get_info('')

if __name__ == "__main__":
    D = Douban()
    D.main()