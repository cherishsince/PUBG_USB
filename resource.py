import os
import sys
import time


def resource_path(relative_path):
    """
    获取 资源路径
    :param relative_path:
    :return:
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    # path = resource_path('img/screenshot/20190413085144_2.jpg')
    # print(path)

    text = '请稍等... 正在为您配置...'
    for i in range(len(text)):
        print(text[i], end='')
        time.sleep(0.1)
