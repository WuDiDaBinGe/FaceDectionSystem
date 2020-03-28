import os
from PyQt5.QtCore import *
import pandas as pd
from utils import predict_pictures_with_model
import numpy as np
import utils.cosnt_value as cosnt_value

class PredictPicturesThread(QThread):
    piedict_pictures_finished=pyqtSignal(str)
    def __init__(self,src_path=None,save_path=None,model_path=None):
        super().__init__()
        self.src_path=src_path
        self.save_path=save_path
        self.model_path=model_path
        self.flag_run=True
        print('构造完毕')


    def run(self):
        predicts=[]
        fname=[]
        # 回传的字典信息
        dict_info={}
        if os.path.exists(self.src_path):
            files = os.listdir(self.src_path)
            num=1
            for f in files:
                pic_type=f.split('.')
                if pic_type[-1] not in cosnt_value.accept_pictures_type:
                    num+=1
                    continue
                path = os.path.join(self.src_path, f)
                predict = predict_pictures_with_model.predict_with_model(path, self.model_path)
                label='real' if predict==1 else 'fake'
                predicts.append(label)
                fname.append(f)
                print(predict)
                dict_info['fname']=f
                dict_info['label']=label
                dict_info['num']=num
                self.piedict_pictures_finished.emit(str(dict_info))
                num+=1
                if self.flag_run==False:
                    break
            predicts=np.array(predicts)
            fname=np.array(fname)
            data=np.column_stack((fname,predicts))
            data=pd.DataFrame(data,columns=['pictures_name','predictions'])
            data.to_csv(self.save_path+'/predict_pics_result.csv')
        else:
            print('路径错误')

    def __del__(self):
        self.wait()
    def quit_(self):
        self.flag_run=False
if __name__ == '__main__':
    predics=['real','fake','real']
    fname=['1.jpg','2.jpg','3.jpg']
    predics=np.array(predics)
    fname=np.array(fname)

    data=np.column_stack((fname,predics))
    data=pd.DataFrame(data,columns=['pictures_name','predictions'])

