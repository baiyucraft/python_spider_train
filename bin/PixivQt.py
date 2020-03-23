import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from threading import Thread
import time
from bin.OnLayout import *
from bin.Usually import *
from Pixiv.pixiv_download import Pixiv

class PixivQt(MyWidget):
    def __init__(self):
        super(PixivQt, self).__init__()
        self.t_layout = MyVBoxLayout()
        self.setLayout(self.t_layout)
        self.setFixedHeight(490)
        self.setFixedWidth(700)
        self.setObjectName('PixivQt')
    
        # self.path = self.path + '\\Pixiv'
        self.path = 'D:/图片/Pixiv'
        self.p = ''

        # 主UI
        self.widget_ui()
        # 载入qss样式
        with open('./bin/PixivQt.qss','r', encoding='utf-8') as f:
            qssStyle = f.read()
        f.close()
        self.setStyleSheet(qssStyle)
    
    def widget_ui(self):
        self.row1_ui()
        self.row2_ui()
        self.row3_ui()
        self.row4_ui()
        self.console_ui()

        # 设置默认值
        self.day_input.setText('20')
        self.week_input.setText('50')
        self.month_input.setText('150')
        self.path_input.setText(self.path)

        self.t_layout.addWidget(self.row1)
        self.t_layout.addSpacing(20)
        self.t_layout.addWidget(self.row2)
        self.t_layout.addSpacing(20)
        self.t_layout.addWidget(self.row3)
        self.t_layout.addSpacing(20)
        self.t_layout.addWidget(self.row4)
        self.t_layout.addSpacing(20)
        self.t_layout.addWidget(self.console)
        
        #信号连接动作
        self.day_download.clicked.connect(self.pixiv_download)
        self.week_download.clicked.connect(self.pixiv_download)
        self.month_download.clicked.connect(self.pixiv_download)
        self.path_button.clicked.connect(self.get_path)
    def row1_ui(self):
        self.row1 = QWidget()
        self.row1_layout = MyHBoxLayout()
        self.row1.setLayout(self.row1_layout)
        self.row1.setObjectName('row')
        self.row1.setFixedHeight(30)
        
        self.day_t = QLabel('日排行榜：')
        self.day_t.setObjectName('t')
        self.day_t.setFixedSize(120, 30)

        self.day_input = QLineEdit()
        self.day_input.setObjectName('input')
        self.day_input.setFixedSize(470, 30)

        self.day_download = QPushButton('下载')
        self.day_download.setObjectName('button1')
        self.day_download.setFixedSize(80, 30)
        self.day_download.setCursor(QCursor(Qt.PointingHandCursor))

        self.row1_layout.addWidget(self.day_t)
        self.row1_layout.addWidget(self.day_input)
        self.row1_layout.addSpacing(30)
        self.row1_layout.addWidget(self.day_download)
    
    def row2_ui(self):
        self.row2 = QWidget()
        self.row2_layout = MyHBoxLayout()
        self.row2.setLayout(self.row2_layout)
        self.row2.setObjectName('row')
        self.row2.setFixedHeight(30)

        self.week_t = QLabel('周排行榜：')
        self.week_t.setObjectName('t')
        self.week_t.setFixedSize(120, 30)

        self.week_input = QLineEdit()
        self.week_input.setObjectName('input')
        self.week_input.setFixedSize(470, 30)

        self.week_download = QPushButton('下载')
        self.week_download.setObjectName('button2')
        self.week_download.setFixedSize(80, 30)
        self.week_download.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.row2_layout.addWidget(self.week_t)
        self.row2_layout.addWidget(self.week_input)
        self.row2_layout.addSpacing(30)
        self.row2_layout.addWidget(self.week_download)

    def row3_ui(self):
        self.row3 = QWidget()
        self.row3_layout = MyHBoxLayout()
        self.row3.setLayout(self.row3_layout)
        self.row3.setObjectName('row')
        self.row3.setFixedHeight(30)
        
        self.month_t = QLabel('月排行榜：')
        self.month_t.setObjectName('t')
        self.month_t.setFixedSize(120, 30)

        self.month_input = QLineEdit()
        self.month_input.setObjectName('input')
        self.month_input.setFixedSize(470, 30)

        self.month_download = QPushButton('下载')
        self.month_download.setObjectName('button3')
        self.month_download.setFixedSize(80, 30)
        self.month_download.setCursor(QCursor(Qt.PointingHandCursor))

        self.row3_layout.addWidget(self.month_t)
        self.row3_layout.addWidget(self.month_input)
        self.row3_layout.addSpacing(30)
        self.row3_layout.addWidget(self.month_download)

    def row4_ui(self):
        self.row4 = QWidget()
        self.row4_layout = MyHBoxLayout()
        self.row4.setLayout(self.row4_layout)
        self.row4.setObjectName('row')
        self.row4.setFixedHeight(30)

        self.path_t = QLabel('下载地址：')
        self.path_t.setObjectName('t')
        self.path_t.setFixedSize(120, 30)

        self.path_input = QLineEdit()
        self.path_input.setObjectName('input')
        self.path_input.setFixedSize(470, 30)

        self.path_button = QPushButton('浏览')
        self.path_button.setObjectName('button')
        self.path_button.setFixedSize(80, 30)
        self.path_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.row4_layout.addWidget(self.path_t)
        self.row4_layout.addWidget(self.path_input)
        self.row4_layout.addSpacing(30)
        self.row4_layout.addWidget(self.path_button)
    
    def console_ui(self):
        self.console = QTextEdit()
        self.console.setObjectName('console')

    def pixiv_download(self):
        if self.sender().objectName() == 'button1':
            self.p = '1'
            self.b = self.day_input.text()
        elif self.sender().objectName() == 'button2':
            self.p = '2'
            self.b = self.week_input.text()
        elif self.sender().objectName() == 'button3':
            self.p = '3'
            self.b = self.month_input.text()
        
        self.pixiv_d = Pixiv(self.p, self.path, self.b)
        # 创建线程
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.thread = TasksThread(self.pixiv_d, communicate=1)
        self.thread.start()
        
# 定义获取id的线程
class ThreadG(QRunnable):
    def __init__(self, pixiv_d):
        # 任务
        super(ThreadG, self).__init__()
        self.pixiv_d = pixiv_d
    def run(self):
        self.pixiv_d.down_main()
# 定义获取图片的线程
class ThreadD(QRunnable):
    def __init__(self, pixiv_d):
        # 任务
        super(ThreadD, self).__init__()
        self.pixiv_d = pixiv_d
    def run(self):
        self.pixiv_d.get_durl()
# 创建线程池
class Tasks(QObject):
    # pixiv_d ；communicate 信号；thread_count 线程数
    def __init__(self, pixiv_d, communicate, thread_count):
        super(Tasks, self).__init__()
        self.pixiv_d = pixiv_d
        self.communicate = communicate
        self.thread_count = thread_count
        # 创建线程池
        self.pool = QThreadPool()
        # 获得全局线程池
        self.pool.globalInstance()
    def thread_stop(self):
        self.pool.clear()
    def start(self):
        # 最大线程池
        # self.pool.setMaxThreadCount(self.thread_count)
        this_get = ThreadG(self.pixiv_d)
        self.pool.start(this_get)
        for i in range(self.thread_count):
            thread_ins = ThreadD(self.pixiv_d)
            thread_ins.setAutoDelete(True)
            self.pool.start(thread_ins)
        # 等待线程结束
        self.pool.waitForDone()
# 运行线程池
class TasksThread(QThread):
    def __init__(self, pixiv_d, communicate, thread_count = 10):
        super(TasksThread, self).__init__()
        self.task = self.task = Tasks(pixiv_d=pixiv_d, communicate=communicate, thread_count=thread_count)
    def run(self):
        self.task.start()














        

        
       
        
