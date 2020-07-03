"""

配置环境
"""
from concurrent.futures import ThreadPoolExecutor


def is_debug():
    """
    获取环境 配置
    :return:
    """
    return True
    # return False


"""
环境配置
"""


class env:
    # usb 芯片是否默认端口启动
    usb_has_default = 1
    # 识别线程 5
    executor_parts = ThreadPoolExecutor(max_workers=1)
    # 识别单个配件线程
    executor_unit_parts = ThreadPoolExecutor(max_workers=1)
    # 主线程
    executor = ThreadPoolExecutor(max_workers=5)
    # 配件数量
    parts_size = 6
    # 图片相似度
    img_similarity = 5
    # 配件相似度
    parts_similarity = 5
    # 图片相似度
    name_similarity = 3
    # 配件 过滤值
    parts_colors = [[[0, 35], [0, 40], [0, 60]]]
    # 配件 过滤填充值
    parts_put_color = (255, 255, 255, 0)
    # 武器名字 过滤值
    weapon_name_colors = [[[230, 255], [230, 255], [230, 255]]]
    # 武器名字 填充值
    weapon_name_put_color = (0, 0, 0, 0)
