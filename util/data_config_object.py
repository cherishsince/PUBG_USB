"""

解析后存储的对象


"""
import datetime
import json


class DateEnconding(json.JSONEncoder):
    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


class Data:
    # 左右修正
    left_right_correction = None
    # 武器名字
    name = None
    # 设计速度
    speed = None
    # 枪口
    muzzle = []
    # 握把
    grip = []
    # 弹夹
    clip = []
    # 屁股
    butt = []
    # 瞄具
    sight = []
