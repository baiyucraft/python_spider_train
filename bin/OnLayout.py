from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QStackedLayout

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
# 页面切换布局
class MyStackedLayout(QStackedLayout):
    def __init__(self):
        super(MyStackedLayout, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
