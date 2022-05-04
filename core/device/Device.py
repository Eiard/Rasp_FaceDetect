import dlib
import cv2


class Device(object):
    # 获取摄像头
    capture = None
    # 人脸检测器
    detector = None
    # 特征值提取器
    predictor = None

    def __init__(self):
        # 初始化 detector(脸部位置检测器) predictor(脸部特征位置检测器) cap(本地摄像头)
        print("[INFO] loading facial landmark predictor...")
        self.set_capture()
        self.set_detector()
        self.set_predictor()

    def set_capture(self):
        # 打开cv2 本地摄像头
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def set_detector(self):
        # 使用dlib.get_frontal_face_detector() 获得脸部位置检测器
        self.detector = dlib.get_frontal_face_detector()

    def set_predictor(self):
        # 使用dlib.shape_predictor获得脸部特征位置检测器
        self.predictor = dlib.shape_predictor("../Landmarks/shape_predictor_68_face_landmarks.dat")
