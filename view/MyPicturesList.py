import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QListWidget, QListView, QHBoxLayout, QListWidgetItem
import os

pictures_path="F:\\dataset\\example"
class MyPicturesListWidget(QWidget):
    def __init__(self, img_w=150,img_h=100,parent=None):
        super(MyPicturesListWidget, self).__init__(parent)

        self.img_w=img_w
        self.img_h=img_h
        self.setupUi()

    def setupUi(self):

        self.iconlist = QListWidget()
        self.iconlist.setViewMode(QListView.IconMode)
        self.iconlist.setSpacing(2)

        self.iconlist.setMovement(False)
        self.iconlist.setResizeMode(QListView.Adjust)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.iconlist)

        self.setLayout(hlayout)


    def additems(self,pictures_path):
        # 读取缩略图
        files = os.listdir(pictures_path)
        for f1 in files:
            path=os.path.join(pictures_path,f1)
            pix1 = QPixmap(path)
            item1 = QListWidgetItem(QIcon(pix1.scaled(self.img_w, self.img_h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)),
                                    os.path.split(f1)[-1])
            self.iconlist.addItem(item1)

    def update(self,pictures_path):
        self.img_w=self.width()/2.5
        self.img_h=self.img_w/3*2
        #显示两列图片
        self.iconlist.setIconSize(QSize(self.img_w, self.img_h))
        # 先清空列表，再添加
        self.iconlist.clear()
        self.additems(pictures_path)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = MyPicturesListWidget(150, 100)
    mainwin.update(pictures_path)
    sys.exit(app.exec_())
