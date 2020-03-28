import sys
from PyQt5.QtCore import *
import time
from utils import predict_video_with_model

class DetectVideoThread(QThread):
    detect_video_finished=pyqtSignal(str)
    def __init__(self,src_path,save_path,model_path,startframe,end_frame):
        super().__init__()
        self.src_path=src_path
        self.save_path=save_path
        self.model_path=model_path
        self.startframe=startframe
        self.endframe=end_frame

        print('构造完毕')


    def run(self):
        print('正在执行')
        endpoints=predict_video_with_model.detect_from_video(self.src_path,self.save_path,self.model_path,
                                                   self.startframe,self.endframe)

        self.detect_video_finished.emit(str(endpoints))

    def __del__(self):
        self.wait()

