"""

页面检查
"""
import os
import time

import resource
from util import image_util
from PIL import Image

"""
//////////////////
检查是否背包页面
//////////////////
"""


def package_positions():
    """
    获取 背包 位置
    :return:
    """
    position1 = (110, 170, 55, 90)
    return [position1]


def package_positions_images(image, position_arr):
    """
    获取 背包 位置图片
    :param image:
    :param position_arr:
    :return:
    """
    res = []
    for position in position_arr:
        x1, x2, y1, y2 = position

        if image is None:
            res.append(image_util.capture((x1, y1, x2, y2)))
        else:
            res.append(image.crop((x1, y1, x2, y2)))

    return res


def has_package_page(image_arr):
    """
    是否 背包 页面
    :param image_arr:
    :return:
    """

    # 检查白色  167,162,157   163,164,166  157,157,155
    colors = [
        [[167 - 20, 167 + 20], [162 - 30, 162 + 30], [157 - 40, 157 + 40]],
    ]
    max_count = 5
    has_page = False
    for position_image in image_arr:
        has_page = image_util.find_color_count(position_image, colors, max_count)
        if has_page:
            break

    return has_page


"""
//////////////////
检查是开枪
//////////////////
"""


def shoot_positions():
    """
    获取开枪 需要检查点的
    :return:
    """
    position1 = (1560, 1563, 950, 1040)
    return [position1]


def shoot_images(image, shoot_positions):
    """
    获取 开枪图片
    :param image:
    :param shoot_positions:
    :return:
    """
    res = []
    for position in shoot_positions:
        x1, x2, y1, y2 = position

        if image is None:
            res.append(image_util.capture((x1, y1, x2, y2)))
        else:
            res.append(image.crop((x1, y1, x2, y2)))

    return res


def check_shoot(shoot_images):
    """
    检查 是否开枪装填
    :param shoot_images:
    :return:
    """
    # 检查红色  221,18,12
    colors = [
        [[220, 255], [0, 20], [0, 20]],
    ]
    max_count = 3
    has_page = False
    for position_image in shoot_images:
        has_page = image_util.find_color_count(position_image, colors, max_count)
        if has_page:
            break

    return not has_page


"""
//////////////////
检查开枪姿势
//////////////////
"""


def stance_positions():
    position1 = (715, 720, 1005, 1010)
    position2 = (715, 720, 1023, 1028)
    position3 = (715, 720, 1036, 1041)
    return [position1, position2, position3]


def stance_images(image, positions):
    """
       获取 检查开枪姿势
       :param positions:
       :param image:
       :return:
       """
    res = []
    for position in positions:
        x1, x2, y1, y2 = position

        if image is None:
            res.append(image_util.capture((x1, y1, x2, y2)))
        else:
            res.append(image.crop((x1, y1, x2, y2)))

    return res


def check_stance(images):
    """
       获取 检查开枪姿势

        # stand 站着
        # squat 蹲着
        # prostrate 趴着

       :param images:
       :return:
       """
    res = None
    # 检查红色  221,18,12
    colors = [
        [[190, 233], [190, 233], [190, 233]],
    ]
    max_count = 2
    for i in range(len(images)):
        image = images[i]
        # image.show()
        if i == 0:
            # 站着
            has_stand = image_util.find_color_count(image, colors, max_count)
            if has_stand:
                res = 'stand'
                break
        elif i == 1:
            # 蹲着
            has_squat = image_util.find_color_count(image, colors, max_count)
            if has_squat:
                res = 'squat'
                break
        elif i == 2:
            # 蹲着
            has_prostrate = image_util.find_color_count(image, colors, max_count)
            if has_prostrate:
                res = 'prostrate'
                break
    return res


"""
//////////////////
检查是否开镜
//////////////////
"""

if __name__ == '__main__':
    # path = resource.resource_path(os.path.join('img', 'screenshot', '20190423175051_1.jpg'))
    # path = resource.resource_path(os.path.join('img', 'screenshot', '20190424225757_1.jpg'))
    # path = resource.resource_path(os.path.join('img', 'screenshot', '20190425100723_1.jpg'))
    path = resource.resource_path(os.path.join('img', 'screenshot', '20190425100717_1.jpg'))
    # path = resource.resource_path(os.path.join('img', 'screenshot', '20190425100714_1.jpg'))
    img = Image.open(path)

    # positions = package_positions()
    # position_images = package_positions_images(img, positions)
    # has_package = has_package_page(position_images)

    # positions = shoot_positions()
    # position_images = shoot_images(img, positions)
    # has_shoot = check_shoot(position_images)

    now = time.time()
    positions = stance_positions()
    position_images = stance_images(img, positions)
    has_stance = check_stance(position_images)

    # 绘制线
    image_util.drawing_line(img, positions)
    print('耗时{}'.format(time.time() - now))
    print(has_stance)

    img.show()
