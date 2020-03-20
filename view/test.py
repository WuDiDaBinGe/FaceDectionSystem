from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtCore import *
import time


# 继承QThread
class Runthread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.2)
            self._signal.emit(str(i))  # 注意这里与_signal = pyqtSignal(str)中的类型相同


class Example(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # 按钮初始化
        self.button = QtWidgets.QPushButton('开始', self)
        self.button.setToolTip('这是一个 <b>QPushButton</b> widget')
        self.button.resize(self.button.sizeHint())
        self.button.move(120, 80)
        self.button.clicked.connect(self.start_login)  # 绑定多线程触发事件

        # 进度条设置
        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setGeometry(50, 50, 210, 25)
        self.pbar.setValue(0)

        # 窗口初始化
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('OmegaXYZ.com')
        self.show()

        self.thread = None  # 初始化线程

    def start_login(self):
        # 创建线程
        self.thread = Runthread()
        # 连接信号
        self.thread._signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
        # 开始线程
        self.thread.start()

    def call_backlog(self, msg):
        self.pbar.setValue(int(msg))  # 将线程的参数传入进度条


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = Example()
    myshow.show()
    sys.exit(app.exec_())
