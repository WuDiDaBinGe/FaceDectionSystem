from PyQt5.QtCore import *
import cv2
import dlib
from utils import tools

class SplitVideoThreads(QThread):
    split_finish=pyqtSignal(dict)
    all_finished=pyqtSignal(dict)
    def __init__(self,src_path=None,save_path=None,interval=None,f_start=None,f_end=None,f_w=None,f_h=None):
        super().__init__()
        self.video_src_path=src_path
        self.frame_save_path=save_path
        self.interval=interval
        self.start_frame = f_start
        self.end_frame = f_end
        self.frame_width=f_w
        self.frame_height=f_h

        self.run_flag=True
        print('构造完毕')


    def run(self):
        video_src_path=self.video_src_path
        frame_save_path=self.frame_save_path
        start_frame=self.start_frame
        end_frame=self.end_frame
        interval=self.interval
        w=self.frame_width
        h=self.frame_height

        # 传递参数
        info_dict={}
        info_dict['src'] = self.video_src_path
        info_dict['out'] = self.frame_save_path
        info_dict['total'] = tools.get_split_video_total(self.start_frame, self.end_frame, self.interval)
        print("正在分割视频：" + format(video_src_path))
        # 取出视频的名称
        video_name = video_src_path.split('/')[-1].split('.')[0]

        print(video_name)
        cap = cv2.VideoCapture(video_src_path)

        face_detector = dlib.get_frontal_face_detector()
        total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("总共的帧数为{}".format(total_frame))

        assert start_frame < total_frame - 1
        assert end_frame <= total_frame

        frame_index = 0
        frame_count = 0
        while (cap.isOpened() and self.run_flag):
            ret, frame = cap.read()
            print("正在读取第%d帧" % frame_index)
            if frame_index < start_frame:
                frame_index+=1
                continue
            if ret and (frame_index-start_frame) % interval == 0:

                f_height, f_width = frame.shape[:2]
                # 转化成gray
                gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_detector(gray_img, 1)
                if len(faces):
                    face = faces[0]

                    x, y, size = tools.get_boundingbox(face, f_width, f_height)

                    face = frame[y:y + size, x:x + size]
                    if w is not None and h is not None:
                        face = cv2.resize(face, (w, h), interpolation=cv2.INTER_LINEAR)
                    print(face.shape)
                    # 将frame 保存到指定的路径下
                    cv2.imwrite(frame_save_path + '/' + video_name + '_%d.jpg' % frame_count, face)
                    print(".....保存了第%d幅图片" % frame_count)
                    frame_count += 1

            info_dict['current'] = frame_index
            info_dict['count'] = frame_count
            step=frame_index-start_frame
            step=0 if step<0 else step
            info_dict['step']= step
            self.split_finish.emit(info_dict)
            frame_index += 1
            # 这里一定要加 要不然会一直循环下去
            if frame_index > end_frame:
                break
        self.all_finished.emit(info_dict)
        cap.release()
        print("分割完毕！")

    def __del__(self):
        self.wait()

    def quit_(self):
        self.run_flag=False
    def start_(self):
        self.run_flag=True



