from core.Def import Def
from core.Utils.DataExecute import total_ratio
from core.Utils.DataExecute import get_head_pose


class Face_Data(object):
    # 人脸 特征值
    shape = None

    # 左右眼 特征值
    left_eye = None
    right_eye = None

    # 内外嘴 特征值
    mouth = None
    inner_mouth = None

    # 眼 比例
    eye_ratio = None
    # 内外嘴 比例
    mouth_ratio = None
    inner_mouth_ratio = None

    # 欧拉角
    euler_angle = None
    #
    reproject_dst = None

    def __init__(self, shape):
        self.shape = shape
        self.set_eye()
        self.set_mouth()
        self.set_head()
        self.set_ratio()

    def set_eye(self):
        # 提取左眼和右眼坐标 数组array
        self.left_eye = self.shape[Def.lStart:Def.lEnd]
        self.right_eye = self.shape[Def.rStart:Def.rEnd]
        return

    def set_mouth(self):
        # 提取嘴巴外嘴唇和内嘴唇坐标  数组array
        self.mouth = self.shape[Def.mStart:Def.mEnd]
        self.inner_mouth = self.shape[Def.inmStart:Def.inmEnd]
        return

    def set_head(self):
        # 提取嘴巴外嘴唇和内嘴唇坐标  数组array
        self.mouth = self.shape[Def.mStart:Def.mEnd]
        self.inner_mouth = self.shape[Def.inmStart:Def.inmEnd]
        return

    def set_ratio(self):
        # 眼 嘴 内嘴唇 比例 (用以判断)
        self.eye_ratio, self.mouth_ratio, self.inner_mouth_ratio = total_ratio(self.left_eye, self.right_eye,
                                                                               self.mouth, self.inner_mouth)
        #       欧拉角
        self.reproject_dst, self.euler_angle = get_head_pose(self.shape)
        return
