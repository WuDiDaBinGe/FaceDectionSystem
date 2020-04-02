import cv2
import skimage.io
import skimage.transform
from utils import cosnt_value
import numpy as np
import os
def get_split_video_total(startframe,endframe,interval):
    endframe=endframe-startframe
    return endframe//interval+1
def get_video_total_frame(video_path):
    '''
    得到视频一共有多少帧
    :param video_path:
    :return:
    '''
    cap = cv2.VideoCapture(video_path)
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frame
def get_path_many_files(path):
    '''
    得到path文件夹下有多少文件
    :param path:
    :return:
    '''
    if os.path.exists(path):
        files=os.listdir(path)
        return len(files)
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
    '''
    将图片处理成模型需要的格式大小并归一化
    :param image:
    :return:
    '''
    # Revert from BGR
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 转换成需要处理的格式
    image = cv2.resize(image, (cosnt_value.IMG_SIZE, cosnt_value.IMG_SIZE), interpolation=cv2.INTER_LINEAR)

    image = np.expand_dims(image, 0)
    image = image / 255.0
    print(image.shape)
    return image
def load_img(path):
    print(path)
    img = skimage.io.imread(path)
    img = img / 255.0
    # crop image
    short_edge = min(img.shape[:2])
    yy = int((img.shape[0] - short_edge) / 2)
    xx = int((img.shape[1] - short_edge) / 2)
    # 剪裁图片成正方形
    crop_image = img[yy:yy + short_edge, xx:xx + short_edge]
    resize_img = skimage.transform.resize(crop_image, (cosnt_value.IMG_SIZE, cosnt_value.IMG_SIZE))[None, :, :, :]
    return resize_img


if __name__ == '__main__':
    print(get_split_video_total(4,20,3))


