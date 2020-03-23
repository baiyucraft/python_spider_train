import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from bin.OnLayout import *
from bin.Usually import *
from spider.novel_download import Novel

class NovelQt(MyWidget):
    def __init__(self):
        super(NovelQt, self).__init__()
        self.t_layout = MyVBoxLayout()
        self.setLayout(self.t_layout)
        self.setFixedHeight(460)
        self.setFixedWidth(700)
        self.setObjectName('NovelQt')
    
        self.path = self.path + '\\novel'

        # 主UI
        self.widget_ui()
        # 载入qss样式
        with open('./bin/NovelQt.qss','r', encoding='utf-8') as f:
            qssStyle = f.read()
        self.setStyleSheet(qssStyle)
        
    # 主ui
    def widget_ui(self):
        self.row1_ui()
        self.row2_ui()
        self.console_ui()

        self.t_layout.addWidget(self.row1)
        self.t_layout.addSpacing(60)
        self.t_layout.addWidget(self.row2)
        self.t_layout.addSpacing(60)
        self.t_layout.addWidget(self.console)

        # 默认值
        self.id_input.setText('5')
        self.path_input.setText(self.path)

        #信号连接动作
        self.download.clicked.connect(self.novel_download)
        self.path_button.clicked.connect(self.get_path)

    # 第一行
    def row1_ui(self):
        self.row1 = QWidget()
        self.row1_layout = MyHBoxLayout()
        self.row1.setLayout(self.row1_layout)
        self.row1.setObjectName('row')
        self.row1.setFixedHeight(30)
        # 控件
        self.id_t = QLabel('小说ID：')
        self.id_t.setFont(QFont('Microsoft YaHei'))
        self.id_t.setObjectName('t')
        self.id_t.setFixedSize(120, 30)

        self.id_input = QLineEdit()
        self.id_input.setObjectName('input')
        self.id_input.setFixedSize(470, 30)

        self.download = QPushButton('下载')
        self.download.setObjectName('button')
        self.download.setFixedSize(80, 30)
        self.download.setCursor(QCursor(Qt.PointingHandCursor))

        self.row1_layout.addWidget(self.id_t)
        self.row1_layout.addWidget(self.id_input)
        self.row1_layout.addSpacing(30)
        self.row1_layout.addWidget(self.download)

    # 第二行
    def row2_ui(self):
        self.row2 = QWidget()
        self.row2_layout = MyHBoxLayout()
        self.row2.setLayout(self.row2_layout)
        self.row2.setObjectName('row')
        self.row2.setFixedHeight(30)
        # 控件
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

        self.row2_layout.addWidget(self.path_t)
        self.row2_layout.addWidget(self.path_input)
        self.row2_layout.addSpacing(30)
        self.row2_layout.addWidget(self.path_button)

    # 第三行
    def console_ui(self):
        self.console = QTextEdit()
        self.console.setObjectName('console')
        
    # 下载小说
    def novel_download(self):
        # 创建线程
        self.thread = NovelThread(self.id_input.text(),self.path_input.text())
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.thread.start()

# 定义下载小说的线程类
class NovelThread(QThread):
    def __init__(self, id, path):
        super(NovelThread, self).__init__()
        self.id = id
        self.path = path
    def __del__(self):
        self.wait()
    # 设置run的文件
    def run(self):
        self.novel_d = Novel(self.id, self.path)
        self.novel_d.main_novel_download()