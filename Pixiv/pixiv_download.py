from threading import Thread
import requests
import os
import time
from queue import Queue


class Pixiv:
    # 初始化
    def __init__(self, p, path, b):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            'Accept-Language': 'zh-CN,zh',
            'Connection': 'close'
        }
        self.pic_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            'Sec-Fetch-Dest': 'image',
            'Connection': 'close'
        }
        self.daily_url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust'
        self.week_url = 'https://www.pixiv.net/ranking.php?mode=weekly&content=illust'
        self.month_url = 'https://www.pixiv.net/ranking.php?mode=monthly&content=illust'
        self.url = ''
        self.folder_path = path
        self.p = p 
        self.b = int(b) 
        #设置requests
        self.s = requests.session()
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.s.keep_alive = False  # 关闭多余连接

    # 获取排行榜图片ID
    def get_id(self):
        # 每50个图片id进行分类
        if self.b/50 == int(self.b/50):
            tl = int(self.b/50)
        else:
            tl = int(self.b/50) + 1
        url_list = []
        # 通过返回的json数据抓取所有图片的数据
        for t in range(tl):
            self.id_url = self.url + '&p=' + str(t+1) + '&format=json'
            rs = self.s.get(self.id_url, headers=self.header).json()
            url_list += rs['contents']
        # 对每一个id进行编号，采用二维数组
        num = 1
        self.url_id = []
        for u in url_list:
            self.url_id.append([num, str(u['illust_id'])])
            num = num + 1
        # 创建下载id队列
        self.u_id = Queue()
        for id in self.url_id[:self.b]:
            self.u_id.put(id)

    # 获取图片下载地址
    def get_durl(self):
        while True:
            try:
                # 不阻塞的读取队列数据
                id = self.u_id.get_nowait()
            except:
                break
            url = 'https://www.pixiv.net/ajax/illust/' + id[1] + '/pages'
            # 获取json中的body内容
            imgBody = self.s.get(url, headers=self.header).json()['body']
            img_url = []
            for imgp in imgBody:
                img_url.append(imgp['urls']['original'])
            if len(img_url) <= 20:
                self.download_img(img_url, id)

    # 下载图片
    def download_img(self, img_url, id):
        self.pic_header['Referer'] = 'https://www.pixiv.net/artworks/' + id[1]
        for img in img_url:
            img_back = img[-7:]
            img_path = self.folder_path + '/' + id[1] + img_back
            if not os.path.isfile(img_path):
                print(str(id[0]) + '.正在下载图片：' + id[1] + img_back + '...')
                imgRes = self.s.get(img, headers=self.pic_header).content
                with open(img_path, 'wb') as f:
                    f.write(imgRes)
                    f.close()
            else:
                print(str(id[0]) + '.文件已存在')

    # 创建文件夹
    def creat_floder(self):
        # 判断文件夹是否已经存在
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)
        print('文件夹已创建...')

    #主函数
    def down_main(self):
        if self.p == '1':
            self.url = self.daily_url
            self.folder_path = self.folder_path + '/day/' + time.strftime("%Y.%m.%d", time.localtime())
            print('正在下载日排行榜的图片...')
        elif self.p == '2':
            self.url = self.week_url
            self.folder_path = self.folder_path + '/week'
            print('正在下载周排行榜的图片...')
        elif self.p == '3':
            self.url = self.month_url
            self.folder_path = self.folder_path + '/month'
            print('正在下载月排行榜的图片...')
        self.get_id()
        self.creat_floder()
        self.threads()
        print('已完成排名前'+ str(self.b) +'图片的下载，下载目录在：' + self.folder_path)

    # 多线程下载
    def threads(self):
        T = []
        for i in range(10):
            t = Thread(target=self.get_durl, args=())
            T.append(t)
        for i in T:
            i.start()
        for i in T:
            i.join()

if __name__ == '__main__':
    pic = Pixiv('3', 'D:/图片/Pixiv', 150)
    pic.down_main()