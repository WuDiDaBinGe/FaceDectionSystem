import cv2
import os
import dlib

srcvideo_path = "Video/data_dst.mp4"
dstframe_path = "video_frame_save/"
interval = 10
width = 720
height = 480


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


def video_to_frame(video_src_path, frame_save_path, interval, start_frame, end_frame,w=None,h=None):
    """
    将视频按照固定的间隔分割成图片
    :param video_src_path:  video path
    :param frame_save_path: frame path
    :param frame_width: frame width
    :param frame_height: frame height
    :param start_frame:start frame
    :param end_frame: end frame
    :param interval: interval
    :return: frame
    """
    print("正在分割视频：" + format(video_src_path))
    # 取出视频的名称
    video_name = video_src_path.split('/')[-1].split('.')[0]

    print(video_name)
    cap = cv2.VideoCapture(video_src_path)

    face_detector = dlib.get_frontal_face_detector()
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("总共的帧数为{}".format(total_frame))

    assert start_frame < total_frame - 1
    assert end_frame<=total_frame

    frame_index = 0
    frame_count = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        print("正在读取第%d帧" % frame_index)
        frame_index += 1
        if frame_index < start_frame:
            continue

        if ret and frame_index % interval == 0:

            f_height, f_width = frame.shape[:2]
            # 转化成gray
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector(gray_img, 1)
            if len(faces):
                face = faces[0]

                x, y, size = get_boundingbox(face, f_width, f_height)

                face = frame[y:y + size, x:x + size]
                if w is not None and h is not None:
                    face=cv2.resize(face,(w,h),interpolation=cv2.INTER_LINEAR)
                print(face.shape)
                # 将frame 保存到指定的路径下
                cv2.imwrite(frame_save_path + '/' + video_name + '%d.jpg' % frame_count, face)
                print(".....保存了第%d幅图片" % frame_count)
                frame_count += 1
        # 这里一定要加 要不然会一直循环下去
        if frame_index > end_frame:
            break
    cap.release()
    print("分割完毕！")
    return frame_count

def extract_faces_from_pictures(pics_path,out_path,pic_width=None,pic_height=None):
    face_detector=dlib.get_frontal_face_detector()
    files=os.listdir(pics_path)
    count=0
    for f in files:
        pic_name=f.split('.')[0]
        pic_type=f.split('.')[-1]
        if pic_type  not in ['jpg','png']:
            continue
        path=os.path.join(pics_path,f)
        picture=cv2.imread(path)
        f_height, f_width = picture.shape[:2]
        # 转化成gray
        gray_img = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
        faces = face_detector(gray_img, 1)
        if len(faces):
            face=faces[0]
            x, y, size = get_boundingbox(face, f_width, f_height)
            face=picture[y:y+size,x:x+size]
            if pic_width is not None and pic_height is not None:
                face = cv2.resize(face, (pic_width, pic_height), interpolation=cv2.INTER_LINEAR)
            print(face.shape)
            # 将frame 保存到指定的路径下
            cv2.imwrite(out_path + '/' + pic_name + '_face.jpg',face)
            count=count+1
    return count

if __name__ =='__main__':
    video_to_frame(srcvideo_path,dstframe_path,interval,50,100)

