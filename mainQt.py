import sys
import time
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from python_spider_train.spider.novel_download import Novel
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Test')
        self.setFixedSize(1280, 720)
        self.setWindowIcon(QIcon('./128x128.icon'))
        self.novel_path = os.path.dirname(os.path.abspath(__file__)) + '/novel'
        self.thread = None
        self.init_ui()
        self.show()

    # 初始化UI
    def init_ui(self):
        # 主窗口
        self.main_widget = QWidget()
        # 创建主窗口的网格布局
        self.main_layout = QGridLayout()
        # 设置主窗口为网格布局
        self.main_widget.setLayout(self.main_layout)
        # 左侧菜单栏
        self.init_left_ui()
        # 右侧内容栏
        self.init_right_ui()
        # 布局设置
        # 从第0行第0列开始，占12行2列
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)
        # 从第0行第2列开始，占12行10列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)
        # 设置main里的主部件
        self.setCentralWidget(self.main_widget)

    # 左侧的菜单UI
    def init_left_ui(self):
        self.left_widget = QWidget()
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        # 定义控件
        # 关闭按钮
        self.left_close = QPushButton('')
        # 空白按钮
        self.left_visit = QPushButton('')
        # 最小化按钮
        self.left_mini = QPushButton('')
        # 爬虫程序标签
        self.left_label1 = QPushButton('爬虫程序')
        self.left_label1.setObjectName('left_label')
        # 小说下载按钮
        self.left_button1 = QPushButton('小说下载')
        self.left_button1.setObjectName('left_button')
        # Pixiv下载按钮
        self.left_button2 = QPushButton('Pixiv下载')
        self.left_button2.setObjectName('left_button')
        # 更多功能
        self.left_buttonm = QPushButton('更多功能开发中...')
        self.left_buttonm.setObjectName('left_button')

        # 布局
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_label1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_buttonm, 4, 0, 2, 3)

    # 右侧内容UI
    def init_right_ui(self):
        self.right_widget = QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        # 定义控件
        self.right_id_t = QLabel('小说id：')
        self.right_id_input = QLineEdit()
        self.right_path_t = QLabel('小说下载地址：')
        self.right_path_input = QLineEdit()
        self.right_path_button = QPushButton('浏览')
        self.right_download = QPushButton('下载')
        self.right_console = QTextEdit()

        # 设置默认值
        self.right_id_input.setText('5')
        self.right_path_input.setText(self.novel_path)

        # 布局
        self.right_layout.addWidget(self.right_id_t, 1, 1, 1, 1)
        self.right_layout.addWidget(self.right_id_input, 1, 2, 1, 8)
        self.right_layout.addWidget(self.right_path_t, 2, 1, 1, 1)
        self.right_layout.addWidget(self.right_path_input, 2, 2, 1, 7)
        self.right_layout.addWidget(self.right_path_button, 2, 9, 1, 1)
        self.right_layout.addWidget(self.right_download, 3, 7, 1, 2)
        self.right_layout.addWidget(self.right_console, 4, 2, 2, 7)

        # 信号连接动作
        self.right_path_button.clicked.connect(self.get_path)
        self.right_download.clicked.connect(self.novel_download)

    # 浏览目录获取路径
    def get_path(self):
        self.right_path_input.setText(QFileDialog.getExistingDirectory(self, '请选择下载路径', self.novel_path))
    # 下载小说
    def novel_download(self):
        # 创建线程
        self.thread = NovelThead(self.right_id_input.text(),self.right_path_input.text())
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.thread.start()

    def outputWritten(self, text):
        cursor = self.right_console.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.right_console.setTextCursor(cursor)
        self.right_console.ensureCursorVisible()


#定义下载小说的线程类
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
    sys.exit(app.exec_())






    # self.browser = QWebEngineView()
    # url = QUrl(QFileInfo("./html/index.html").absoluteFilePath())
    # self.browser.load(url)
    # self.setCentralWidget(self.browser)