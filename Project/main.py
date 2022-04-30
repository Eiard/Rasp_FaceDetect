# -*- coding: utf-8 -*-
# import the necessary packages
import cv2
import Def
from __init__ import init
from DataExecute import face_detect
from DataExecute import face_feature_points
from DataExecute import total_ratio
from DataExecute import get_head_pose
from Judge import judge_eye_ratio
from Judge import judge_mouth_ratio
from Judge import judge_nod_ratio

# 初始化 detector(脸部位置检测器) predictor(脸部特征位置检测器) cap(本地摄像头)
detector, predictor, cap = init()

while True:
    # 读取图片
    ret, frame = cap.read()
    if not ret:  # 如果没读到图片这次循环直接结束
        break

    # 从图片中读取人脸信息
    faces, gray_frame, frame = face_detect(frame, detector)

    # 循环脸部位置信息，使用predictor(gray, rect)获得脸部特征位置的信息
    for face in faces:
        shape = face_feature_points(face, gray_frame, predictor)

        # 提取左眼和右眼坐标 数组array
        left_eye = shape[Def.lStart:Def.lEnd]
        right_eye = shape[Def.rStart:Def.rEnd]
        # 提取嘴巴外嘴唇和内嘴唇坐标  数组array
        mouth = shape[Def.mStart:Def.mEnd]
        inner_Mouth = shape[Def.inmStart:Def.inmEnd]

        # 眼 嘴 内嘴唇 比例 (用以判断)
        eye_ratio, mouth_ratio, inner_mouth_ratio = total_ratio(left_eye, right_eye, mouth, inner_Mouth)
        #
        reprojectdst, euler_angle = get_head_pose(shape)

        # 判断眼
        judge_eye_ratio(eye_ratio)
        # 判断嘴
        judge_mouth_ratio(mouth_ratio, inner_mouth_ratio)
        # 判断点头
        judge_nod_ratio(reprojectdst, euler_angle)

        # 第十一步：使用cv2.convexHull获得凸包位置，使用drawContours画出轮廓位置进行画图操作  绘制左眼和右眼
        leftEyeHull = cv2.convexHull(left_eye)
        rightEyeHull = cv2.convexHull(right_eye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        mouthHull = cv2.convexHull(mouth)
        cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

        # 第十二步：进行画图操作，用矩形框标注人脸
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)

        # 第十四步：进行画图操作，同时使用cv2.putText将眨眼次数进行显示
        cv2.putText(frame, "Faces: {}".format(len(faces)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "COUNTER: {}".format(COUNTER), (150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(eye_ratio), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Blinks: {}".format(TOTAL), (450, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.putText(frame, "mCOUNTER: {}".format(mCOUNTER), (150, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "MAR: {:.2f}".format(mouth_ratio), (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Yawning: {}".format(mTOTAL), (450, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # 绘制正方体12轴
        # for start, end in line_pairs:
        #    cv2.line(frame, reprojectdst[start], reprojectdst[end], (0, 0, 255))
        # 显示角度结果
        cv2.putText(frame, "X: " + "{:7.2f}".format(euler_angle[0, 0]), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (0, 255, 0), thickness=2)  # GREEN
        cv2.putText(frame, "Y: " + "{:7.2f}".format(euler_angle[1, 0]), (150, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (255, 0, 0), thickness=2)  # BLUE
        cv2.putText(frame, "Z: " + "{:7.2f}".format(euler_angle[2, 0]), (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (0, 0, 255), thickness=2)  # RED
        cv2.putText(frame, "Nod: {}".format(hTOTAL), (450, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # 第十六步：进行画图操作，68个特征点标识
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        print('嘴巴实时长宽比:{:.2f} '.format(mouth_ratio) + "\t是否张嘴：" + str([False, True][mouth_ratio > Def.MOUTH_AR_THRESH]))
        print('眼睛实时长宽比:{:.2f} '.format(eye_ratio) + "\t是否眨眼：" + str([False, True][COUNTER >= 1]))
        print('内嘴巴实时长宽比:{:.2f} '.format(inner_mouth_ratio) + "\t是否张嘴：" + str(
            [False, True][inner_mouth_ratio > Def.INNER_MOUTH_AR_THRESH]))

    # 确定疲劳提示:眨眼50次，打哈欠15次，瞌睡点头15次
    if TOTAL >= 50 or mTOTAL >= 15 or hTOTAL >= 15:
        cv2.putText(frame, "SLEEP!!!", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

    # 按q退出
    cv2.putText(frame, "Press 'q': Quit", (20, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (84, 255, 159), 2)

    # 窗口显示 show with opencv
    cv2.imshow("Frame", frame)

    # if the `q` key was pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头 release camera
cap.release()
# do a bit of cleanup
cv2.destroyAllWindows()
