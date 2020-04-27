# -*- coding: UTF-8 -*-
import requests
import xlwt
from bs4 import BeautifulSoup
# from douban.douban import Douban
from douban import Douban
from threading import Thread

class DouMovie(Douban):
    def __init__(self):
        super().__init__()

    def all_movie(self):
        print('正在爬取所有电影')

    # 电影top250
    def movie_top250(self):
        print('正在爬取...')
        self.top250_url = 'https://movie.douban.com/top250'
        self.top250_param = {'start': 0}
        url_list = []
        num = 1
        for i in range(0, 250, 25):
            self.top250_param['start'] = i
            bs = self.get_html(self.top250_url, self.top250_param)
            a_list = bs.select('.item .hd a')
            for a in a_list:
                url_list.append([num, a['href']])
                num += 1
        # print(url_list)
        self.cr_excel()
        for url in url_list:
            print('正在导入排行' + str(url[0]))
            info = self.get_info(url[1])
            data = self.info_process(info)
            self.wr_excel(url[0], data, 'top250')
        self.work_book.save('D:/project/1testpack/top250.xls')
        
    # 数据存储
    def info_process(self, info):
        data = {}
        # 电影名
        data['name'] = info['name']
        # 评分
        data['rank_v'] = info['aggregateRating']['ratingValue']
        # 导演
        data['director'] = []
        for i in info['director']:
            data['director'].append(i['name'])
        # 编剧
        data['author'] = []
        for i in info['author']:
            data['author'].append(i['name'])
        # 主演
        data['actor'] = []
        for i in info['actor']:
            data['actor'].append(i['name'])
        # 上映时间
        data['publish_time'] = info['datePublished']
        # 类型
        data['genre'] = []
        for i in info['genre']:
            data['genre'].append(i)
        # 片长
        data['duration_time'] = info['duration']
        # 简介
        data['description'] = info['description']
        return data

    # 创建EXcel
    def cr_excel(self):
        self.work_book = xlwt.Workbook(encoding='utf-8')
        self.work_sheet1 = self.work_book.add_sheet('sheet1')
        self.work_sheet1.write(0, 0, '电影名')
        self.work_sheet1.write(0, 1, '评分')
        self.work_sheet1.write(0, 2, '导演')
        self.work_sheet1.write(0, 3, '编剧')
        self.work_sheet1.write(0, 4, '主演')
        self.work_sheet1.write(0, 5, '上映时间')
        self.work_sheet1.write(0, 6, '类型')
        self.work_sheet1.write(0, 7, '片长')
        self.work_sheet1.write(0, 8, '简介')
        # 设置字体样式
        # font = xlwt.Font()
        # font.name = '宋体'
    
    # 数据写入Excel
    def wr_excel(self, num, data, t):
        self.work_sheet1.write(num, 0, data['name'])
        self.work_sheet1.write(num, 1, data['rank_v'])
        self.work_sheet1.write(num, 2, data['director'])
        self.work_sheet1.write(num, 3, data['author'])
        self.work_sheet1.write(num, 4, data['actor'])
        self.work_sheet1.write(num, 5, data['publish_time'])
        self.work_sheet1.write(num, 6, data['genre'])
        self.work_sheet1.write(num, 7, data['duration_time'])
        self.work_sheet1.write(num, 8, data['description'])


    def threads(self):
        T = []
        for i in range(50):
            t = Thread(target=self.test_ip, args=())
            T.append(t)
        for i in T:
            print(i)
            i.start()
        for i in T:
            i.join()

    def main(self):
        # 获取ip池
        self.get_ip(10)
        print(self.ip_proxy)
        self.movie_top250()

if __name__ == "__main__":
    D = DouMovie()
    D.main()