import sys
from PyQt5.QtCore import *
import time
from utils import video_frame_save

class ExtractPicFacesThread(QThread):
    split_finish=pyqtSignal(int)
    def __init__(self,src_path=None,save_path=None,f_w=None,f_h=None):
        super().__init__()
        self.src_path=src_path
        self.save_path=save_path
        self.width=f_w
        self.height=f_h

        print('构造完毕')


    def run(self):
        print('正在执行')
        # 如何实施的传递参数
        count=video_frame_save.extract_faces_from_pictures(self.src_path,self.save_path,
                                        self.width,self.height)

        self.split_finish.emit(count)

    def __del__(self):
        self.wait()

