import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# 定义控制器输出
class EmittingStr(QObject):
    # 定义一个发送str的信号
    textWritten = pyqtSignal(str)
    def write(self, text):
        # 发送信号str
        self.textWritten.emit(str(text))
# 自定义窗体
class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.path = os.getcwd()
        self.thread = None

    # 获取地址
    def get_path(self):
        self.path = QFileDialog.getExistingDirectory(self, '请选择下载路径', self.path)
        self.path_input.setText(self.path)

    # 输出控制台
    def outputWritten(self, text):
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.console.setTextCursor(cursor)
        self.console.ensureCursorVisible()