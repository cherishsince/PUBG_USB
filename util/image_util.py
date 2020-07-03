import os
import time
from PIL import Image, ImageGrab
from functools import reduce
# import pyscreenshot as ImageGrab
import numpy as np
from numpy import average, dot, linalg
import math
import operator

import environment
import resource


def capture(box):
    """
    截屏
    :return:
    """
    if box is None:
        box = (0, 0, 1920, 1080)

    # now = time.time()
    # 截屏图片
    if environment.is_debug():
        # path = resource.resource_path(os.path.join('img', 'screenshot2', '20190423112307_1.jpg'))
        # image = Image.open(path)
        image = ImageGrab.grab(box)
    else:
        image = ImageGrab.grab(box)
    # image.save(str(time.time()) + '_ccc.png')
    # print('截图耗时 {}'.format(time.time() - now))
    return image


def drawing_line(img, positions):
    """
    绘制线条
    :param img:
    :param positions:
    :return:
    """
    # 绘制线条/保存图片
    for i in range(0, len(positions)):
        # 绘制线条
        position_line_drawing(img, positions[i])


def position_line_drawing(im, box):
    """
    绘制 position 线条

    用于：debug 或者测试，让图片更加明显
    :param im:
    :param box:
    :return: im 绘制后的图片
    """

    x1, x2, y1, y2 = box

    # 线条颜色值
    put_color = (228, 230, 0, 0)

    # x 轴线
    for x in range(x1, x2):
        put_x1, put_y1 = x, y1
        put_x2, put_y2 = x, y2
        im.putpixel((put_x1, put_y1), put_color)
        im.putpixel((put_x2, put_y2), put_color)

    # y 轴线
    for y in range(y1, y2):
        put_x1, put_y1 = x1, y
        put_x2, put_y2 = x2, y
        im.putpixel((put_x1, put_y1), put_color)
        im.putpixel((put_x2, put_y2), put_color)

    return im


def img_to_8bit(image, size=(64, 64), greyscale=False):
    """
    图片 to 8bit
    :param image:
    :param size:
    :param greyscale:
    :return:
    """
    # 利用image对图像大小重新设置, Image.ANTIALIAS为高质量的
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        # 将图片转换为L模式，其为灰度图，其每个像素用8个bit表示
        image = image.convert('L')

    return image


def img_similarity(img1, img2):
    """
    图片相似度
    :param img1:
    :param img2:
    :return:
    """
    res = None
    try:
        # img1 = img_to_8bit(img1)
        # img2 = img_to_8bit(img2)
        # images = [img1, img2]
        # vectors = []
        # norms = []
        # for image in images:
        #     vector = []
        #     for pixel_tuple in image.getdata():
        #         vector.append(average(pixel_tuple))
        #     vectors.append(vector)
        #     # linalg=linear（线性）+algebra（代数），norm则表示范数
        #     norms.append(linalg.norm(vector, 2))
        # a, b = vectors
        # a_norm, b_norm = norms
        # # dot返回的是点积，对二维数组（矩阵）进行计算
        # res = dot(a / a_norm, b / b_norm)
        h1 = img1.histogram()
        h2 = img2.histogram()
        res = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    except Exception as e:
        print(e)
    finally:
        return res


def filter_colors_inverse(img, colors, put_color):
    """
    过滤色值
    将指定色值填充位某一色值
    :param put_color:
    :param img:
    :param colors:
    :return:
    """
    # 图片信息
    width, height = img.size
    pixel = img.load()
    count = 0
    for i in range(0, width):  # 遍历所有长度的点
        for j in range(0, height):  # 遍历所有宽度的点
            rgb = pixel[i, j]  # 打印该图片的所有点
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]

            for color_rgb in colors:
                if (color_rgb[0][0] <= r <= color_rgb[0][1]
                        and color_rgb[1][0] <= g <= color_rgb[1][1]
                        and color_rgb[2][0] <= b <= color_rgb[2][1]):
                    # 则这些像素点的颜色改成  其他色色值
                    count = count + 1
                    continue
                else:
                    img.putpixel((i, j), put_color)

    img = img.convert("RGB")  # 把图片强制转成RGB
    return img, count


def find_color_count(img, colors, max_count):
    find_result = find_color_count2(img, colors, max_count)
    return find_result[0]


def find_color_count2(img, colors, max_count):
    # 图片信息
    # np_img = np.array(img)
    # row y，cols x
    # rows, cols, _ = np_img.shape
    width, height = img.size
    pixel = img.load()
    count = 0
    for i in range(0, width):  # 遍历所有长度的点
        for j in range(0, height):  # 遍历所有宽度的点
            # 使用的是 np_img， x y 坐标相反
            x, y = j, i
            rgb = pixel[y, x]
            # rgb = np_img[x, y]
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]

            for color_rgb in colors:
                if (color_rgb[0][0] <= r <= color_rgb[0][1]
                        and color_rgb[1][0] <= g <= color_rgb[1][1]
                        and color_rgb[2][0] <= b <= color_rgb[2][1]):
                    # 则这些像素点的颜色改成  其他色色值
                    count = count + 1
                    if count >= max_count:
                        return True, x, y
                else:
                    count = 0
    return False, 0, 0


def image_to_string(image_arr):
    """
    图片转 字符串
    :param image_arr:
    :return:
    """
    image_str = ''
    for i in image_arr:
        image_str = image_str + str(i)

    return image_str


if __name__ == '__main__':
    time.sleep(1)
    image = capture(None)
    image.show()
    # im1 = Image.open('../img/parts/parts1_1.png')
    # im2 = Image.open('../img/parts/parts1_2.png')
    # print(pil_image_similarity(im1, im2))