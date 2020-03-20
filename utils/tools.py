import cv2

def get_video_total_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frame

if __name__ == '__main__':
    print(get_video_total_frame('E:/MyCoding/TensorFlow/OpenCV/Video/data_dst.mp4'))


