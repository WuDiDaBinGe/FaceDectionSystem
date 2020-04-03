import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
import numpy as np
from models.research.deeplab.core import xception
from utils.cosnt_value import IMG_SIZE,NUM_CLASS
import tensorflow as tf
import cv2
import dlib

VIDEO_PATH='F:/dataset/FaceForensics++/video_txt/49.mp4'
VIDEO_OUT_PATH='F:/dataset/'
MODEL_PATH='E:/MyCoding/TensorFlow/FaceForensics/train_models/transfer_xception41_3.7_deepfake'



def get_boundingbox(face, width, height, scale=1.3, minsize=None):
    """
    Expects a dlib face to generate a quadratic bounding box.
    期望dlib面生成二次边界框。
    重新生成dlib面的边界框（scale决定边界框的大小）
    :param face: dlib face class
    :param width: frame width      视频帧图片的宽
    :param height: frame height    视频帧图片的高
    :param scale: bounding box size multiplier to get a bigger face region  扩大的倍数
    :param minsize: set minimum bounding box size
    :return: x, y, bounding_box_size in opencv form  返回x，y为新的边界框的坐标，size__bb为边界框的边长
    """
    x1 = face.left()
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()
    size_bb = int(max(x2 - x1, y2 - y1) * scale)
    if minsize:
        if size_bb < minsize:
            size_bb = minsize
    center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

    # Check for out of bounds, x-y top left corner
    # 判断中心点到边界的距离是否>size_bb/2 .若小于则x1，y1为0
    x1 = max(int(center_x - size_bb // 2), 0)
    y1 = max(int(center_y - size_bb // 2), 0)

    # Check for too big bb size for given x, y
    size_bb = min(width - x1, size_bb)
    size_bb = min(height - y1, size_bb)
    return x1, y1, size_bb

def process_pictures(image):
    # Revert from BGR
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 转换成需要处理的格式
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)

    image =np.expand_dims(image,0)
    image=image/255.0
    print(image.shape)
    return image

def predict_with_model(image,model_path):
    tf.reset_default_graph()
    image=process_pictures(image)

    x_ = tf.placeholder(tf.float32, [None, IMG_SIZE, IMG_SIZE, 3])

    with tf.contrib.slim.arg_scope(xception.xception_arg_scope()):
        net, end_point = xception.xception_41(x_, NUM_CLASS, is_training=False)

    logits=tf.reshape(net,(-1,2))
    prediction=tf.argmax(tf.nn.softmax(logits),1)

    saver=tf.train.Saver()

    with tf.Session() as sess:
        init_op = tf.group(tf.global_variables_initializer())
        sess.run(init_op)
        ckpt = tf.train.get_checkpoint_state(model_path)
        if ckpt and ckpt.model_checkpoint_path:
            print(ckpt.model_checkpoint_path)
            saver.restore(sess, ckpt.model_checkpoint_path)
            predict=sess.run(prediction,{x_:image})
            print(predict[0])

        return predict[0]

def detect_from_video(video_src_path, out_video_path, model_path, start_frame, end_frame):
    """
    将视频按照固定的间隔分割成图片
    :param video_src_path:  video path
    :param out_video_path: frame path
    :param start_frame:start frame
    :param end_frame: end frame
    :return: frame
    """
    print("正在分割视频：" + format(video_src_path))
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
    assert end_frame<=total_frame
    print("xnsanx2")
    frame_index = 0
    endpoints={}
    while (cap.isOpened()):
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

                x, y, size = get_boundingbox(face, f_width, f_height)
                # face 为人脸二次区域
                cropped_face = frame[y:y + size, x:x + size]
                # 预测
                predict=predict_with_model(cropped_face,model_path)
                endpoints[frame_index]=predict
                # -----------------------------------------------
                # Text
                x = face.left()
                y = face.top()
                w = face.right() - x
                h = face.bottom() - y

                label='real' if predict==1 else 'fake'
                color = (0, 0, 255) if predict == 0 else (0, 255, 0)
                # 图片中加上文字
                cv2.putText(frame,  label, (x, y + h + 30),
                            font_face, font_scale,
                            color, thickness, 2)
                # draw box over face
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            writer.write(frame)
        # 这里一定要加,要不然会一直循环下去
        if frame_index > end_frame:
            break

    print("分割完毕！")
    cap.release()
    if writer is not None:
        writer.release()
        print('Finished! Output saved under {}'.format(out_video_path))
    else:
        print('Input video file was empty')
    return endpoints
if __name__ == '__main__':
    end=detect_from_video(VIDEO_PATH,VIDEO_OUT_PATH,MODEL_PATH,0,10)
    print(str(end))

