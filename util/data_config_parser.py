"""

数据配置解析器

data_config  目录下的配置文件
"""
import json
import os

import resource
from util import data_config_object


def parser(path):
    """
    配置文件 path
    :param path:
    :return:
    """
    data_object_arr = {}
    for file_name in os.listdir(path):
        config = open(os.path.join(path, file_name), encoding='utf-8')
        config_data = json.load(config)
        data_object = data_config_object.Data()
        data_object.name = config_data['name']
        data_object.left_right_correction = config_data['left_right_correction']
        data_object.speed = config_data['speed']
        data_object.muzzle = config_data['muzzle']
        data_object.grip = config_data['grip']
        data_object.clip = config_data['clip']
        data_object.butt = config_data['butt']
        data_object.sight = config_data['sight']
        # print('data_object -> {}'.format(data_object))
        filed = file_name.replace('.json', '')
        data_object_arr[filed] = data_object

        print('加载配置 ->{}'.format(file_name))

    return data_object_arr


if __name__ == '__main__':
    path = resource.resource_path('data_config')
    parser(path)
