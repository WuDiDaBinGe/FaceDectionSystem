import sys
from PyQt5.QtCore import *
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from utils import video_frame_save

class SplitVideoThreads(QThread):
    split_finish=pyqtSignal(int)
    def __init__(self,src_path,save_path,interval,f_start,f_end,f_w,f_h):
        super().__init__()
        self.video_src_path=src_path
        self.frame_save_path=save_path
        self.interval=interval
        self.start_frame = f_start
        self.end_frame = f_end
        self.frame_width=f_w
        self.frame_height=f_h

        print('构造完毕')


    def run(self):
        print('正在执行')
        # 如何实施的传递参数
        count=video_frame_save.video_to_frame(self.video_src_path,self.frame_save_path,
                                        self.interval,self.start_frame,self.end_frame,
                                        self.frame_width,self.frame_height)

        self.split_finish.emit(count)
    def __del__(self):
        self.wait()

