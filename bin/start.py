# -*- coding: utf-8 -*-
# import the necessary packages

import cv2
from Device.Device import Device
from Judge import Judge
from FaceData import Face_Data

from DataExecute import face_detect
from DataExecute import face_feature_points
from Ui.UiShow import show_ui

# 设备对象
device = Device()
# 判断对象
judge = Judge()

while True:
    # 读取图片
    ret, frame = device.capture.read()
    if not ret:  # 如果没读到图片这次循环直接结束
        break

    # 从图片中读取人脸信息
    faces, gray_frame, frame = face_detect(frame, device.detector)

    # 循环脸部位置信息，使用predictor(gray, rect)获得脸部特征位置的信息
    for face in faces:
        # 获取人脸特征值
        shape = face_feature_points(face, gray_frame, device.predictor)

        # 封装脸部信息
        face_data = Face_Data(shape)

        judge.face_data = face_data

        # 判断函数
        judge.judge_all()

        cv2 = show_ui(frame, cv2, face, len(faces), face_data, judge)

    # 窗口显示 show with opencv
    cv2.imshow("Frame", frame)
    # if the `q` key was pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头 release camera
device.capture.release()
# do a bit of cleanup
device.capture.destroyAllWindows()
