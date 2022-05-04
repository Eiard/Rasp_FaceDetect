from core.Def import Def


class Judge(object):
    # 人脸相关数据
    face_data = None

    # 初始化帧计数器和眨眼总数
    COUNTER = 0
    TOTAL = 0

    # 初始化帧计数器和打哈欠总数
    mCOUNTER = 0
    inmCOUNTER = 0
    mTOTAL = 0

    # 初始化帧计数器和点头总数
    hCOUNTER = 0
    hTOTAL = 0

    def set_face_data(self, face_data):
        self.face_data = face_data
        return

    def judge_eye_ratio(self):
        """
            逐帧判断(一张图片)
                判断是否满足阈值(COUNTER 连续满足的次数)
                    如果连续多张图片都是闭眼状态 (说明已经犯困睡眠)
                        眨眼次数猛增
        """
        if self.face_data.eye_ratio < Def.EYE_AR_THRESH:  # 眼睛长宽比：
            self.COUNTER += 1
            if self.COUNTER >= Def.SLEEP_EYE_AR_CON_SEC_FRAMES:  # 阈值：
                self.TOTAL += Def.SLEEP_EYE_INC
                self.COUNTER = 0
            elif self.COUNTER >= Def.EYE_AR_THRESH:  # 阈值：
                self.TOTAL += Def.EYE_INC
        else:
            # 重置眼帧计数器
            self.COUNTER = 0
        return

    def judge_mouth_ratio(self):
        """
            计算张嘴评分，如果小于阈值，则加1，
                如果连续3次都小于阈值，则表示打了一次哈欠，同一次哈欠大约在3帧
        """
        if self.face_data.mouth_ratio > Def.MOUTH_AR_THRESH:  # 张嘴阈值
            if self.face_data.inner_mouth_ratio > Def.INNER_MOUTH_AR_THRESH:  # 内部张嘴阈值
                self.mCOUNTER += 1
        else:
            # 如果连续2次都小于阈值，则表示打了一次哈欠
            if self.mCOUNTER >= Def.NOD_AR_CON_SEC_FRAMES:  # 阈值：
                self.mTOTAL += 1
            # 重置嘴帧计数器
            self.mCOUNTER = 0
        return

    def judge_nod_ratio(self):
        """
            瞌睡点头
                判断
        """
        # 取pitch旋转角度
        if self.face_data.euler_angle[0, 0] > Def.HEAD_AR_THRESH:  # 点头阈值
            self.hCOUNTER += 1
        else:
            # 如果连续2次都小于阈值，则表示瞌睡点头一次
            if self.hCOUNTER >= Def.NOD_AR_CON_SEC_FRAMES:  # 阈值：2
                self.hTOTAL += 1
            # 重置点头帧计数器
            self.hCOUNTER = 0
        return

    def judge_fatigue(self):
        # 确定疲劳提示:眨眼50次，打哈欠15次，瞌睡点头15次
        if self.TOTAL >= 50 or self.mTOTAL >= 15 or self.hTOTAL >= 15:
            print("疲劳了 !!!")
        return

    def print_console(self):
        print('嘴巴实时长宽比:{:.2f} '.format(self.face_data.mouth_ratio) + "\t是否张嘴：" + str(
            [False, True][self.face_data.mouth_ratio > Def.MOUTH_AR_THRESH]))
        print('眼睛实时长宽比:{:.2f} '.format(self.face_data.eye_ratio) + "\t是否眨眼：" + str([False, True][Judge.COUNTER >= 1]))
        print('内嘴巴实时长宽比:{:.2f} '.format(self.face_data.inner_mouth_ratio) + "\t是否张嘴：" + str(
            [False, True][self.face_data.inner_mouth_ratio > Def.INNER_MOUTH_AR_THRESH]))

        return

    def judge_all(self):
        self.judge_eye_ratio()
        self.judge_mouth_ratio()
        self.judge_nod_ratio()
        self.judge_fatigue()
        self.print_console()
        return
