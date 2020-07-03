from PIL import Image
import time
import os

from util import common, image_util
from weapon import weapon
import hashlib
import numpy as np


def main():
    im = Image.open('../img/20190420220739_1.jpg')

    # 获取配件信息
    main_positions = weapon.main_weapon_parts_positions()
    parts_images = weapon.get_weapon_parts(im, main_positions)

    # 绘制线条
    image_util.drawing_line(im, main_positions)
    im.show()

    # for i in range(0, len(parts_images)):
    #     parts_img = parts_images[i]
    # parts_img.save(str('img/') + str(time.time()) + '_' + str(i) + '.png')

    # 初始化 配件信息
    parts_path = os.path.join(os.getcwd(), '../img/parts')
    init_data = weapon.init_parts(parts_path)

    # 识别配件
    weapon.identifying_parts(init_data, parts_images)


def image_md5_arr_test():
    a1 = str(np.array(Image.open('../img/parts/parts1_1.png')))
    a2 = str(np.array(Image.open('../img/parts/parts2_4.png')))

    print(a1)
    print(a2)
    print(a1 == a2)
    print(hashlib.md5(str(np.array(Image.open('../img/parts/parts1_1.png'))).encode(encoding='UTF-8')).hexdigest())
    print(hashlib.md5(str(np.array(Image.open('../img/parts/parts2_1.png'))).encode(encoding='UTF-8')).hexdigest())
    print(hashlib.md5(str(np.array(Image.open('../img/parts/parts2_4.png'))).encode(encoding='UTF-8')).hexdigest())
    print(hashlib.md5(str(np.array(Image.open('../img/parts/parts5_4.png'))).encode(encoding='UTF-8')).hexdigest())


def image_string_test():
    a1 = image_util.image_to_string(np.array(Image.open('../img/parts/parts1_1.png')))
    a2 = image_util.image_to_string(np.array(Image.open('../img/parts/parts2_4.png')))
    print(a1 == a2)


if __name__ == '__main__':
    # main()
    # image_md5_arr_test()

    # 初始化 配件信息
    parts_path = os.path.join(os.getcwd(), '..', 'img', 'weapon_name')
    init_weapon_name_data = weapon.init_parts(parts_path)

    print(init_weapon_name_data)