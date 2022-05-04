
def show_all_face_feature_points(frame, shape, cv2):
    for (x, y) in shape:
        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
    return


def show_face(face, frame, cv2):
    left = face.left()
    top = face.top()
    right = face.right()
    bottom = face.bottom()
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
    return


def show_drawContours(face_data, frame, cv2):
    leftEyeHull = cv2.convexHull(face_data.left_eye)
    rightEyeHull = cv2.convexHull(face_data.right_eye)
    cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
    cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
    mouthHull = cv2.convexHull(face_data.mouth)
    cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
    inner_mouthHull = cv2.convexHull(face_data.inner_mouth)
    cv2.drawContours(frame, [inner_mouthHull], -1, (0, 255, 0), 1)
    return


def put_text(face_data, len_face, frame, cv2, judge):
    cv2.putText(frame, "Faces: {}".format(len_face), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "COUNTER: {}".format(judge.COUNTER), (150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 0, 255), 2)
    cv2.putText(frame, "EAR: {:.2f}".format(face_data.eye_ratio), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "Blinks: {}".format(judge.TOTAL), (450, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (255, 255, 0), 2)

    cv2.putText(frame, "mCOUNTER: {}".format(judge.mCOUNTER), (150, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 0, 255), 2)
    cv2.putText(frame, "MAR: {:.2f}".format(face_data.mouth_ratio), (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "Yawning: {}".format(judge.mTOTAL), (450, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (255, 255, 0), 2)

    # 按q退出
    cv2.putText(frame, "Press 'q': Quit", (20, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (84, 255, 159), 2)

    return


def show_angle_results(euler_angle, frame, cv2, judge):
    cv2.putText(frame, "X: " + "{:7.2f}".format(euler_angle[0, 0]), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                (0, 255, 0), thickness=2)  # GREEN
    cv2.putText(frame, "Y: " + "{:7.2f}".format(euler_angle[1, 0]), (150, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                (255, 0, 0), thickness=2)  # BLUE
    cv2.putText(frame, "Z: " + "{:7.2f}".format(euler_angle[2, 0]), (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                (0, 0, 255), thickness=2)  # RED
    cv2.putText(frame, "Nod: {}".format(judge.hTOTAL), (450, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0),
                2)


def show_ui(frame, cv2, face, len_face, face_data, judge):
    # 使用cv2.convexHull获得凸包位置，使用drawContours画出轮廓位置进行画图操作
    # 绘制左眼和右眼
    show_drawContours(face_data, frame, cv2)

    # 进行画图操作，用矩形框标注人脸
    show_face(face, frame, cv2)

    # 进行画图操作，同时使用cv2.putText将眨眼次数进行显示
    put_text(face_data, len_face, frame, cv2, judge)

    # 显示角度结果
    show_angle_results(face_data.euler_angle, frame, cv2, judge)

    # 显示所有特征点
    show_all_face_feature_points(frame, face_data.shape, cv2)

    return cv2
