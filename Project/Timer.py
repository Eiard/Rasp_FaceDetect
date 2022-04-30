import time

# 计时器线程
def CountTime(delay):
    while True:
        time.sleep(delay * 60)
        global COUNTER, TOTAL, mCOUNTER, mTOTAL, inmCOUNTER, hCOUNTER, hTOTAL

        # 清空帧计数器和眨眼总数
        COUNTER = 0
        TOTAL = 0
        # 清空帧计数器和打哈欠总数
        mCOUNTER = 0
        mTOTAL = 0
        inmCOUNTER = 0
        # 清空帧计数器和点头总数
        hCOUNTER = 0
        hTOTAL = 0
