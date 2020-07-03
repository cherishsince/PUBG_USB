import time
import os
import hashlib
from util import image_util
from PIL import Image, ImageGrab
from numpy import average, dot, linalg


def init_parts(path):
    """
    初始化 配件信息
    :param path:
    :return:
    """
    sports_data = {}
    m2 = hashlib.md5()
    for filename in os.listdir(path):
        image_path = os.path.join(path, filename)
        parts_image = Image.open(image_path)
        # 将配件图片 转换为 像素点 str 保存 map 提高图片识别速度
        parts_str = str(parts_image.load())

        # 转换为 md5 减少内存使用
        m2.update(parts_str.encode("utf-8"))
        parts_md5 = m2.hexdigest()

        # 设置 init 数据
        parts_name = filename.replace('.png', '')
        sports_data[parts_md5] = parts_name

    return sports_data


def img_similarity_test():
    # img1 = Image.open('img/1555815389.779096_5.png')
    img1 = Image.open('1555825823.551665_2.png')
    img2 = Image.open('1555825864.82494_2.png')
    now = time.time()
    print(image_util.img_similarity(img1, img2))
    print('耗时 {}'.format(time.time() - now))
    print('耗时 {}'.format(now))
    print('耗时 {}'.format(time.time()))

    # 39, 47, 50      96,98,97    190,121,106
    # colors = [
    #     [[0, 39], [0, 47], [0, 50]],
    #     [[190 + 5, 190 - 5], [121 + 5, 121 - 5], [106 + 10, 106 - 10]],
    # ]
    # put_color = (255, 255, 255, 0)

    # img1, count = image_util.filter_colors_inverse(img1, colors, put_color)
    # img2, count = image_util.filter_colors_inverse(img2, colors, put_color)
    # print(image_util.img_similarity(img1, img2))


if __name__ == '__main__':
    img_similarity_test()

    # path = os.path.join(os.getcwd(), '../img/parts')
#     # parts_data = init_parts(path)
#     # print(parts_data)
