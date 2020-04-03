import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from PyQt5.QtCore import *
from utils import tools
from models.research.deeplab.core import xception
from utils.cosnt_value import IMG_SIZE,NUM_CLASS
import tensorflow as tf
import cv2
import dlib
import numpy as np

class DetectVideoThread(QThread):
    detect_video_finished=pyqtSignal(dict)
    all_finished=pyqtSignal(dict)
    model_error=pyqtSignal()
    fake_face=0
    real_face=0
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
        video_src_path = self.src_path
        start_frame = self.startframe
        end_frame = self.endframe
        out_video_path = self.save_path
        model_path = self.model_path
        # 加载模型
        if self.model_init(model_path):

            info_dict={}
            result_dict={}
            print("正在分割视频：" + format(self.src_path))

            print('模型加载成功')
            # 取出视频的名称
            video_name = video_src_path.split('/')[-1].split('.')[0]

            print(video_name)

            # Reader and Writer
            cap = cv2.VideoCapture(video_src_path)
            video_fn = video_name + '.avi'  # 输出视频的名称
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            writer = None
            # Text variables
            font_face = cv2.FONT_HERSHEY_SIMPLEX
            thickness = 2
            font_scale = 1

            face_detector = dlib.get_frontal_face_detector()

            assert start_frame < total_frame - 1
            assert end_frame <= total_frame
            print("xnsanx2")
            frame_index = 0
            list_frame_index=[]
            list_frame_predict=[]
            while (cap.isOpened() and self.run_flag):
                ret, frame = cap.read()
                print("正在读取第%d帧" % frame_index)
                frame_index += 1

                if frame_index < start_frame:
                    continue

                if ret:
                    f_height, f_width = frame.shape[:2]
                    print(os.path.join(out_video_path, video_fn))
                    # Init output writer
                    if writer is None:
                        writer = cv2.VideoWriter(os.path.join(out_video_path, video_fn), fourcc, fps,
                                                 (f_height, f_width)[::-1])

                    # 转化成gray
                    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_detector(gray_img, 1)
                    if len(faces):
                        face = faces[0]

                        x, y, size = tools.get_boundingbox(face, f_width, f_height)
                        # face 为人脸二次区域
                        cropped_face = frame[y:y + size, x:x + size]
                        # 预测
                        predict = self.predict_with_model(cropped_face)
                        if predict==1:
                            self.real_face+=1
                        else:
                            self.fake_face+=1
                        list_frame_index.append(frame_index)
                        list_frame_predict.append(predict)

                        info_dict['src']=video_src_path
                        info_dict['index']=frame_index
                        info_dict['predict']='real' if predict==1 else 'fake'
                        info_dict['out']=os.path.join(out_video_path, video_fn)
                        info_dict['start']=start_frame
                        info_dict['end']=end_frame
                        info_dict['total']=total_frame
                        step=frame_index-start_frame
                        step=0 if step<0 else step
                        info_dict['step']=step
                        self.detect_video_finished.emit(info_dict)
                        # -----------------------------------------------
                        # Text
                        x = face.left()
                        y = face.top()
                        w = face.right() - x
                        h = face.bottom() - y

                        label = 'real' if predict == 1 else 'fake'
                        color = (0, 0, 255) if predict == 0 else (0, 255, 0)
                        # 图片中加上文字
                        cv2.putText(frame, label, (x, y + h + 30),
                                    font_face, font_scale,
                                    color, thickness, 2)
                        # draw box over face
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    writer.write(frame)
                # 这里一定要加,要不然会一直循环下去
                if frame_index > end_frame:
                    break
            print("分割完毕！")
            result_dict['fake_num']=self.fake_face
            result_dict['real_num']=self.real_face
            result_dict['x']=np.array(list_frame_index)
            result_dict['y']=np.array(list_frame_predict)
            self.all_finished.emit(result_dict)
            cap.release()
            if writer is not None:
                writer.release()
                print('Finished! Output saved under {}'.format(out_video_path))
            else:
                print('Input video file was empty')
        else:
            self.model_error.emit()

    def __del__(self):
        self.wait()

    def quit_(self):
        self.run_flag=False
    def start_(self):
        self.run_flag=True
    def model_init(self,model_path):
        self.x_ = tf.placeholder(tf.float32, [None, IMG_SIZE, IMG_SIZE, 3])

        with tf.contrib.slim.arg_scope(xception.xception_arg_scope()):
            net, end_point = xception.xception_41(self.x_, NUM_CLASS, is_training=False)

        logits = tf.reshape(net, (-1, 2))
        self.prediction = tf.argmax(tf.nn.softmax(logits), 1)

        self.saver = tf.train.Saver()

        self.sess=tf.Session()
        init_op = tf.group(tf.global_variables_initializer())
        self.sess.run(init_op)
        ckpt = tf.train.get_checkpoint_state(model_path)
        if ckpt and ckpt.model_checkpoint_path:
            print(ckpt.model_checkpoint_path)
            self.saver.restore(self.sess, ckpt.model_checkpoint_path)
            return True
        else:
            return False

    def predict_with_model(self,image):
        image=tools.process_pictures(image)
        predict=self.sess.run(self.prediction,{self.x_:image})
        print(predict)
        return predict[0]




