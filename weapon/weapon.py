"""

武器名字识别
"""
import os
import time

from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed, ALL_COMPLETED, wait

import environment
from util import image_util, common, image_util2, image_util3

# 启动线程池
_executor_parts = environment.env.executor_parts
_executor_unit_parts = environment.env.executor_unit_parts


def init_parts(path):
    """
    初始化 配件信息
    :param path:
    :return:
    """
    sports_data = {}
    for filename in os.listdir(path):
        image_path = os.path.join(path, filename)
        parts_image = Image.open(image_path)
        # 根据 parts1、2、3 这种分类
        parts_classification = filename.replace('.png', '').split('_')[0]

        # 设置 init 数据
        has_key = common.arr_contain(sports_data.keys(), parts_classification)
        if has_key:
            sports_data[parts_classification].append(parts_image)
        else:
            sports_data[parts_classification] = [parts_image]

    return sports_data


def init_weapon_name(path):
    """
    初始化 武器名字
    :param path:
    :return:
    """
    sports_data = {}
    for filename in os.listdir(path):
        image_path = os.path.join(path, filename)
        parts_image = Image.open(image_path)
        # 根据 parts1、2、3 这种分类
        parts_classification = filename.replace('.png', '').split('_')[0]

        # 设置 init 数据
        sports_data[parts_classification] = parts_image

    return sports_data


def get_weapon_parts(img, main_positions):
    """
    获取武器 配件信息
    :param main_positions:
    :param img:
    :return:
    """
    # 主武器 位置信息
    parts_images = []
    # 绘制线条/保存图片
    for i in range(0, len(main_positions)):
        # 保存图片
        x1, x2, y1, y2 = main_positions[i]

        if img is None:
            im = image_util.capture((x1, y1, x2, y2))
        else:
            im = img.crop((x1, y1, x2, y2))

        if i % 6 == 0:
            put_weapon_name(im)
        else:
            put_weapon_parts(im)

        parts_images.append(im)

    return parts_images


def main_weapon_parts_positions():
    """
    所有主武器 配件位置信息
    :return:
    """
    # 主武器开始 x 坐标
    main_start_x = 1347
    # 主武器开始 y 坐标
    main_start_y = 96
    # 主武器名字 宽度
    main_name_w = 60
    # 主武器名字 高度
    main_name_h = 28
    # 主武器 之间的距离 y
    main_distance_y = 230

    # box x1,x2,y1,y2
    weapon_line_array = []
    for i in range(0, 2):
        x1, x2 = main_start_x, main_start_x + main_name_w
        # y1, y2 = 0, 0

        if i == 0:
            y1, y2 = main_start_y, main_start_y + main_name_h
        else:
            y1, y2 = main_start_y + main_distance_y, main_start_y + main_distance_y + main_name_h

        # main box
        main_box = (x1, x2, y1, y2)
        main_weapon_line = main_weapon_parts_position(main_box)

        if len(weapon_line_array) > 0:
            weapon_line_array = np.vstack((weapon_line_array, main_weapon_line))
        else:
            weapon_line_array = main_weapon_line

    return weapon_line_array


def main_weapon_parts_position(main):
    """
    主武器 配件信息
    :param main:
    :return:
    """
    # 50 像素 小方块
    parts_size = 42
    # 武器和配件的距离 y
    parts_distance_y = main[2] + 155
    parts1 = (1316, 1316 + parts_size, parts_distance_y, parts_distance_y + parts_size)
    parts2 = (1419, 1419 + parts_size, parts_distance_y, parts_distance_y + parts_size)
    parts3 = (1528, 1528 + parts_size, parts_distance_y, parts_distance_y + parts_size)
    parts4 = (1740, 1740 + parts_size, parts_distance_y, parts_distance_y + parts_size)
    parts5 = (1588, 1588 + parts_size, main[2] + 24, main[2] + 24 + parts_size)
    return [main, parts1, parts2, parts3, parts4, parts5]


def put_weapon_name(im):
    """
    填充 武器名字
    :param im:
    :return:
    """
    # 名字 只保留白色
    # 配件信息，只保留 黑色
    colors = environment.env.weapon_name_colors
    put_color = environment.env.weapon_name_put_color
    im, count = image_util.filter_colors_inverse(im, colors, put_color)
    return im, count


def put_weapon_parts(im):
    """
    填充 武器配件
    :param im:
    :return:
    """
    # 配件信息，只保留 黑色
    colors = environment.env.parts_colors
    put_color = environment.env.parts_put_color
    im, count = image_util.filter_colors_inverse(im, colors, put_color)
    return im, count


"""
识别 配件信息/ 识别武器 操作
"""


def identifying_parts(init_data, init_weapon_name_data, parts_images):
    """
    识别配件信息
    :param init_data:
    :param init_weapon_name_data:
    :param parts_images:
    :return:
    """
    global _executor

    # 武器信息 - 配件信息
    weapon_info_parts = []
    weapon_parts = {}

    task_arr = []
    for i in range(0, len(parts_images)):
        parts_index = i % environment.env.parts_size
        parts_image = parts_images[i]
        if parts_index == 0:
            # parts_index == 0 为武器名字
            weapon_parts = {}
            weapon_info_parts.append(weapon_parts)

            # 创建一个 task
            # task = _executor_parts.submit(identification_weapon_name, parts_image, init_weapon_name_data, weapon_parts)
            # task_arr.append(task)
            # 武器处理
            # weapon_name = identification_weapon_name(parts_image, init_weapon_name_data, weapon_parts)
            identification_weapon_name(parts_image, init_weapon_name_data, weapon_parts)

            # 设置 weapon_parts
            # weapon_parts['name'] = weapon_name
        else:
            parts_key = 'parts' + str(parts_index)
            identification_unit_parts(parts_image, init_data, parts_key, weapon_parts)
            # has_parts, parts_index = identification_unit_parts(parts_image, init_data, parts_key, weapon_parts)
            # if has_parts:
            #     weapon_parts[parts_key] = parts_index + 1
            # else:
            #     weapon_parts[parts_key] = None

            # 创建一个 task
            # task = _executor_parts.submit(identification_unit_parts, parts_image, init_data, parts_key, weapon_parts)
            # task_arr.append(task)

    # wait(task_arr, return_when=ALL_COMPLETED)
    # print("main")
    for future in as_completed(task_arr):
        try:
            resp = future.result()
        except Exception as e:
            print('%s' % e)
        else:
            print('else ->> {}'.format(resp))

    # for task in task_arr:
    #     print(task.result())
    # for future in as_completed(task_arr):
    #     data = future.result()
    #     print("in main: get page {}s success".format(data))

    # 返回识别的信息
    return weapon_info_parts


def identification_unit_parts(parts_image, init_data, parts_key, weapon_parts):
    """
    识别某个配件

    :param weapon_parts:
    :param parts_image:
    :param init_data:
    :param parts_key:
    :return:
    """
    now = time.time()
    has_key = common.arr_contain(init_data.keys(), parts_key)
    if has_key:
        parts_images2 = init_data[parts_key]
        # parts_image.show()
        task_arr = []
        for ii in range(len(parts_images2)):
            parts_image2 = parts_images2[ii]
            # parts_image2.show()
            # task = _executor_unit_parts.submit(image_util.img_similarity, parts_image, parts_image2)
            # task_arr.append(task)
            similarity_value = image_util3.class_histogram_with_split(parts_image2, parts_image)
            # print('key {} val{}', parts_key, similarity_value)
            if similarity_value <= environment.env.parts_similarity:
                weapon_parts[parts_key] = ii + 1
                # print('识别某个配件 parts_key {} {}'.format(parts_key, time.time() - now))
                return True, ii, parts_key

        # for future in as_completed(task_arr):
        #     try:
        #         similarity_value = future.result()
        #     except Exception as e:
        #         print('%s' % e)
        #     else:
        #         print('else ->> {}'.format(similarity_value))
        #         if similarity_value >= environment.env.img_similarity:
        #             weapon_parts[parts_key] = i + 1
        #             return True, i, parts_key

    weapon_parts[parts_key] = None
    # print('识别某个配件 parts_key {} {}'.format(parts_key, time.time() - now))
    return False, -1, parts_key


def identification_weapon_name(parts_image, init_weapon_name_data, weapon_parts):
    """
    识别 武器名字
    :param weapon_parts:
    :param parts_image:
    :param init_weapon_name_data:
    :return:
    """
    res_weapon_name = None
    # parts_image.show()
    for weapon_name in init_weapon_name_data:
        weapon_image = init_weapon_name_data[weapon_name]
        similarity_res = image_util3.class_histogram_with_split(parts_image, weapon_image)
        # print('武器名字 {}'.format(similarity_res))
        # weapon_image.show()
        if similarity_res <= environment.env.name_similarity:
            res_weapon_name = weapon_name
            break

    weapon_parts['name'] = res_weapon_name
    # print('识别 武器名字 {}'.format(time.time() - now))
    return res_weapon_name, 'name'

# def setting_weapon_parts(index, weapon_parts, value):
#     """
#     设置 weapon parts 暂时不用
#     :param index:
#     :param weapon_parts:
#     :param value:
#     :return:
#     """
#     if index == 0:
#         weapon_parts.name = value
#     elif index == 1:
#         weapon_parts.parts1 = value
#     elif index == 2:
#         weapon_parts.parts2 = value
#     elif index == 3:
#         weapon_parts.parts3 = value
#     elif index == 4:
#         weapon_parts.parts4 = value
#     elif index == 5:
#         weapon_parts.parts5 = value
