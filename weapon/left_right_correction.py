"""

左右修正

"""
import time
from PIL import Image
import numpy as np
import pyscreenshot as ImageGrab

import environment
from util import image_util


def get_positions():
    start_x = 780
    w = 200
    position1 = (start_x, start_x + w, 22, 23)
    position2 = (start_x, start_x + w, 45, 46)
    return [position1, position2]


def get_position_images(image, positions):
    res = []
    for position in positions:
        x1, x2, y1, y2 = position
        if image is None:
            weapon_img = image_util.capture((x1, y1, x2, y2))
        else:
            weapon_img = image.crop((x1, y1, x2, y2))

        res.append(weapon_img)
    return res


def correction(correction_images):
    # print(1)
    if len(correction_images) <= 1:
        return None

    image1 = correction_images[0]
    image2 = correction_images[1]

    # 坐标颜色  245,244,240
    colors = [
        [[235, 255], [235, 255], [235, 255]],
    ]

    # 坐标一
    has_1 = image_util.find_color_count2(image1, colors, 3)
    has_2 = image_util.find_color_count2(image2, colors, 2)

    # print(has_1)
    # print(has_2)
    return (has_1[2], has_2[2])


if __name__ == '__main__':
    image = Image.open('../img/screenshot/20190413085144_2.jpg')
    # w, h = image.size
    # np_img = np.array(image)
    # rows, cols, _ = np_img.shape
    # #
    # print(np_img[21, 20])
    # print(image.getpixel((20, 21)))
    # for i in range(100):
    #     for j in range(h):
    #         print(np_img[i,j])
    #         # print(np.array(image))

    positions2 = get_positions()
    position_images = get_position_images(image, positions2)

    now = time.time()
    res = correction(position_images)
    print(res)
    print('{}'.format(time.time() - now))

    image_util.drawing_line(image, positions2)
    image.show()