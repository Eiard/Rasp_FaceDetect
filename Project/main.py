# -*- coding: utf-8 -*-
# import the necessary packages
import cv2
import imutils
import __init__
import Def
import DataExecute
from imutils import face_utils

# 初始化帧计数器和眨眼总数
COUNTER = 0
TOTAL = 0

# 初始化帧计数器和打哈欠总数
mCOUNTER = 0
mTOTAL = 0
inmCOUNTER = 0

# 初始化帧计数器和点头总数
hCOUNTER = 0
hTOTAL = 0

# 初始化 detector(脸部位置检测器) predictor(脸部特征位置检测器) cap(本地摄像头)
detector, predictor, cap = __init__.init()

while True:
    # 读取图片
    ret, frame = cap.read()
    # 图片做维度扩大
    frame = imutils.resize(frame, width=720)
    # 灰度处理
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 使用detector(gray, 0) 进行脸部位置检测 检测到多张脸
    faces = detector(gray, 0)

    # 循环脸部位置信息，使用predictor(gray, rect)获得脸部特征位置的信息
    for face in faces:
        # 获取人脸的特征点对象
        shape = predictor(gray, face)

        # 将脸部特征信息转换为数组array的格式
        shape = face_utils.shape_to_np(shape)

        # 提取左眼和右眼坐标 数组array
        leftEye = shape[Def.lStart:Def.lEnd]
        rightEye = shape[Def.rStart:Def.rEnd]
        # 提取嘴巴外嘴唇和内嘴唇坐标  数组array
        mouth = shape[Def.mStart:Def.mEnd]
        inMouth = shape[Def.inmStart:Def.inmEnd]

        # 构造函数计算左右眼的EAR值，使用平均值作为最终的EAR
        eye_ratio = DataExecute.average_eyes_ratio(leftEye, rightEye)

        # 内嘴唇比 与 外嘴唇比
        mouth_ratio = DataExecute.mouth_aspect_ratio(mouth)
        inner_mouth_ratio = DataExecute.inner_mouth_aspect_ratio(inMouth)

        # 第十一步：使用cv2.convexHull获得凸包位置，使用drawContours画出轮廓位置进行画图操作  绘制左眼和右眼
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
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

        '''
            逐帧判断(一张图片)
                判断是否满足阈值(COUNTER 连续满足的次数)
                    如果连续多张图片都是闭眼状态 (说明已经犯困睡眠)
                        眨眼次数猛增
                    
                
        '''
        if eye_ratio < Def.EYE_AR_THRESH:  # 眼睛长宽比：
            COUNTER += 1

            if COUNTER >= Def.SLEEP_EYE_AR_CON_SEC_FRAMES:  # 阈值：
                TOTAL += Def.SLEEP_EYE_INC
                COUNTER = 0

            elif COUNTER >= Def.EYE_AR_THRESH:  # 阈值：
                TOTAL += Def.EYE_INC

        else:
            # 重置眼帧计数器
            COUNTER = 0

        # 第十四步：进行画图操作，同时使用cv2.putText将眨眼次数进行显示
        cv2.putText(frame, "Faces: {}".format(len(faces)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "COUNTER: {}".format(COUNTER), (150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(eye_ratio), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Blinks: {}".format(TOTAL), (450, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        '''
            计算张嘴评分，如果小于阈值，则加1，如果连续3次都小于阈值，则表示打了一次哈欠，同一次哈欠大约在3帧
        '''

        # 同理，判断是否打哈欠
        if mouth_ratio > Def.MOUTH_AR_THRESH:  # 张嘴阈值
            if inner_mouth_ratio > Def.INNER_MOUTH_AR_THRESH:  # 内部张嘴阈值
                mCOUNTER += 1
        else:
            # 如果连续2次都小于阈值，则表示打了一次哈欠
            if mCOUNTER >= Def.NOD_AR_CON_SEC_FRAMES:  # 阈值：
                mTOTAL += 1
            # 重置嘴帧计数器
            mCOUNTER = 0

        cv2.putText(frame, "mCOUNTER: {}".format(mCOUNTER), (150, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "MAR: {:.2f}".format(mouth_ratio), (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Yawning: {}".format(mTOTAL), (450, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        """
        瞌睡点头
        """
        # 第十五步：获取头部姿态
        reprojectdst, euler_angle = DataExecute.get_head_pose(shape)

        har = euler_angle[0, 0]  # 取pitch旋转角度
        if har > Def.HEAD_AR_THRESH:  # 点头阈值
            hCOUNTER += 1
        else:
            # 如果连续2次都小于阈值，则表示瞌睡点头一次
            if hCOUNTER >= Def.NOD_AR_CON_SEC_FRAMES:  # 阈值：2
                hTOTAL += 1
            # 重置点头帧计数器
            hCOUNTER = 0

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
