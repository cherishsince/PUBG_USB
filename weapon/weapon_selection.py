"""

武器选择
"""
from PIL import Image
import weapon
from util import image_util


def weapon_positions():
    """
    武器位置
    :return:
    """
    weapon_h = 10
    weapon_w = 80
    weapon_start_x = 1520
    weapon_start_y = 955

    weapon_distance_y = 60
    weapon1_box = (weapon_start_x, weapon_start_x + weapon_w, weapon_start_y, weapon_start_y + weapon_h)
    weapon2_box = (weapon_start_x, weapon_start_x + weapon_w,
                   weapon_start_y + weapon_distance_y, weapon_start_y + weapon_distance_y + weapon_h)
    return [weapon1_box, weapon2_box]


def weapon_selection_images(image, positions):
    """
    武器选择
    :param image:
    :param positions:
    :return:
    """
    res = []
    for position in positions:
        x1, x2, y1, y2 = position
        if image is None:
            weapon_img = image_util.capture((x1, y1, x2, y2))
        else:
            weapon_img = image.crop((x1, y1, x2, y2))
        res.append(weapon_img)
    return res


def get_selection(weapon_image_arr):
    """
    获取 选择的武器
    :param weapon_image_arr:
    :return:
    """

    # 被使用的武器，会变白色   217,214,209
    colors = [
        [[200, 255], [200, 255], [200, 255]],
    ]

    max_count = 5
    select_index = None
    for i in range(0, len(weapon_image_arr)):
        weapon_image = weapon_image_arr[i]
        has_find = image_util.find_color_count(weapon_image, colors, max_count)
        # weapon_image.show()
        if has_find:
            select_index = len(weapon_image_arr) - i
            break

    return select_index


if __name__ == '__main__':
    img = Image.open('../img/screenshot/20190413085144_2.jpg')
    # 选择的 position
    selection_positions = weapon_positions()
    # 绘制线条
    image_util.drawing_line(img, selection_positions)
    img.show()
    # 获取武器选择的图片
    weapon_images = weapon_selection_images(img, selection_positions)
    # 获取选择的武器
    selection_index = get_selection(weapon_images)

    print('选择的武器 {}'.format(selection_index))
