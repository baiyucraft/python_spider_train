import sys
import time
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bin.OnLayout import *
from bin.NovelQt import NovelQt
from bin.PixivQt import PixivQt

# 主要的布局
class MainP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Program')
        self.setFixedSize(1300, 740)
        self.setWindowIcon(QIcon('./128x128.icon'))
        self.setObjectName('app')
        # 设置窗口透明度
        # self.setWindowOpacity(0.9)
        # 设置窗口边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
        # 窗口移动用
        self._isTracking = False
        self._startPos = QPoint(0, 0)
        self._endPos = QPoint(0, 0)

    # 初始化UI
    def init_ui(self):
        # 主窗口
        self.main_widget = QWidget()
        # 创建主窗口的布局
        self.main_layout = MyHBoxLayout()
        self.main_widget.setFixedSize(1300, 740)
        # 设置主窗口为垂直布局
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setObjectName('main')
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setOffset(0.0)
        self.shadow.setColor(Qt.gray)
        self.shadow.setBlurRadius(20)
        self.main_widget.setGraphicsEffect(self.shadow)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # 左侧菜单栏
        self.init_left_ui()
        # 右侧内容栏
        self.init_right_ui()

        self.main_layout.addWidget(self.left_widget)
        self.main_layout.addWidget(self.right_widget)
        self.setCentralWidget(self.main_widget)

    # 左侧的菜单UI
    def init_left_ui(self):
        self.left_widget = QWidget()
        self.left_widget.setObjectName('left')
        self.left_layout = MyVBoxLayout()
        self.left_widget.setLayout(self.left_layout)
        self.left_widget.setFixedWidth(300)

        self.left_admin = QWidget()
        self.left_admin.setFixedHeight(190)
        self.left_admin.setObjectName('left_admin')
        self.init_lef_mid_ui()
        self.left_bottom = QWidget()
        self.left_bottom.setFixedHeight(260)
        self.left_bottom.setObjectName('left_bottom')

        self.left_layout.addWidget(self.left_admin)
        self.left_layout.addWidget(self.left_mid)
        self.left_layout.addWidget(self.left_bottom)
        
    # 左侧中部主要内容
    def init_lef_mid_ui(self):
        self.left_mid = QWidget()
        self.left_mid.setObjectName('left_mid')
        self.left_mid_layout = MyVBoxLayout()
        self.left_mid_layout.setContentsMargins(0, 30, 0, 0)
        self.left_mid.setLayout(self.left_mid_layout)
        
        # 定义控件
        # 爬虫程序标签
        self.left_label1 = QPushButton('爬虫程序')
        self.left_label1.setObjectName('left_label')
        # 小说下载按钮
        self.left_button1 = QPushButton('小说下载')
        self.left_button1.setObjectName('left_button_t')
        self.left_button1.setCursor(QCursor(Qt.PointingHandCursor))
        # Pixiv下载按钮
        self.left_button2 = QPushButton('Pixiv下载')
        self.left_button2.setObjectName('left_button')
        self.left_button2.setCursor(QCursor(Qt.PointingHandCursor))
        # 更多功能
        self.left_button_m = QPushButton('更多功能开发中...')
        self.left_button_m.setObjectName('left_more')

        self.left_mid_layout.addWidget(self.left_label1)
        self.left_mid_layout.addSpacing(10)
        self.left_mid_layout.addWidget(self.left_button1)
        self.left_mid_layout.addSpacing(10)
        self.left_mid_layout.addWidget(self.left_button2)
        self.left_mid_layout.addSpacing(10)
        self.left_mid_layout.addWidget(self.left_button_m)

        self.left_button1.clicked.connect(self.change_novel)
        self.left_button2.clicked.connect(self.change_pixiv)

    # 右侧内容UI
    def init_right_ui(self):
        self.right_widget = QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = MyVBoxLayout()
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.setFixedWidth(980)

        # 上部状态栏
        self.init_top_ui()
        # 中部主要栏
        self.init_mid_ui()

        self.right_layout.addWidget(self.top_widget)
        self.right_layout.addWidget(self.mid_widget)
        
    # 上部状态栏
    def init_top_ui(self):
        self.top_widget = QWidget()
        self.top_layout = MyHBoxLayout()
        self.top_widget.setLayout(self.top_layout)
        self.top_widget.setObjectName('top')
        self.top_widget.setFixedHeight(40)

        # 左边菜单
        self.init_top_left_ui()
        # 右边控制
        self.init_top_right_ui()

        self.top_layout.addWidget(self.top_left)
        self.top_layout.addWidget(self.top_right)

    # 上部左侧菜单
    def init_top_left_ui(self):
        self.top_left = QWidget()
        self.top_left_layout = MyHBoxLayout()
        self.top_left.setLayout(self.top_left_layout)
        self.top_left.setObjectName('top_left')
        self.top_left.setFixedWidth(870)

    # 上部右侧控制
    def init_top_right_ui(self):
        self.top_right = QWidget()
        self.top_right_layout = MyHBoxLayout()
        self.top_right.setLayout(self.top_right_layout)
        self.top_right.setObjectName('top_right')
        self.top_right.setFixedWidth(110)

        # 最小化按钮
        self.top_mini = QPushButton('')
        self.top_mini.setObjectName('top_mini')
        self.top_mini.setFixedSize(20, 20)
        # 关闭按钮
        self.top_close = QPushButton('')
        self.top_close.setObjectName('top_close')
        self.top_close.setFixedSize(20, 20)
        
        self.top_right_layout.addWidget(self.top_mini)
        self.top_right_layout.addWidget(self.top_close)

        self.top_mini.clicked.connect(self.showMinimized)
        self.top_close.clicked.connect(self.close)
    
    # 中部主要栏
    def init_mid_ui(self):
        self.mid_widget = QWidget()
        self.mid_layout = MyVBoxLayout()
        self.mid_widget.setLayout(self.mid_layout)
        self.mid_widget.setObjectName('mid')
        self.mid_widget.setFixedHeight(680)

        self.mid_main = QWidget()
        self.mid_main_layout = MyVBoxLayout()
        self.mid_main.setLayout(self.mid_main_layout)
        self.mid_main.setObjectName('mid_main')

        self.mid_stacked = QWidget()
        # 页面切换布局
        self.mid_stacked_layout = MyStackedLayout()
        self.mid_stacked.setLayout(self.mid_stacked_layout)
        self.mid_stacked.setObjectName('mid_stacked')

        self.mid_main_layout.setContentsMargins(140, 90, 140, 90)
        # self.mid_main_layout.setContentsMargins(140, 75, 140, 75)
        self.novel_qt = NovelQt()
        self.pixiv_qt = PixivQt()

        # 布局
        self.mid_layout.addWidget(self.mid_main)
        self.mid_layout.addSpacing(40)
        self.mid_main_layout.addWidget(self.mid_stacked)
        self.mid_stacked_layout.addWidget(self.novel_qt)
        self.mid_stacked_layout.addWidget(self.pixiv_qt)

    # 底部信息栏-暂定没有
    def init_bottom_ui(self):
        self.bottom_widget = QWidget()
        self.bottom_layout = MyGridLayout()
        self.bottom_widget.setLayout(self.bottom_layout)
        self.bottom_widget.setObjectName('bottom')
    
    # 重写鼠标事件
    def isTop(self, this):
        if this.x() > 310 and this.x() < 1290 and this.y() > 10 and this.y() < 50:
            return True 

    def mousePressEvent(self, e):
        
        if e.button() == Qt.LeftButton and self.isTop(e):
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())
    
    def mouseMoveEvent(self, e):
        if self._isTracking: 
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.isTop(e):
            self._isTracking = False
            self._startPos = QPoint(0, 0)
            self._endPos = QPoint(0, 0)
    
    # 切换
    def change_novel(self):
        if self.mid_stacked_layout.currentIndex() != 0:
            self.mid_main_layout.setContentsMargins(140, 90, 140, 90)
            self.left_button1.setObjectName('left_button_t')
            self.left_button2.setObjectName('left_button')
            self.setStyleSheet(self.qssStyle)
            self.mid_stacked_layout.setCurrentIndex(0)

    def change_pixiv(self):
        if self.mid_stacked_layout.currentIndex() != 1:
            self.mid_main_layout.setContentsMargins(140, 75, 140, 75)
            self.left_button1.setObjectName('left_button')
            self.left_button2.setObjectName('left_button_t')
            self.setStyleSheet(self.qssStyle)
            self.mid_stacked_layout.setCurrentIndex(1)
    # 主函数
    def main_Q(self):
        with open('./style.qss','r', encoding='utf-8') as f:
            self.qssStyle = f.read()
        self.setStyleSheet(self.qssStyle)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建窗口
    ui_main = MainP()
    ui_main.main_Q()
    sys.exit(app.exec_())