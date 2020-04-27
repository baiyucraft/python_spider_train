import requests
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import time
import os

class Spide():
    def __init__(self):
        super().__init__()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69',
            "Accept": "text/html,application/xhtml+xml,"
                      "application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "close",
        }
        # 所得到的ip地址
        self.proxy = Queue()
        # 筛选后的ip地址缓存
        self.ip_temp = []
        # 输出
        self.ip_proxy = []
        self.s = requests.session()
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.s.keep_alive = False  # 关闭多余连接
    
    def get_ip(self, count):
        self.proxy_path = 'proxy.txt'    
        try:
            if (time.time()-os.path.getmtime(self.proxy_path))/86400 > 1:
                print('文件已经失效')
                # self.xici(count)
                self.kuai(count)
                # print(self.proxy)
                print('正在测试...')
                # 多线程测试
                self.threads()
                self.s_flod()
        except:
            # self.xici(count)
            self.kuai(count)
            # print(self.proxy)
            print('正在测试...')
            # 多线程测试
            self.threads()
            self.s_flod()
        else:
            print('读取文件')
            with open(self.proxy_path, 'r', encoding='utf-8') as f:
                self.ip_temp = f.read().split()
            f.close()
        for ip in self.ip_temp:
            self.ip_proxy.append({'http': ip, 'https': ip})
        print(self.ip_proxy)


    # 写入代理
    def s_flod(self):
        with open(self.proxy_path, 'w') as f:
            for ip in self.ip_temp:
                f.write(ip+' ')
        f.close
        print('已经写入文件')

    # 快代理
    def kuai(self, count):
        num = 1
        for i in range(count+1)[1:]:
            # url = 'https://www.kuaidaili.com/free/intr/' + str(i) # 普通
            url = 'https://www.kuaidaili.com/free/inha/' + str(i) # 高匿
            print(url)
            rs = self.s.get(url, headers=self.header)
            rs.encoding = 'utf-8'
            bs = BeautifulSoup(rs.text, 'html5lib')
            ip_list = bs.select('.table-striped tbody tr')
            for ip in ip_list:
                self.proxy.put([num, 'http://' + ip.select('td')[0].string + ':' + ip.select('td')[1].string])
                num += 1
            print('共获取' + str(num) +'个代理')
            time.sleep(2)
        
    # 西祠代理
    def xici(self, count):
        for i in range(count):
            url = 'https://www.xicidaili.com/nn/'+str(i)
            rs = self.s.get(url, headers=self.header)
            rs.encoding = 'utf-8'
            bs = BeautifulSoup(rs.text, 'html5lib')
            ip_list = bs.select('#ip_list tr')
            for ip in ip_list[1:]:
                this = ip.select('.country')[2].select('.bar_inner')
                # print()
                if this[0]['class'][1] == 'fast':
                    # print(ip.select('td')[1].string)
                    self.proxy.put('http://' + ip.select('td')[1].string)
        # print(self.proxy)

    # 测试代理
    def test_ip(self):
        while True:
            try:
                # 不阻塞的读取队列数据
                p = self.proxy.get_nowait()
            except:
                break
            this = {'http': p[1], 'https': p[1]}
            try:
                resp = self.s.get('https://www.baidu.com', proxies=this, timeout=20)
            except:
                self.test2(p)
                print(str(p[0]) + '.1.连接失败')
            else:
                self.ip_temp.append(p[1])
                print(str(p[0]) + '.1.连接成功')

    # 第二次测试
    def test2(self, p):
        this = {'http': p[1], 'https': p[1]}
        try:
            resp = self.s.get('https://www.kongfz.com', proxies=this, timeout=20)
        except:
            self.test3(p)
            print(str(p[0]) + '.2.连接失败')
        else:
            self.ip_temp.append(p[1])
            print(str(p[0]) + '.2.连接成功')
            
    # 第三次测试
    def test3(self, p):
        this = {'http': p[1], 'https': p[1]}
        try:
            resp = self.s.get('https://www.sina.com.cn', proxies=this, timeout=20)
        except:
            print(str(p[0]) + '.3.连接失败')
        else:
            self.ip_temp.append(p[1])
            print(str(p[0]) + '.3.连接成功')


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


if __name__ == "__main__":
    S = Spide()
    p = S.get_ip(100)
    # print(p)