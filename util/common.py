"""

常用方法
"""
import hashlib


def arr_contain(arr, val):
    """
    数组是否包含 val
    :param arr:
    :param val:
    :return:
    """
    # 判断是否存在
    for key in arr:
        if key == val:
            return True

    return False


def md5(text):
    """
    md5 值
    :param text:
    :return:
    """
    m2 = hashlib.md5()
    m2.update(text.encode("utf-8"))
    return m2.hexdigest()

