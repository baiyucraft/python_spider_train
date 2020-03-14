import requests
import bs4
import os
import time


class Pixiv:
    # 初始化
    def __init__(self):
        self.header = header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            'Cookie': '_cfduid=d013dbab27f08d937abf1668bba1c507b1582800657; age_certification=isok; _ga=GA1.2.981223937.1582800691; _gid=GA1.2.993052740.1582800691; wordpress_logged_in_6242fde54bf6f4f4b0c842643584bd9b=hjj19991111%7C1584010356%7CTLIjKCulafQoTZo4aLk8HxDkTBnKsWa7NZPp8CvSipv%7Ccb3e5132b4894dc7d31d2494bfbd0c62eb9d4dd547fc6ba7919a5cca85c8de63; PHPSESSID=tmufe0qi6auio9jead30s3o99n',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'close'
        }
        self.picHeader = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            'Sec-Fetch-Dest': 'image',
            'Connection': 'close'
        }
        self.dailyUrl = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust'
        self.weekUrl = 'https://www.pixiv.net/ranking.php?mode=weekly&content=illust'
        self.monthUrl = 'https://www.pixiv.net/ranking.php?mode=monthly&content=illust'
        self.Url = ''
        self.urlId = []
        self.folderPath = 'D:/图片/Pixiv/'
        self.p = ''
        self.b = 0
        #设置requests
        self.s = requests.session()
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.s.keep_alive = False  # 关闭多余连接

    # 获取排行榜图片ID
    def getId(self):
        self.header['referer'] = self.Url
        urlL = []
        if self.p =='3':
            for i in ['1','2','3']:
                self.Url = self.Url + '&p=' + i + '&format=json'
                rs = self.s.get(self.Url, headers=self.header).json()
                urlL += rs['contents']
        else:
            self.Url = self.Url + '&p=1&format=json'
            rs = self.s.get(self.Url, headers=self.header).json()
            urlL += rs['contents']
        for u in urlL:
            self.urlId.append(str(u['illust_id']))

    # 获取图片下载地址
    def getDUrl(self):
        num = 1
        for id in self.urlId[:self.b]:
            url = 'https://www.pixiv.net/ajax/illust/' + id + '/pages'
            # 获取json中的body内容
            imgBody = self.s.get(url, headers=self.header).json()['body']
            imgUrl = []
            for imgp in imgBody:
                imgUrl.append(imgp['urls']['original'])
            if len(imgUrl) <= 10:
                self.downloadImg(imgUrl, id, num)
            num = num+1

    # 下载图片
    def downloadImg(self, imgUrl, id, num):
        self.picHeader['Referer'] = 'https://www.pixiv.net/artworks/' + id
        for img in imgUrl:
            imgBack = img[-7:]
            imgPath = self.folderPath + '/' + id + imgBack
            if not os.path.isfile(imgPath):
                print(str(num) + '.正在下载图片：' + id + imgBack + '...')
                imgRes = self.s.get(img, headers=self.picHeader).content
                with open(imgPath, 'wb') as f:
                    f.write(imgRes)
                    f.close()
            else:
                print(str(num) + '.文件已存在')

    # 创建文件夹
    def creatFloder(self):
        # 判断文件夹是否已经存在
        if not os.path.exists(self.folderPath):
            os.mkdir(self.folderPath)
        print('文件夹已创建...')

    #主函数
    def downMain(self):
        self.p = input("请输入要下载的是日排行榜(1)、周排行榜(2)、月排行榜(3)：")
        if self.p == '1':
            self.Url = self.dailyUrl
            self.b = 20
            self.folderPath = self.folderPath + 'day/' + time.strftime("%Y.%m.%d", time.localtime())
            print('正在下载日排行榜的图片...')
        elif self.p == '2':
            self.Url = self.weekUrl
            self.b = 50
            self.folderPath = self.folderPath + 'week'
            print('正在下载周排行榜的图片...')
        elif self.p == '3':
            self.Url = self.monthUrl
            self.b = 150
            self.folderPath = self.folderPath + 'month'
            print('正在下载月排行榜的图片...')
        else:
            print('请输入正确的数字')
            return 0
        self.getId()
        self.creatFloder()
        self.getDUrl()
        print('已完成排名前'+ str(self.b) +'图片的下载，下载目录在：' + self.folderPath)

if __name__ == '__main__':
    pic = Pixiv()
    pic.downMain()