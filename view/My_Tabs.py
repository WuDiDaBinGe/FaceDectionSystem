import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class MyTabs(QTabWidget):

    def __init__(self,parent=None):
        super(MyTabs, self).__init__(parent)
        self.input_pictures_path=None
        self.video_in_path=None
        self.model_path=None
        self.frame_save_path=None
        self.out_result_path=None
        self.pics_extract_path=None

        self.textline_validator=QIntValidator(0,10000)

        # 创建选项卡小控件窗口
        self.tab_input_video=QWidget()
        self.tab_input_pictures=QWidget()
        self.tab_split_videos=QWidget()
        self.tab_extract_pictures=QWidget()
        self.tab_model_select=QWidget()
        # 将选项卡添加到顶层窗口中
        self.addTab(self.tab_input_video, "输入视频")
        self.addTab(self.tab_split_videos, "分割视频")
        self.addTab(self.tab_input_pictures, "输入图片")
        self.addTab(self.tab_extract_pictures,"提取人脸")
        self.addTab(self.tab_model_select,"模型选择")
        # 每个选项卡自定义的内容
        self.Input_Video_UI()
        self.Split_Videos_UI()
        self.Input_Pictures_UI()
        self.Extract_Pictures_UI()
        self.Model_Select_UI()
        # 动作控件关联
        self.action_widget_asscion()

    def Input_Video_UI(self):
        # 表单布局
        layout=QFormLayout()
        self.btn_in_video=QPushButton('选择视频..')
        self.line_in_video_path=QLineEdit()
        self.line_in_video_path.setObjectName('no_border_lineEdit')
        self.line_in_video_path.setReadOnly(True)

        hbox_input_video = QHBoxLayout()
        hbox_input_video.addWidget(self.btn_in_video)
        hbox_input_video.setStretchFactor(self.btn_in_video, 2)
        hbox_input_video.addWidget(self.line_in_video_path)
        hbox_input_video.setStretchFactor(self.line_in_video_path, 8)

        layout.addRow('选择输入视频',hbox_input_video)

        # 设置选项卡的小标题与布局方式
        self.setTabText(0,'输入视频')
        self.tab_input_video.setLayout(layout)

    def Input_Pictures_UI(self):
        #zhu表单布局，次水平布局
        layout=QFormLayout()

        self.btn_open_pictures_file=QPushButton('打开图片文件夹..')
        self.line_picture_file_path=QLineEdit()
        self.line_picture_file_path.setObjectName('no_border_lineEdit')
        self.line_picture_file_path.setReadOnly(True)


        # 水平布局添加单选按钮
        hbox_input = QHBoxLayout()
        hbox_input.addWidget(self.btn_open_pictures_file)
        hbox_input.setStretchFactor(self.btn_open_pictures_file,2)
        hbox_input.addWidget(self.line_picture_file_path)
        hbox_input.setStretchFactor(self.line_picture_file_path, 8)

        # 表单布局添加控件
        layout.addRow(QLabel('选择图片地址'),hbox_input)

        # 设置标题与布局
        self.setTabText(2,'输入图片')
        self.tab_input_pictures.setLayout(layout)

    def Split_Videos_UI(self):
        hbox=QHBoxLayout()
        form_layout_left = QFormLayout()
        form_layout_mid = QFormLayout()
        form_layout_right = QFormLayout()

        # 第一列参数
        self.textline_start_frame=QLineEdit()
        self.textline_start_frame.setPlaceholderText('(选填)默认0')
        self.textline_start_frame.setValidator(self.textline_validator)
        self.textline_end_frame=QLineEdit()
        self.textline_end_frame.setPlaceholderText('(选填)默认总帧数')
        self.textline_end_frame.setValidator(self.textline_validator)
        self.textline_interval_frame=QLineEdit()
        self.textline_interval_frame.setPlaceholderText('(选填)默认1')
        self.textline_interval_frame.setValidator(self.textline_validator)

        form_layout_left.addRow('开始分割帧数',self.textline_start_frame)
        form_layout_left.addRow('结束分割帧数', self.textline_end_frame)
        form_layout_left.addRow('分割间隔帧数', self.textline_interval_frame)

        # 第二列参数
        self.textline_frame_width=QLineEdit()
        self.textline_frame_width.setPlaceholderText('(选填)系统自适应')
        self.textline_frame_width.setValidator(self.textline_validator)
        self.textline_frame_height=QLineEdit()
        self.textline_frame_height.setPlaceholderText('(选填)系统自适应')
        self.textline_frame_height.setValidator(self.textline_validator)

        form_layout_mid.addRow('帧宽度',self.textline_frame_width)
        form_layout_mid.addRow('帧高度', self.textline_frame_height)

        # 第三列参数
        self.btn_frame_save_path=QPushButton('选择保存路径..')
        self.line_frame_save_path=QLineEdit('还未选择')
        self.line_frame_save_path.setObjectName("no_border_lineEdit")
        self.line_frame_save_path.setReadOnly(True)

        form_layout_right.addRow('保存帧路径',self.btn_frame_save_path)
        form_layout_right.addRow('路径',self.line_frame_save_path)
        # 添加3行
        hbox.addLayout(form_layout_left)
        hbox.addStretch(1)
        hbox.addLayout(form_layout_mid)
        hbox.addStretch(1)
        hbox.addLayout(form_layout_right)
        hbox.addStretch(1)
        # 设置小标题与布局方式
        self.setTabText(1,'分割视频')
        self.tab_split_videos.setLayout(hbox)
    def Extract_Pictures_UI(self):
        # 水平布局
        layout = QHBoxLayout()
        form_layout_1=QFormLayout()

        self.textline_newpic_width=QLineEdit()
        self.textline_newpic_width.setPlaceholderText('(选填)系统自适应')
        self.textline_newpic_width.setValidator(self.textline_validator)
        self.textline_newpic_height = QLineEdit()
        self.textline_newpic_height.setPlaceholderText('(选填)系统自适应')
        self.textline_newpic_height.setValidator(self.textline_validator)

        self.btn_save_newpic_path = QPushButton('选择保存路径..')
        self.label_save_newpic_path = QLabel()

        # 水平布局添加单选按钮
        hbox_input = QHBoxLayout()
        hbox_input.addWidget(self.btn_save_newpic_path)
        hbox_input.setStretchFactor(self.btn_save_newpic_path, 2)
        hbox_input.addWidget(self.label_save_newpic_path)
        hbox_input.setStretchFactor(self.label_save_newpic_path, 8)

        form_layout_1.addRow('生成图片的宽', self.textline_newpic_width)
        form_layout_1.addRow('生成图片的高', self.textline_newpic_height)
        form_layout_1.addRow('选择保存路径', hbox_input)
        layout.addLayout(form_layout_1)
        layout.addStretch(1)

        # 设置小标题与布局方式
        self.setTabText(3, '提取人脸图片')
        self.tab_extract_pictures.setLayout(layout)

    def Model_Select_UI(self):
        # 表单布局
        layout = QFormLayout()
        self.btn_in_model = QPushButton('选择模型..')
        self.line_in_model_path = QLineEdit()
        self.line_in_model_path.setObjectName("no_border_lineEdit")
        self.line_in_model_path.setReadOnly(True)

        hbox_input_video = QHBoxLayout()
        hbox_input_video.addWidget(self.btn_in_model)
        hbox_input_video.setStretchFactor(self.btn_in_model, 2)
        hbox_input_video.addWidget(self.line_in_model_path)
        hbox_input_video.setStretchFactor(self.line_in_model_path, 8)

        self.btn_out_result_file = QPushButton('修改输出路径')
        self.line_outresult_file_path = QLineEdit()
        self.line_outresult_file_path.setObjectName('no_border_lineEdit')
        self.line_outresult_file_path.setReadOnly(True)
        hbox_out = QHBoxLayout()
        hbox_out.addWidget(self.btn_out_result_file)
        hbox_out.setStretchFactor(self.btn_out_result_file, 2)
        hbox_out.addWidget(self.line_outresult_file_path)
        hbox_out.setStretchFactor(self.line_outresult_file_path, 8)

        hbox_choice_ways=QHBoxLayout()
        self.qbutton_predict_pictures=QRadioButton('预测图片',self)
        # 默认为预测图片
        self.qbutton_predict_pictures.setChecked(True)
        self.qbutton_predict_video=QRadioButton('预测视频',self)
        hbox_choice_ways.addWidget(self.qbutton_predict_pictures)
        hbox_choice_ways.setStretchFactor(self.qbutton_predict_pictures,2)
        hbox_choice_ways.addWidget(self.qbutton_predict_video)
        hbox_choice_ways.setStretchFactor(self.qbutton_predict_video, 2)
        hbox_choice_ways.addStretch(6)

        self.group_ways=QButtonGroup()
        self.group_ways.addButton(self.qbutton_predict_pictures,1)
        self.group_ways.addButton(self.qbutton_predict_video,2)



        layout.addRow('选择模型', hbox_input_video)
        layout.addRow('选择输出路径',hbox_out)
        layout.addRow('选择预测方式',hbox_choice_ways)

        # 设置小标题与布局方式
        self.setTabText(4, '模型选择')
        self.tab_model_select.setLayout(layout)



    def action_widget_asscion(self):
        # 选择文件夹对话框
        self.btn_open_pictures_file.clicked.connect(self.open_pics_file)
        # 修改输出的预测文件对话框
        self.btn_out_result_file.clicked.connect(self.update_out_result_path)
        self.btn_in_video.clicked.connect(self.select_in_video)
        self.btn_frame_save_path.clicked.connect(self.select_frame_save_path)
        self.btn_save_newpic_path.clicked.connect(self.select_extract_pictures)
        self.btn_in_model.clicked.connect(self.select_model_path)

    def select_in_video(self):
        video_in=QFileDialog.getOpenFileName(self,'选择视频','./','*.mp4')
        self.video_in_path = video_in[0]
        if video_in[0]:
            with open(video_in[0],'r') as f:
                self.line_in_video_path.setText(f.name)

    def open_pics_file(self):
        file_path=QFileDialog.getExistingDirectory(self,'选择输入图片文件夹','/')
        self.line_picture_file_path.setText(file_path)
        if file_path==None:
            QMessageBox.information(self,'提示','文件为空，请重新选择')
        else:
            self.input_pictures_path=file_path

    def update_out_result_path(self):

        file_path = QFileDialog.getExistingDirectory(self, '选择输出文件路径', '/')
        self.line_outresult_file_path.setText(file_path)
        if file_path == None:
            QMessageBox.information(self, '提示', '文件为空，请重新选择')
        else:
            self.out_result_path = file_path

    def select_frame_save_path(self):
        save_path=QFileDialog.getExistingDirectory(self,'选择分割图片路径','/')
        self.line_frame_save_path.setText(save_path)
        if save_path==None:
            QMessageBox.information(self, '提示', '文件为空，请重新选择')
        else:
            self.frame_save_path=save_path

    def select_extract_pictures(self):
        save_path = QFileDialog.getExistingDirectory(self, '选择图片路径', '/')
        self.label_save_newpic_path.setText(save_path)
        if save_path == None:
            QMessageBox.information(self, '提示', '文件为空，请重新选择')
        else:
            self.pics_extract_path = save_path

    def select_model_path(self):
        save_path = QFileDialog.getExistingDirectory(self, '选择模型路径', '/')
        self.line_in_model_path.setText(save_path)
        if save_path == None:
            QMessageBox.information(self, '提示', '文件为空，请重新选择')
        else:
            self.model_path = save_path

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=MyTabs()
    demo.show()
    sys.exit(app.exec_())
