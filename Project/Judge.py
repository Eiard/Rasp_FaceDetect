import Def

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


def judge_eye_ratio(eye_ratio):
    """
        逐帧判断(一张图片)
            判断是否满足阈值(COUNTER 连续满足的次数)
                如果连续多张图片都是闭眼状态 (说明已经犯困睡眠)
                    眨眼次数猛增
    """
    global COUNTER, TOTAL
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
    return


def judge_mouth_ratio(mouth_ratio, inner_mouth_ratio):
    """
        计算张嘴评分，如果小于阈值，则加1，
            如果连续3次都小于阈值，则表示打了一次哈欠，同一次哈欠大约在3帧
    """
    global mCOUNTER, mTOTAL
    if mouth_ratio > Def.MOUTH_AR_THRESH:  # 张嘴阈值
        if inner_mouth_ratio > Def.INNER_MOUTH_AR_THRESH:  # 内部张嘴阈值
            mCOUNTER += 1
    else:
        # 如果连续2次都小于阈值，则表示打了一次哈欠
        if mCOUNTER >= Def.NOD_AR_CON_SEC_FRAMES:  # 阈值：
            mTOTAL += 1
        # 重置嘴帧计数器
        mCOUNTER = 0
    return


def judge_nod_ratio(reprojectdst, euler_angle):
    """
        瞌睡点头
            判断
    """
    global hTOTAL, hCOUNTER
    har = euler_angle[0, 0]  # 取pitch旋转角度
    if har > Def.HEAD_AR_THRESH:  # 点头阈值
        hCOUNTER += 1
    else:
        # 如果连续2次都小于阈值，则表示瞌睡点头一次
        if hCOUNTER >= Def.NOD_AR_CON_SEC_FRAMES:  # 阈值：2
            hTOTAL += 1
        # 重置点头帧计数器
        hCOUNTER = 0
    return
