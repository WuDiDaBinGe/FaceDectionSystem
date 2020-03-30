import os
accept_pictures_type=['jpg','JPG','png','PNG']

video_in_info='''视频读取完成！
视频文件名称：{}
视频文件总帧数：{}'''

split_video_info='''分割视频中...
原视频：{}
保存路径：{}    
正在分割：{}帧  目前分割了{}张     
'''
split_video_finished='''分割完成!
原视频：{}
保存路径：{}     
共分割了{}张 
'''
extract_pictures_face='''提取人脸图片中...
图片文件夹：{}
进度：{}/{}
'''
extract_pictures_finished='''提取完毕！
图片文件夹：{}
保存路径：{}
共处理{}张图片
'''
detect_video_info='''检测视频
视频路径：{}
输出文件：{}
开始检测帧数：{}  结束检测帧数：{}   
视频总帧数：{}
帧数：{}         检测结果：{}
'''
predict_pictures_info='''正在检测图片
图片路径：{}
图片名称：{}     检测结果：{}
进度：{}/{}
'''
predict_pictures_finish='''检测图片完成！
图片路径：{}
结果保存路径：{}
总共预测：{}
'''




IMG_SIZE=299
NUM_CLASS=2


