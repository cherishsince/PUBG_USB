"""

图片提取
"""
from PIL import Image, ImageGrab

import environment
from util import image_util
import numpy as np
import time

from weapon import weapon


def drawing_line_tools():
    """
    线条绘制
    :return:
    """
    img = Image.open('../img/20190420220739_1.jpg')
    main_positions = weapon.main_weapon_parts_positions()
    parts_images = weapon.get_weapon_parts(img, main_positions)
    image_util.drawing_line(img, main_positions)

    for i in range(0, len(parts_images)):
        parts_index = i % environment.env.parts_size
        parts_image = parts_images[i]
        parts_image.save(str(time.time()) + '_' + str(parts_index) + '.png')

    # 显示图片
    img.show()


if __name__ == '__main__':
    # 线条绘制
    drawing_line_tools()
