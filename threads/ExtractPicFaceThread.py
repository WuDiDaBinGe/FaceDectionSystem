import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
import cv2
import dlib
from utils import cosnt_value
from PyQt5.QtCore import *
from utils import tools

class ExtractPicFacesThread(QThread):
    extract_finish=pyqtSignal(dict)
    all_finished=pyqtSignal(dict)
    def __init__(self,src_path=None,save_path=None,f_w=None,f_h=None):
        super().__init__()
        self.src_path=src_path
        self.save_path=save_path
        self.width=f_w
        self.height=f_h
        self.run_flag=True
        print('构造完毕')

    def run(self):
        pics_path=self.src_path
        out_path=self.save_path
        pic_width=self.width
        pic_height=self.height
        info_dict={}
        info_dict['src'] = self.src_path
        info_dict['out']=self.save_path
        print('正在执行')
        face_detector = dlib.get_frontal_face_detector()
        files = os.listdir(pics_path)
        count = 0
        f_index=1
        for f in files:
            if self.run_flag==False:
                break
            pic_name = f.split('.')[0]
            pic_type = f.split('.')[-1]
            if pic_type not in cosnt_value.accept_pictures_type:
                f_index+=1
                continue
            path = os.path.join(pics_path, f)
            picture = cv2.imread(path)
            f_height, f_width = picture.shape[:2]
            # 转化成gray
            gray_img = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
            faces = face_detector(gray_img, 1)
            if len(faces):
                face = faces[0]
                x, y, size = tools.get_boundingbox(face, f_width, f_height)
                face = picture[y:y + size, x:x + size]
                if pic_width is not None and pic_height is not None:
                    face = cv2.resize(face, (pic_width, pic_height), interpolation=cv2.INTER_LINEAR)
                print(face.shape)
                # 将frame 保存到指定的路径下
                cv2.imwrite(out_path + '/' + pic_name + '_face.jpg', face)
                count = count + 1
            info_dict['step']=f_index
            info_dict['num']=count
            info_dict['total']=len(files)
            self.extract_finish.emit(info_dict)
            f_index+=1
        self.all_finished.emit(info_dict)

    def __del__(self):
        self.wait()

    def quit_(self):
        self.run_flag=False
    def start_(self):
        self.run_flag=True

