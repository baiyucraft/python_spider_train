import requests
import bs4
import os
import time
from threading import Thread
import html5lib
# -*- coding: UTF-8 -*-

class Novel():
    def __init__(self, id, path):
        self.header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0'
        }
        self.url = "http://www.dingdiansk.com"
        self.novel_path = path
        self.novel_id = id
    # 获取网页html内容
    def get_html(self, url):
        rs = requests.get(url, headers=self.header)
        rs.encoding = "utf-8"
        bs = bs4.BeautifulSoup(rs.text, "html5lib")
        return bs
    # 获取章节列表
    def get_chaper(self):
        self.bookUrl = self.url+"/book/"+self.novel_id+".html"
        chaperA = self.get_html(self.bookUrl).select(".dccss > a",)
        self.chaperL = []
        for chaper in chaperA:
            self.chaperL.append([chaper["href"],chaper.string])
    # 获取书名
    def get_title(self):
        self.novel_title = self.get_html(self.bookUrl).select('meta[property="og:novel:book_name"]')[0]["content"]
        print("正在下载小说：《"+self.novel_title+"》...")
    # 下载小说
    def downlaod_chaper(self):
        self.get_title()
        if not os.path.exists(self.novel_path):
            os.mkdir(self.novel_path)
        with open(self.novel_path + '/' + self.novel_id + ".txt", 'w', encoding="utf-8") as f:
            for chaper in self.chaperL:
                cont = self.get_html(self.url+chaper[0]).select("#content")
                print("正在下载 "+chaper[1])
                chaperText = cont[0].get_text()
                f.write(chaper[1])
                f.write(chaperText)
        f.close()
        self.clean()
    # 去广告
    def clean(self):
        print('正在清理文件...')
        with open(self.novel_path + '/' + self.novel_id + ".txt", 'r', encoding='utf-8') as f, open(self.novel_path + '/' + self.novel_title + ".txt", 'w', encoding='utf-8') as n:
            for line in f.readlines():
                if line == '\n':
                    line = line.strip('\n')
                if line == '天才一秒记住本站地址:(顶点中文)www.dingdiansk.com,最快更新!无广告!\n':
                    line = line.strip('天才一秒记住本站地址:(顶点中文)www.dingdiansk.com,最快更新!无广告!\n')
                if line == '    （本章完）      \n':
                    line = line.strip('    （本章完）      \n')
                if line == '    （本章未完，请翻页）\n':
                    line = line.strip('    （本章未完，请翻页）\n')
                n.write(line)
        f.close()
        n.close()
        print('小说下载完成')

    def main_novel_download(self):
        self.get_chaper()
        self.downlaod_chaper()



if __name__ == '__main__':
    # N = Novel('116046', 'novel')
    N = Novel('5', 'novel')
    N.main_novel_download()

