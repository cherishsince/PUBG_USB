"""

data 解析器


数据格式说明

武器名字,左右修正,射速,步枪消音+20后坐力|武器补偿 -10 等...
M416   = 1,      0.06, 1-1 +20        |1-2 _10    |1-3 5, 2-1 _10|2-2 _5|2-3 _2|2-4 _5|2-5 _2,, 4-1 _20,
5-1 10-20 20-20|5-2 10-20 20-20|5-3 0-10 10-20|5-4 0-10 10-20|5-5 0-10 10-20|5-6 0-10 10-20

"""
from util.data_object import DataObject


def read_data(data_path):
    """
    读取 data 数据
    :param data_path:
    :return:
    """
    file = open(data_path)
    data_object = {}
    while 1:
        line = file.readline()
        if not line:
            break

        # 解析内容
        data = parser(line)
        data_object[data.name] = data
        pass

    return data_object


def parser(line_text):
    """
    解析 line text
    :param line_text:
    :return:
    """
    name, arr1 = str(line_text).split('=')
    arr2 = str(arr1).split(',')

    # 创建 data_object 保存解析数据
    data_object = DataObject()
    data_object.name = str(name).strip()
    data_object.left_right_correction = int(str(arr2[0]).strip())
    data_object.speed = float(str(arr2[1]).strip())
    data_object.muzzle = parser_sight(arr2[2])
    data_object.grip = parser_sight(arr2[3])
    data_object.clip = parser_sight(arr2[4])
    data_object.butt = parser_sight(arr2[5])
    data_object.sight = parser_sight(arr2[6])
    return data_object


def parser_sight(split_text):
    """
    瞄具解析器
    :param split_text:
    :return:
    """
    res = {}
    split_text = str(split_text).strip()
    if len(split_text) <= 0:
        return res

    arr1 = split_text.split('|')
    for item in arr1:
        arr2 = str(item).split(' ')
        key = arr2[0]

        sight_speed = []
        for i in range(1, len(arr2)):
            sight_speed.append(arr2[i])

        res[key] = sight_speed

    return res


def parser_parts(split_text):
    """
    配件解析器
    :param split_text:
    :return:
    """
    res = {}
    split_text = str(split_text).strip()
    if len(split_text) <= 0:
        return res

    arr1 = split_text.split('|')
    for item in arr1:
        key, val = str(item).split(' ')
        res[key] = int(str(val).replace('_', '-'))

    return res


if __name__ == '__main__':
    read_data('../data')
