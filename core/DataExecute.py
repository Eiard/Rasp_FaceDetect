# -*- coding: utf-8 -*-
# import the necessary packages
import numpy as np  # 数据处理的库 numpy
from scipy.spatial import distance as dist
import cv2
import math
from Def import Def
import imutils
from imutils import face_utils

def face_detect(frame, detector):  # 灰度处理并且读取人脸信息
    # 图片做维度扩大
    frame = imutils.resize(frame, width = 1080)
    # 灰度处理
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 使用detector(gray_frame, 0) 进行脸部位置检测 检测到多张脸
    faces = detector(gray_frame, 0)
    return faces, gray_frame, frame  # 返回人脸信息


def face_feature_points(face, gray_frame, predictor):
    # 获取人脸的特征点对象
    shape = predictor(gray_frame, face)
    # 将脸部特征信息转换为数组array的格式
    shape = face_utils.shape_to_np(shape)
    return shape  # 数组array


def get_head_pose(shape):  # 头部姿态估计
    # （像素坐标集合）填写2D参考点，注释遵循https://ibug.doc.ic.ac.uk/resources/300-W/
    # 17左眉左上角/21左眉右角/22右眉左上角/26右眉右上角/36左眼左上角/39左眼右上角/42右眼左上角/
    # 45右眼右上角/31鼻子左上角/35鼻子右上角/48左上角/54嘴右上角/57嘴中央下角/8下巴角
    image_pts = np.float32([shape[17], shape[21], shape[22], shape[26], shape[36],
                            shape[39], shape[42], shape[45], shape[31], shape[35],
                            shape[48], shape[54], shape[57], shape[8]])
    # solvePnP计算姿势——求解旋转和平移矩阵：
    # rotation_vec表示旋转矩阵，translation_vec表示平移矩阵，cam_matrix与K矩阵对应，dist_coeffs与D矩阵对应。
    _, rotation_vec, translation_vec = cv2.solvePnP(Def.object_pts, image_pts, Def.cam_matrix, Def.dist_coeffs)
    # projectPoints重新投影误差：原2d点和重投影2d点的距离（输入3d点、相机内参、相机畸变、r、t，输出重投影2d点）
    reprojectdst, _ = cv2.projectPoints(Def.reprojectsrc, rotation_vec, translation_vec, Def.cam_matrix,
                                        Def.dist_coeffs)
    reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))  # 以8行2列显示

    # 计算欧拉角calc euler angle
    # 参考https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#decomposeprojectionmatrix
    rotation_mat, _ = cv2.Rodrigues(rotation_vec)  # 罗德里格斯公式（将旋转矩阵转换为旋转向量）
    pose_mat = cv2.hconcat((rotation_mat, translation_vec))  # 水平拼接，vconcat垂直拼接
    # decomposeProjectionMatrix将投影矩阵分解为旋转矩阵和相机矩阵
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)

    pitch, yaw, roll = [math.radians(_) for _ in euler_angle]

    pitch = math.degrees(math.asin(math.sin(pitch)))
    roll = -math.degrees(math.asin(math.sin(roll)))
    yaw = math.degrees(math.asin(math.sin(yaw)))
    print('pitch:{}, yaw:{}, roll:{}'.format(pitch, yaw, roll))

    return reprojectdst, euler_angle  # 投影误差，欧拉角


def eye_aspect_ratio(eye):
    #   Eye
    #   1  2
    # 0      3
    #   5  6

    # 垂直眼标志（X，Y）坐标
    A = dist.euclidean(eye[1], eye[5])  # 计算两个集合之间的欧式距离
    B = dist.euclidean(eye[2], eye[4])
    # 计算水平之间的欧几里得距离
    # 水平眼标志（X，Y）坐标
    C = dist.euclidean(eye[0], eye[3])
    # 眼睛长宽比的计算
    eye_ratio = (A + B) / (2.0 * C)
    # 返回眼睛的长宽比
    return eye_ratio


def mouth_aspect_ratio(mouth):  # 嘴部
    #                51  52  53
    #           50  62 63  64 65  54
    #        49  61

    A = np.linalg.norm(mouth[2] - mouth[9])  # 51, 59
    B = np.linalg.norm(mouth[3] - mouth[8])  # 52, 58
    C = np.linalg.norm(mouth[4] - mouth[7])  # 53, 57
    D = np.linalg.norm(mouth[0] - mouth[6])  # 49, 55
    # 外嘴唇长宽比的计算
    mouth_ratio = (A + B + C) / (3.0 * D)
    # 返回外嘴唇的长宽比
    return mouth_ratio


def inner_mouth_aspect_ratio(inner_mouth):  # 内部嘴部

    A = np.linalg.norm(inner_mouth[1] - inner_mouth[7])  # 62, 68
    B = np.linalg.norm(inner_mouth[2] - inner_mouth[6])  # 63, 67
    C = np.linalg.norm(inner_mouth[3] - inner_mouth[5])  # 64, 66
    D = np.linalg.norm(inner_mouth[0] - inner_mouth[4])  # 61, 65
    # 内嘴唇长宽比的计算
    inner_mouth_ratio = (A + B + C) / (3.0 * D)
    return inner_mouth_ratio


def average_eyes_ratio(left_eye, right_eye):
    leftEAR = eye_aspect_ratio(left_eye)
    rightEAR = eye_aspect_ratio(right_eye)
    return (leftEAR + rightEAR) / 2.0


def total_ratio(left_eye, right_eye, mouth, inner_mouth):
    eye_ratio = average_eyes_ratio(left_eye, right_eye)
    mouth_ratio = mouth_aspect_ratio(mouth)
    inner_mouth_ratio = inner_mouth_aspect_ratio(inner_mouth)
    return eye_ratio, mouth_ratio, inner_mouth_ratio
