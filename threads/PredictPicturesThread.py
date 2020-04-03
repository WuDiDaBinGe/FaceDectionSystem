import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from PyQt5.QtCore import *
import pandas as pd
import numpy as np
import tensorflow as tf
from models.research.deeplab.core import xception
from utils import tools
import utils.cosnt_value as cosnt_value

class PredictPicturesThread(QThread):
    piedict_pictures_finished=pyqtSignal(dict)
    all_finished=pyqtSignal(dict,dict)
    model_error=pyqtSignal()
    fake_num=0
    real_num=0
    def __init__(self,src_path=None,save_path=None,model_path=None):
        super().__init__()
        self.src_path=src_path
        self.save_path=save_path
        self.model_path=model_path
        self.flag_run=True
        print('构造完毕')


    def run(self):
        if self.model_init(self.model_path):
            print('模型加载完成')
            predicts_label=[]
            predicts=[]
            fname=[]
            # 回传的字典信息
            dict_info={}
            result_info={}
            if os.path.exists(self.src_path):
                files = os.listdir(self.src_path)
                num=1
                pic_count = 0
                for f in files:
                    pic_type=f.split('.')
                    if pic_type[-1] not in cosnt_value.accept_pictures_type:
                        num+=1
                        continue
                    path = os.path.join(self.src_path, f)
                    predict = self.predict_with_model(path)
                    if predict==1:
                        self.real_num+=1
                    else:
                        self.fake_num+=1
                    predicts.append(predict)
                    label='real' if predict==1 else 'fake'
                    predicts_label.append(label)
                    fname.append(f)
                    print(predict)
                    dict_info['fname']=f
                    dict_info['label']=label
                    dict_info['num']=num
                    self.piedict_pictures_finished.emit(dict_info)
                    num+=1
                    pic_count += 1
                    if self.flag_run==False:
                        break

                result_info['f_name']=fname
                result_info['labels']=predicts_label
                result_info['fake_num']=self.fake_num
                result_info['real_num']=self.real_num
                result_info['y']=np.array(predicts)
                result_info['x']=np.arange(1,pic_count+1)


                # 写文件
                predicts_label = np.array(predicts_label)
                fname = np.array(fname)
                data = np.column_stack((fname, predicts_label))
                data = pd.DataFrame(data, columns=['pictures_name', 'predictions'])
                data.to_csv(self.save_path + '/predict_pics_result.csv')
                dict_info['out'] = self.save_path + '/predict_pics_result.csv'
                # 发送完成信号
                self.all_finished.emit(dict_info, result_info)
            else:
                print('路径错误')
        else:
            self.model_error.emit()

    def __del__(self):
        self.wait()
    def quit_(self):
        self.flag_run=False
    def start_(self):
        self.flag_run=True
    def model_init(self,model_path):
        self.x_ = tf.placeholder(tf.float32, [None, cosnt_value.IMG_SIZE, cosnt_value.IMG_SIZE, 3])

        with tf.contrib.slim.arg_scope(xception.xception_arg_scope()):
            net, end_point = xception.xception_41(self.x_, cosnt_value.NUM_CLASS, is_training=False)

        logits = tf.reshape(net, (-1, 2))
        self.prediction = tf.argmax(tf.nn.softmax(logits), 1)

        saver = tf.train.Saver()

        self.sess=tf.Session()
        init_op = tf.group(tf.global_variables_initializer())
        self.sess.run(init_op)
        ckpt = tf.train.get_checkpoint_state(model_path)
        if ckpt and ckpt.model_checkpoint_path:
            print(ckpt.model_checkpoint_path)
            saver.restore(self.sess, ckpt.model_checkpoint_path)
            return True
        else:
            return False

    def predict_with_model(self,path):
        image = tools.load_img(path)
        predict = self.sess.run(self.prediction, {self.x_: image})
        return predict[0]


if __name__ == '__main__':
    predics=['real','fake','real']
    fname=['1.jpg','2.jpg','3.jpg']
    predics=np.array(predics)
    fname=np.array(fname)

    data=np.column_stack((fname,predics))
    data=pd.DataFrame(data,columns=['pictures_name','predictions'])

