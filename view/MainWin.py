import sys
import os
from PyQt5.QtWidgets import *
from view.My_Tabs import MyTabs
from view.MyPicturesList import MyPicturesListWidget
import utils.cosnt_value as cons_value
from utils import tools,video_frame_save
from threads import SplitVideoThreads,ExtractPicFaceThread,DetectVideoThread,PredictPicturesThread



class MainWin(QMainWindow):

    def __init__(self):
        super(MainWin, self).__init__()
        self.initUI()

        self.action_widget_associate()
        self.split_thread=None
    def initUI(self):
        self.tabs_top=MyTabs(self)
        self.tabs_top.setObjectName('top_table')

        self.list_pictures=MyPicturesListWidget()
        self.list_pictures.setObjectName('list_pictures')

        frame_mid_right1=QFrame(self)
        frame_mid_right1.setFrameShape(QFrame.StyledPanel)
        frame_mid_right1.setObjectName("frame_mid_right1")

        # 信息提示区域
        self.label_info=QLabel(frame_mid_right1)
        self.label_info.setObjectName("label_info")
        self.label_info.setText("提示信息区域")


        frame_mid_right2 = QFrame(self)
        frame_mid_right2.setFrameShape(QFrame.StyledPanel)
        frame_mid_right2.setObjectName("frame_mid_right2")

        vbox_mid_right = QVBoxLayout(self)
        vbox_mid_right.setObjectName('vbox_mid_right')
        vbox_mid_right.addWidget(frame_mid_right1)
        vbox_mid_right.setStretchFactor(frame_mid_right1,2)
        vbox_mid_right.addWidget(frame_mid_right2)
        vbox_mid_right.setStretchFactor(frame_mid_right2, 8)

        hbox_mid=QHBoxLayout()
        hbox_mid.addWidget(self.list_pictures)
        hbox_mid.setStretchFactor(self.list_pictures,3)
        hbox_mid.addLayout(vbox_mid_right)
        hbox_mid.setStretchFactor(vbox_mid_right,7)


        self.btn_Start=QPushButton("开始",self)
        self.btn_Stop=QPushButton("停止",self)
        hbox_bottom=QHBoxLayout()
        hbox_bottom.addWidget(self.btn_Start)
        hbox_bottom.addWidget(self.btn_Stop)
        hbox_bottom.addStretch(1)

        vbox_main=QVBoxLayout()
        vbox_main.addWidget(self.tabs_top)
        vbox_main.setStretchFactor(self.tabs_top,2)
        vbox_main.addLayout(hbox_mid)
        vbox_main.setStretchFactor(hbox_mid,8)
        vbox_main.addLayout(hbox_bottom)
        vbox_main.setStretchFactor(hbox_bottom,1)


        center_widget = QWidget()
        center_widget.setLayout(vbox_main)
        self.setCentralWidget(center_widget)

        self.setGeometry(300,300,1219,769)
        self.setWindowTitle('人脸合成图像检测系统')
        self.useQss()
        self.show()


    def action_widget_associate(self):
        self.tabs_top.line_in_video_path.textChanged.connect(self.update_info_invideo)
        self.tabs_top.currentChanged.connect(self.start_btn_changed_slot)
        self.tabs_top.group_ways.buttonClicked.connect(self.ways_clicked)
    def useQss(self):
        with open('MainWin.qss') as file:
            str = file.readlines()
            str = ''.join(str).strip('\n')
        self.setStyleSheet(str)



    def update_info_invideo(self):
        '''
        当输入视频改变的时候，改变提示框内容，显示选择视频的信息
        :return: null
        '''
        file_name=self.tabs_top.video_in_path
        file_name=file_name.split('/')[-1]
        total_frame=tools.get_video_total_frame(self.tabs_top.video_in_path)
        str=cons_value.video_in_info.format(file_name,total_frame)

        self.label_info.setText(str)
        self.label_info.adjustSize()

    def showPictures(self):
        self.pictures_file_path = self.tabs_top.input_pictures_path
        if self.pictures_file_path:
            self.list_pictures.update(self.pictures_file_path)
        else:
            print(self.pictures_file_path)

    def spilt_video(self):
        video_src_path=self.tabs_top.video_in_path
        frame_save_path=self.tabs_top.frame_save_path
        if video_src_path is not None and frame_save_path is not None:
            start_frame = self.tabs_top.textline_start_frame.text()
            if start_frame=='':
                start_frame=0
            else:
                start_frame=int(start_frame)

            end_frame = self.tabs_top.textline_end_frame.text()
            if end_frame=='':
                end_frame=tools.get_video_total_frame(video_src_path)
            else:
                end_frame=int(end_frame)

            interval = self.tabs_top.textline_interval_frame.text()
            if interval=='':
                interval=1
            else:
                interval=int(interval)

            frame_width = self.tabs_top.textline_frame_width.text()
            if frame_width=='':
                frame_width=None
            else:
                frame_width=int(frame_width)

            frame_height = self.tabs_top.textline_frame_height.text()
            if frame_height=='':
                frame_height=None
            else:
                frame_height=int(frame_height)


            self.split_thread = SplitVideoThreads.SplitVideoThreads(video_src_path,frame_save_path,
                                                                    interval,start_frame,end_frame,
                                                                    frame_width,frame_height)

            self.split_thread.split_finish.connect(self.split_video_info)
            self.split_thread.start()
            self.label_info.setText("正在分割视频中....")
            self.label_info.adjustSize()
        else:
            QMessageBox.information(self, '提示', '输入输出路径不能为空！')

    def detect_video(self):
        video_src_path = self.tabs_top.video_in_path
        video_save_path = self.tabs_top.line_outresult_file_path.text()
        model_path=self.tabs_top.model_path
        if video_src_path is not None and video_save_path != '' and model_path is not None:
            start_frame = self.tabs_top.textline_start_frame.text()
            if start_frame == '':
                start_frame = 0
            else:
                start_frame = int(start_frame)

            end_frame = self.tabs_top.textline_end_frame.text()
            if end_frame == '':
                end_frame = tools.get_video_total_frame(video_src_path)
            else:
                end_frame = int(end_frame)
            self.detect_video_thread = DetectVideoThread.DetectVideoThread(video_src_path,video_save_path,model_path,
                                                                           start_frame,end_frame)

            self.detect_video_thread.detect_video_finished.connect(self.detect_video_info)
            self.detect_video_thread.start()
            self.label_info.setText(cons_value.detect_video_info.format(video_src_path, video_save_path, model_path,
                                                                        start_frame, end_frame))
            self.label_info.adjustSize()

        else:
            QMessageBox.information(self, '提示', '输入输出路径不能为空！')

    def split_video_info(self,num):
        self.label_info.setText('一共分割了{}张图片'.format(num))
        self.label_info.adjustSize()
        if self.tabs_top.frame_save_path:
            self.list_pictures.update(self.tabs_top.frame_save_path)

    def detect_video_info(self,str):
        self.label_info.setText(str)
        self.label_info.adjustSize()


    def extract_pictures_face(self):
        pics_src_path=self.tabs_top.input_pictures_path
        faces_pics_save_path=self.tabs_top.pics_extract_path
        if pics_src_path is not None and faces_pics_save_path is not None:
            pic_width = self.tabs_top.textline_newpic_width.text()
            if pic_width == '':
                pic_width = None
            else:
                pic_width = int(pic_width)

            pic_height = self.tabs_top.textline_newpic_height.text()
            if pic_height == '':
                pic_height = None
            else:
                pic_height = int(pic_height)
            self.extract_pictures_thread=ExtractPicFaceThread.ExtractPicFacesThread(pics_src_path,faces_pics_save_path,
                                                                                    pic_width,pic_height)
            self.extract_pictures_thread.split_finish.connect(self.extract_pictures_info)
            self.extract_pictures_thread.start()
            self.label_info.setText("正在提取图片中....")
            self.label_info.adjustSize()
        else:
            QMessageBox.information(self, '提示', '输入输出路径不能为空！')

    def extract_pictures_info(self,num):
        self.label_info.setText('一共分割了{}张图片'.format(num))
        self.label_info.adjustSize()
        if self.tabs_top.pics_extract_path:
            self.list_pictures.update(self.tabs_top.pics_extract_path)
    def predict_pictures(self):
        pics_src_path = self.tabs_top.input_pictures_path
        result_save_path = self.tabs_top.line_outresult_file_path.text()
        model_path=self.tabs_top.model_path
        if pics_src_path is not None and result_save_path is not None and model_path is not None:
            self.predict_pics_thread=PredictPicturesThread.PredictPicturesThread(pics_src_path, result_save_path, model_path)
            self.predict_pics_thread.piedict_pictures_finished.connect(self.predict_pictures_info)
            self.predict_pics_thread.start()
        else:
            QMessageBox.information(self, '提示', '输入/输出/模型/路径不能为空！')
    def predict_pictures_info(self,info):
        pics_src_path = self.tabs_top.input_pictures_path
        model_path = self.tabs_top.model_path
        files=os.listdir(pics_src_path)
        total=len(files)
        self.label_info.setText(cons_value.predict_pictures_info.format(pics_src_path,model_path,info,total))
        self.label_info.adjustSize()

    def ways_clicked(self):
        if self.tabs_top.group_ways.checkedId()==1:
            self.btn_Start.clicked.connect(self.predict_pictures)
            self.btn_Stop.setText('pictures')
        elif self.tabs_top.group_ways.checkedId()==2:
            self.btn_Start.clicked.connect(self.detect_video)
            self.btn_Stop.setText('video')
        else:
            pass
    def start_btn_changed_slot(self):
        self.btn_Start.disconnect()
        index=self.tabs_top.currentIndex()
        if index==2:
            self.btn_Start.clicked.connect(self.showPictures)
        elif index==1:
            self.btn_Start.clicked.connect(self.spilt_video)
        elif index==3:
            self.btn_Start.clicked.connect(self.extract_pictures_face)
        elif index==4:
            self.btn_Start.clicked.connect(self.predict_pictures)
        else:
            pass
        self.btn_Stop.setText(str(index))

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MainWin()
    sys.exit(app.exec_())