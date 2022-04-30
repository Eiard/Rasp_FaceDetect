import dlib
import cv2

def init():
    # 初始化DLIB的人脸检测器（HOG），然后创建面部标志物预测
    print("[INFO] loading facial landmark predictor...")

    # 使用dlib.get_frontal_face_detector() 获得脸部位置检测器
    detector = dlib.get_frontal_face_detector()
    # 使用dlib.shape_predictor获得脸部特征位置检测器
    predictor = dlib.shape_predictor("../Landmarks/shape_predictor_68_face_landmarks.dat")

    # 打开cv2 本地摄像头
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    return detector, predictor, cap
