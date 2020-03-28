import os
from PyQt5.QtCore import *
import pandas as pd
from utils import predict_pictures_with_model


class PredictPicturesThread(QThread):
    piedict_pictures_finished=pyqtSignal(str)
    def __init__(self,src_path,save_path,model_path):
        super().__init__()
        self.src_path=src_path
        self.save_path=save_path
        self.model_path=model_path
        print('构造完毕')


    def run(self):
        predicts=[]
        fname=[]
        if os.path.exists(self.src_path):
            files = os.listdir(self.src_path)
            num=0
            for f in files:
                path = os.path.join(self.src_path, f)
                predict = predict_pictures_with_model.predict_with_model(path, self.model_path)
                label='real' if predict==1 else 'fake'
                predicts.append(label)
                fname.append(f)
                print(predict)
                self.piedict_pictures_finished.emit(str(num))
                num+=1
            results=[]
            results.append(fname,predicts)
            df=pd.DataFrame(predicts,columns=['picture_name','prediction'])
            df.to_csv(self.save_path)
        else:
            print('路径错误')

    def __del__(self):
        self.wait()

