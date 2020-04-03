import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
import matplotlib
matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view.My_Tabs import MyTabs
from view.MyPicturesList import MyPicturesListWidget
import utils.cosnt_value as cons_value
from utils import tools
from threads import SplitVideoThreads,ExtractPicFaceThread,DetectVideoThread,PredictPicturesThread



class MainWin(QMainWindow):

    def __init__(self):
        super(MainWin, self).__init__()
        self.initUI()

        self.action_widget_associate()
        # 先定义线程
        self.split_thread=SplitVideoThreads.SplitVideoThreads()
        self.predict_pics_thread=PredictPicturesThread.PredictPicturesThread()
        self.extract_pictures_thread=ExtractPicFaceThread.ExtractPicFacesThread()
        self.detect_video_thread=DetectVideoThread.DetectVideoThread()
        # 画布面板标志
        self.is_draw=False
    def initUI(self):
        # 解决无法显示中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决无法显示负号
        plt.rcParams['axes.unicode_minus'] = False
        # 顶部tab
        self.tabs_top=MyTabs(self)
        self.tabs_top.setObjectName('top_table')

        self.list_pictures=MyPicturesListWidget()
        self.list_pictures.setObjectName('list_pictures')
        # 布局信息提示区域
        frame_mid_right1=QFrame(self)
        frame_mid_right1.setFrameShape(QFrame.StyledPanel)
        frame_mid_right1.setObjectName("frame_mid_right1")

        # 信息提示区域
        self.label_info=QLabel()
        self.label_info.setObjectName("label_info")
        self.label_info.setText("提示信息区域")
        self.label_info.setAlignment(Qt.AlignTop)
        # 进度条
        self.pbar=QProgressBar()
        self.pbar.setMaximum(100)

        vbox_right1=QVBoxLayout()
        vbox_right1.addWidget(self.label_info)
        vbox_right1.setStretchFactor(self.label_info,8)
        vbox_right1.addWidget(self.pbar)
        vbox_right1.setStretchFactor(self.pbar,2)
        frame_mid_right1.setLayout(vbox_right1)
        # -----------------------------------------------
        # 布局结果展示区域
        hbox_mid_right_2 = QHBoxLayout()
        hbox_mid_right_2.setObjectName("hbox_mid_right_2")

        # 画布
        self.figure=plt.figure()
        self.ax1 = self.figure.add_subplot(211)
        self.ax1.set_title('检测结果')
        self.ax2=self.figure.add_subplot(212)
        self.ax2.set_title('检测统计')
        self.convas=FigureCanvas(self.figure)

        # 表格数据
        self.table_result=QTableWidget()
        self.table_result.setColumnCount(2)
        self.table_result.setHorizontalHeaderLabels(['检测序列','检测结果'])
        self.table_result.setObjectName("table_result")

        hbox_mid_right_result=QHBoxLayout()
        hbox_mid_right_result.addWidget(self.convas)
        hbox_mid_right_result.setStretchFactor(self.convas, 6)
        hbox_mid_right_result.addWidget(self.table_result)
        hbox_mid_right_result.setStretchFactor(self.table_result,4)
        hbox_mid_right_2.addLayout(hbox_mid_right_result)

        vbox_mid_right = QVBoxLayout(self)
        vbox_mid_right.setObjectName('vbox_mid_right')
        vbox_mid_right.addWidget(frame_mid_right1)
        vbox_mid_right.setStretchFactor(frame_mid_right1,2)
        vbox_mid_right.addLayout(hbox_mid_right_2)
        vbox_mid_right.setStretchFactor(hbox_mid_right_2, 8)

        hbox_mid=QHBoxLayout()
        hbox_mid.addWidget(self.list_pictures)
        hbox_mid.setStretchFactor(self.list_pictures,4)
        hbox_mid.addLayout(vbox_mid_right)
        hbox_mid.setStretchFactor(vbox_mid_right,6)
        # -------------------------------------------

        # 下部按钮
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

        self.setGeometry(0,0,1219,900)
        self.setWindowTitle('人脸合成图像检测系统')
        self.useQss()
        self.show()


    def action_widget_associate(self):
        self.tabs_top.line_in_video_path.textChanged.connect(self.update_info_invideo)
        self.tabs_top.currentChanged.connect(self.start_btn_changed_slot)
        self.tabs_top.group_ways.buttonClicked.connect(self.start_btn_changed_slot)
        self.btn_Stop.clicked.connect(self.StopThread)

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
        if self.pictures_file_path is not None:
            self.list_pictures.update(self.pictures_file_path)
        else:
            QMessageBox.information(self, '请检查', '输入图片路径不能为空！')

    def spilt_video(self):
        video_src_path=self.tabs_top.video_in_path
        frame_save_path=self.tabs_top.frame_save_path
        print(frame_save_path)
        if video_src_path is not None and frame_save_path is not None:
            start_frame = self.tabs_top.textline_start_frame.text()
            if start_frame=='':
                start_frame=0
            else:
                start_frame=int(start_frame)

            end_frame = self.tabs_top.textline_end_frame.text()
            total_frame=tools.get_video_total_frame(video_src_path)
            if end_frame=='':
                end_frame=total_frame
            else:
                end_frame=int(end_frame)

            interval = self.tabs_top.textline_interval_frame.text()
            if interval=='':
                interval=1
            else:
                interval=int(interval)

            if end_frame>total_frame:
                QMessageBox.information(self, '请检查', '结束帧不能大于视频的总帧数！')
                return
            elif interval>total_frame:
                QMessageBox.information(self, '请检查', '间隔帧数不能大于总帧数！')
                return
            elif start_frame>=end_frame:
                QMessageBox.information(self,'请检查','结束帧要大于开始帧')
                return

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

            self.pbar.setMaximum(end_frame-start_frame)
            self.pbar.setValue(0)
            print('线程构造')
            self.split_thread = SplitVideoThreads.SplitVideoThreads(video_src_path,frame_save_path,
                                                                    interval,start_frame,end_frame,
                                                                    frame_width,frame_height)

            self.split_thread.split_finish.connect(self.split_video_info)
            self.split_thread.all_finished.connect(self.split_video_finished)
            self.split_thread.start()
            self.label_info.setText("正在分割视频中....")
            self.label_info.adjustSize()
        else:
            QMessageBox.information(self, '请检查', '视频路径/保存帧路径不能为空！')

    def split_video_finished(self,dict):
        self.label_info.setText(cons_value.split_video_finished.format(dict['src'], dict['out'],
                                                                    dict['count']))

        self.label_info.adjustSize()
        if dict['out']:
            self.list_pictures.update(dict['out'])

    def split_video_info(self,dict):
        self.label_info.setText(cons_value.split_video_info.format(dict['src'],dict['out'],
                                                                   dict['current'],dict['count']))
        self.label_info.adjustSize()
        self.pbar.setValue(dict['step'])


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

            self.pbar.setMaximum(end_frame-start_frame)
            self.pbar.setValue(0)
            self.detect_video_thread = DetectVideoThread.DetectVideoThread(video_src_path,video_save_path,model_path,
                                                                           start_frame,end_frame)

            self.detect_video_thread.detect_video_finished.connect(self.detect_video_info)
            self.detect_video_thread.all_finished.connect(self.detect_video_finished)
            self.detect_video_thread.model_error.connect(self.model_error)
            self.detect_video_thread.start()
            self.label_info.setText('正在检测视频中......')
            self.label_info.adjustSize()
        else:
            QMessageBox.information(self, '请检查', '输入/输出视频和模型路径不能为空！')
    def detect_video_finished(self,result):
        # 表格显示结果
        frame_list=result['x']
        result_list=result['y']
        result_list=['fake' if x==0 else 'real' for x in result_list]
        row_count=np.size(result['x'])
        # 清除表格内容
        self.table_result.clearContents()
        self.table_result.setHorizontalHeaderLabels(['帧序列','检测结果'])
        self.table_result.setRowCount(row_count)
        for i in range(row_count):
            index_item=QTableWidgetItem(str(frame_list[i]))
            result_item=QTableWidgetItem(result_list[i])
            self.table_result.setItem(i,0,index_item)
            self.table_result.setItem(i,1,result_item)

        # 画图
        self.draw_video_result(result)

    def detect_video_info(self,str):
        info_dict=str
        self.label_info.setText(cons_value.detect_video_info.format(info_dict['src'],info_dict['out'],
                                                                    info_dict['start'],info_dict['end'],info_dict['total'],
                                                                    info_dict['index'],info_dict['predict']))
        self.label_info.adjustSize()
        self.pbar.setValue(info_dict['step'])

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
            self.pbar.setMaximum(tools.get_path_many_files(pics_src_path))
            self.pbar.setValue(0)
            self.extract_pictures_thread=ExtractPicFaceThread.ExtractPicFacesThread(pics_src_path,faces_pics_save_path,
                                                                                    pic_width,pic_height)
            self.extract_pictures_thread.extract_finish.connect(self.extract_pictures_info)
            self.extract_pictures_thread.all_finished.connect(self.extract_pictures_finished)
            self.extract_pictures_thread.start()
            self.label_info.setText("正在提取图片中....")
            self.label_info.adjustSize()
        else:
            QMessageBox.information(self, '请检查', '输入图片/输出图片路径不能为空！')
    def extract_pictures_finished(self,dict):
        self.label_info.setText(cons_value.extract_pictures_finished.format(dict['src'],dict['out'],dict['num']))
        if dict['out']:
            self.list_pictures.update(dict['out'])

    def extract_pictures_info(self,dict):
        self.label_info.setText(cons_value.extract_pictures_face.format(dict['src'],dict['step'],dict['total']))
        self.label_info.adjustSize()
        self.pbar.setValue(dict['step'])


    def predict_pictures(self):
        pics_src_path = self.tabs_top.input_pictures_path
        result_save_path = self.tabs_top.line_outresult_file_path.text()
        model_path=self.tabs_top.model_path
        if pics_src_path is not None and result_save_path is not None and model_path is not None:
            total = tools.get_path_many_files(pics_src_path)
            self.pbar.setMaximum(total)
            self.pbar.setValue(0)
            self.predict_pics_thread=PredictPicturesThread.PredictPicturesThread(pics_src_path, result_save_path, model_path)
            self.predict_pics_thread.piedict_pictures_finished.connect(self.predict_pictures_info)
            self.predict_pics_thread.all_finished.connect(self.predict_pictures_finish)
            self.predict_pics_thread.model_error.connect(self.model_error)
            self.predict_pics_thread.start()
            self.label_info.setText('正在预测图片中......')

        else:
            QMessageBox.information(self, '请检查', '输入图片/输出预测结果文件/模型路径不能为空！')

    def predict_pictures_finish(self,info,result):

        pics_src_path = self.tabs_top.input_pictures_path
        info_dict=info
        self.label_info.setText(cons_value.predict_pictures_finish.format(pics_src_path,info_dict['out'],info_dict['num']))
        self.label_info.adjustSize()
        # 画图
        self.draw_pictures_result(result)
        # 显示表格结果
        # 清除表格内容
        self.table_result.clearContents()
        fname_list = result['f_name']
        result_list = result['labels']
        row_count = np.size(result['x'])
        self.table_result.setHorizontalHeaderLabels(['文件名','结果'])
        self.table_result.setRowCount(row_count)
        for i in range(row_count):
            index_item = QTableWidgetItem(fname_list[i])
            result_item = QTableWidgetItem(result_list[i])
            self.table_result.setItem(i, 0, index_item)
            self.table_result.setItem(i, 1, result_item)

    def predict_pictures_info(self,info):
        pics_src_path = self.tabs_top.input_pictures_path
        info_dict=info
        total=tools.get_path_many_files(pics_src_path)
        self.label_info.setText(cons_value.predict_pictures_info.format(pics_src_path,info_dict['fname'],info_dict['label'],info_dict['num'],total))
        self.label_info.adjustSize()
        self.pbar.setValue(info_dict['num'])

    def ways_clicked(self):
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
        elif index==4 and self.tabs_top.group_ways.checkedId()==1:
            self.btn_Start.clicked.connect(self.predict_pictures)
        elif index==4 and self.tabs_top.group_ways.checkedId()==2:
            self.btn_Start.clicked.connect(self.detect_video)
        else:
            self.btn_Start.clicked.connect(self.update_info_invideo)
    def StopThread(self):
        msg = QMessageBox.question(self, "警告", "你确定停止任务吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # 判断消息的返回值
        if msg == QMessageBox.Yes:
            self.pbar.setValue(0)
            if self.detect_video_thread.isRunning():
                print(1)
                self.detect_video_thread.quit_()
            if self.extract_pictures_thread.isRunning():
                print(2)
                self.extract_pictures_thread.quit_()
            if self.predict_pics_thread.isRunning():
                print(3)
                self.predict_pics_thread.quit_()
            if self.split_thread.isRunning():
                print(4)
                self.split_thread.quit_()
            self.label_info.setText('停止了所有进程！')
            self.label_info.adjustSize()
        else:
            pass
    def model_error(self):
        QMessageBox.information(self, '请检查', '模型出错！')
    def draw_video_result(self,result):
        if self.is_draw:
            self.reset_draw()
        self.ax1.scatter(result['x'], result['y'])
        names = ['fake', 'real']
        values = [result['fake_num'], result['real_num']]
        a=self.ax2.bar(names, values)
        self.autolabel(a)
        self.convas.draw()
        self.is_draw=True

    def draw_pictures_result(self,result):
        if self.is_draw:
            self.reset_draw()
        self.ax1.scatter(result['x'], result['y'])
        names = ['fake', 'real']
        values = [result['fake_num'], result['real_num']]
        a=self.ax2.bar(names, values)
        self.autolabel(a)
        self.convas.draw()
        self.is_draw = True

    # 定义函数来显示柱状上的数值
    def autolabel(self,rects):
        for rect in rects:
            height = rect.get_height()
            self.ax2.text(rect.get_x() + rect.get_width() / 2.-0.1, 1.03 * height, '%s' % float(height))


    def reset_draw(self):
        try:
            self.ax1.cla()
            self.ax1.set_title('检测结果')
            self.ax2.cla()
            self.ax2.set_title('检测统计')
            self.convas.draw()
            self.is_draw=False
        except Exception as e:
            print(e)

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MainWin()
    sys.exit(app.exec_())