import sys
from PyQt5.QtCore import *
import time
from utils import predict_video_with_model

class DetectVideoThread(QThread):
    detect_video_finished=pyqtSignal(str)

    def __init__(self,src_path=None,save_path=None,model_path=None,startframe=None,end_frame=None):
        super().__init__()
        self.src_path=src_path
        self.save_path=save_path
        self.model_path=model_path
        self.startframe=startframe
        self.endframe=end_frame
        self.run_flag=True
        print('构造完毕')


    def run(self):
        print('正在执行')
        while(self.run_flag):
            endpoints=predict_video_with_model.detect_from_video(self.src_path,self.save_path,self.model_path,
                                                       self.startframe,self.endframe)
            self.run_flag=False
            self.detect_video_finished.emit(str(endpoints))

    def __del__(self):
        self.wait()

    def quit_(self):
        self.run_flag=False