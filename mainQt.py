import sys
import time
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from python_spider_train.spider.novel_download import Novel
from spider.novel_download import Novel
from PyQt5.QtWebEngineWidgets import QWebEngineView

# 定义默认布局
# 水平
class MyHBoxLayout(QHBoxLayout):
    def __init__(self):
        super(MyHBoxLayout, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
# 垂直
class MyVBoxLayout(QVBoxLayout):
    def __init__(self):
        super(MyVBoxLayout, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
# 表单
class MyFormLayout(QFormLayout):
        def __init__(self):
            super(MyFormLayout, self).__init__()
            self.setContentsMargins(0, 0, 0, 0)
            self.setSpacing(0)
# 表格
class MyGridLayout(QGridLayout):
    def __init__(self):
        super(MyGridLayout, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

# 主要的布局
class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Test')
        self.setFont(QFont('微软雅黑'))
        self.setFixedSize(1300, 740)
        self.setWindowIcon(QIcon('./128x128.icon'))
        self.setObjectName('app')
        # 设置窗口透明度
        # self.setWindowOpacity(0.9)
        # 设置窗口边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.novel_path = os.path.dirname(os.path.abspath(__file__)) + '/novel'
        self.thread = None
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
        self.mid_layout.setContentsMargins(170, 0, 170, 0)
        self.mid_widget.setObjectName('mid')
        self.mid_widget.setFixedHeight(680)

        self.mid_main = QWidget()
        self.mid_main_layout = MyVBoxLayout()
        self.mid_main.setLayout(self.mid_main_layout)
        self.mid_main.setFixedWidth(700)
        self.mid_main.setFixedHeight(640)
        self.mid_main.setObjectName('mid_main')

        self.mid_main_this_ui()

        # 布局
        self.mid_layout.addWidget(self.mid_main)
        self.mid_layout.addSpacing(40)
        self.mid_main_layout.addSpacing(90)
        self.mid_main_layout.addWidget(self.mid_main_this)
        self.mid_main_layout.addSpacing(90)

    def mid_main_this_ui(self):
        self.mid_main_this = QWidget()
        self.mid_main_this_layout = MyVBoxLayout()
        self.mid_main_this.setLayout(self.mid_main_this_layout)
        self.mid_main_this.setFixedHeight(460)
        self.mid_main_this.setFixedWidth(700 )
        self.mid_main.setObjectName('mid_main_this')
        
        self.mid_row1 = QWidget()
        self.mid_row1_layout = MyHBoxLayout()
        self.mid_row1.setLayout(self.mid_row1_layout)
        self.mid_row1.setObjectName('mid_row1')
        self.mid_row1.setFixedHeight(30)

        self.mid_row2 = QWidget()
        self.mid_row2_layout = MyHBoxLayout()
        self.mid_row2.setLayout(self.mid_row2_layout)
        self.mid_row2.setObjectName('mid_row2')
        self.mid_row2.setFixedHeight(30)
        # self.mid_out = QWidget()

        # 定义控件
        self.mid_id_t = QLabel('小说ID：')
        self.mid_id_t.setObjectName('mid_t')
        self.mid_id_t.setFixedSize(120, 30)

        self.mid_id_input = QLineEdit()
        self.mid_id_input.setObjectName('mid_input')
        self.mid_id_input.setFixedSize(470, 30)

        self.mid_download = QPushButton('下载')
        self.mid_download.setObjectName('mid_but')
        self.mid_download.setFixedSize(80, 30)
        self.mid_download.setCursor(QCursor(Qt.PointingHandCursor))
        # self.mid_download.

        self.mid_path_t = QLabel('下载地址：')
        self.mid_path_t.setObjectName('mid_t')
        self.mid_path_t.setFixedSize(120, 30)

        self.mid_path_input = QLineEdit()
        self.mid_path_input.setObjectName('mid_input')
        self.mid_path_input.setFixedSize(470, 30)

        self.mid_path_button = QPushButton('浏览')
        self.mid_path_button.setObjectName('mid_but')
        self.mid_path_button.setFixedSize(80, 30)
        self.mid_path_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.mid_console = QTextEdit()
        self.mid_console.setObjectName('mid_c')

        # 设置默认值
        self.mid_id_input.setText('5')
        self.mid_path_input.setText(self.novel_path)
        
        self.mid_main_this_layout.addWidget(self.mid_row1)
        self.mid_main_this_layout.addSpacing(60)
        self.mid_main_this_layout.addWidget(self.mid_row2)
        self.mid_main_this_layout.addSpacing(60)
        self.mid_main_this_layout.addWidget(self.mid_console)
        self.mid_row1_layout.addWidget(self.mid_id_t)
        self.mid_row1_layout.addWidget(self.mid_id_input)
        self.mid_row1_layout.addSpacing(30)
        self.mid_row1_layout.addWidget(self.mid_download)
        self.mid_row2_layout.addWidget(self.mid_path_t)
        self.mid_row2_layout.addWidget(self.mid_path_input)
        self.mid_row2_layout.addSpacing(30)
        self.mid_row2_layout.addWidget(self.mid_path_button)

        # 信号连接动作
        self.mid_path_button.clicked.connect(self.get_path)
        self.mid_download.clicked.connect(self.novel_download)

    # 底部信息栏-暂定没有
    def init_bottom_ui(self):
        self.bottom_widget = QWidget()
        self.bottom_layout = MyGridLayout()
        self.bottom_widget.setLayout(self.bottom_layout)
        self.bottom_widget.setObjectName('bottom')

    # 功能实现
    # 浏览目录获取路径
    def get_path(self):
        self.mid_path_input.setText(QFileDialog.getExistingDirectory(self, '请选择下载路径', self.novel_path))
    
    # 下载小说
    def novel_download(self):
        # 创建线程
        self.thread = NovelThead(self.mid_id_input.text(),self.mid_path_input.text())
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.thread.start()

    # 输出控制台
    def outputWritten(self, text):
        cursor = self.mid_console.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.mid_console.setTextCursor(cursor)
        self.mid_console.ensureCursorVisible()

    def isTop(self, this):
        if this.x() > 300 and this.y() < 40:
            return True 

    def mousePressEvent(self, e):
        
        if e.button() == Qt.LeftButton and self.isTop(e):
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())
    
    def mouseMoveEvent(self, e):  # 重写移动事件
        if self._isTracking: 
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.isTop(e):
            self._isTracking = False
            self._startPos = QPoint(0, 0)
            self._endPos = QPoint(0, 0)
    # 主函数
    def main_Q(self):
        with open('./style.qss','r', encoding='utf-8') as f:
            qssStyle = f.read()
        self.setStyleSheet(qssStyle)
        self.show()


# 定义下载小说的线程类
class NovelThead(QThread):
    def __init__(self, id, path):
        super(NovelThead, self).__init__()
        self.id = id
        self.path = path
    def __del__(self):
        self.wait()
    # 设置run的文件
    def run(self):
        self.novel_d = Novel(self.id, self.path)
        self.novel_d.main_novel_download()
# 定义控制器输出
class EmittingStr(QObject):
    # 定义一个发送str的信号
    textWritten = pyqtSignal(str)
    def write(self, text):
        # 发送信号str
        self.textWritten.emit(str(text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建窗口
    ui_main = Test()
    ui_main.main_Q()
    sys.exit(app.exec_())






    # self.browser = QWebEngineView()
    # url = QUrl(QFileInfo("./html/index.html").absoluteFilePath())
    # self.browser.load(url)
    # self.setCentralWidget(self.browser)