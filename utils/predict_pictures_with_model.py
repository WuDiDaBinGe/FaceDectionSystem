import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
import tensorflow as tf
import skimage.io
import skimage.transform
from models.research.deeplab.core import xception
from utils.cosnt_value import IMG_SIZE,NUM_CLASS

def load_img(path):
    print(path)
    img=skimage.io.imread(path)
    img=img/255.0
    # crop image
    short_edge=min(img.shape[:2])
    yy=int((img.shape[0]-short_edge)/2)
    xx=int((img.shape[1]-short_edge)/2)
    # 剪裁图片成正方形
    crop_image=img[yy:yy+short_edge,xx:xx+short_edge]
    resize_img= skimage.transform.resize(crop_image, (IMG_SIZE, IMG_SIZE))[None, :, :, :]

    return resize_img

def predict_with_model(path,model_path):
    tf.reset_default_graph()
    image=load_img(path)
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
            saver.restore(sess, ckpt.model_checkpoint_path)
            predict=sess.run(prediction,{x_:image})
        return predict[0]

if __name__ == '__main__':
    # E:/MyCoding/TensorFlow/FaceForensics/train_models/transfer_xception41_3.7_deepfake
    src_path='F:/dataset/FaceForensics++/Image/Deepfakes_Image/faces/'
    model_path='E:/MyCoding/TensorFlow/FaceForensics/train_models/transfer_xception41_3.7_deepfake'
    if os.path.exists(src_path):
        files=os.listdir(src_path)
        for f in files:
            path=os.path.join(src_path,f)
            predict=predict_with_model(path,model_path)
            print(predict)
    else:
        print('路径错误')






