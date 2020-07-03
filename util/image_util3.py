# -*- coding:utf-8 -*-

from functools import reduce
from PIL import Image


# 計算圖片的局部哈希值--pHash
def phash(img):
    """
    :param img: 圖片
    :return: 返回圖片的局部hash值
    """
    img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
    hash_value = reduce(lambda x, y: x | (y[1] << y[0]),
                        enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())),0)
    # print(hash_value)
    return hash_value


# 計算漢明距離:
def hamming_distance(a, b):
    """
    :param a: 圖片1的hash值
    :param b: 圖片2的hash值
    :return: 返回兩個圖片hash值的漢明距離
    """
    hm_distance = bin(a ^ b).count('1')
    # print(hm_distance)
    return hm_distance


# 計算兩個圖片是否相似:
def class_histogram_with_split(img1, img2):
    """
    :param img1: 圖片1
    :param img2: 圖片2
    :return:  True 圖片相似  False 圖片不相似
    """
    distance = hamming_distance(phash(img1), phash(img2))
    # print(distance)
    # return True if distance <= 5 else False
    return distance


if __name__ == '__main__':
    # 讀取圖片
    im1 = Image.open('../img/parts/parts5_6.png')
    im2 = Image.open('../img/parts/parts5_8.png')

    # 比較圖片相似度
    result = class_histogram_with_split(im1, im2)

    print(result)
