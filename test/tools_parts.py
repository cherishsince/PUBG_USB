from PIL import Image, ImageGrab
import os
import environment
from util import image_util
import time
import numpy as np
from weapon import weapon


def name():
    img = Image.open('../img/screenshot/20190420220739_1.jpg')

    main_position_arr = weapon.main_weapon_parts_positions()
    weapon_parts_images = weapon.get_weapon_parts(img, main_position_arr)

    # 处理图片色值
    index = 0
    for parts_image in weapon_parts_images:
        parts_index = index % environment.env.parts_size
        colors = [
            [[0, 20], [0, 30], [0, 40]]
        ]
        put_color = (255, 255, 255, 0)
        filter_image, count = image_util.filter_colors_inverse(parts_image, colors, put_color)
        filter_image.save(str(time.time()) + str('_') + str(parts_index) + '.png')

    # 绘制线条
    for i in range(0, len(main_position_arr)):
        image_util.position_line_drawing(img, main_position_arr[i])

    # 显示图片
    img.show()


def parts(img):
    main_position_arr = weapon.main_weapon_parts_positions()
    weapon_parts_images = weapon.get_weapon_parts(img, main_position_arr)

    # 处理图片色值
    # index = 0
    # for parts_image in weapon_parts_images:
    #     parts_index = index % environment.env.parts_size
    #     colors = environment.env.parts_colors
    #     put_color = (255, 255, 255, 0)
    #     filter_image, count = image_util.filter_colors_inverse(parts_image, colors, put_color)
    #     filter_image.save('img/' + str(time.time()) + str('_') + str(parts_index) + '.png')

    # 绘制线条
    image_util.drawing_line(img, main_position_arr)

    # 显示图片
    img.show()


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), '..', 'img', 'screenshot2')
    for filename in os.listdir(path):
        image_path = os.path.join(path, filename)
        parts(Image.open(image_path))
