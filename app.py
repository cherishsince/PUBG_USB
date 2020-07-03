import os
import time

from PIL import Image
import pyscreenshot as ImageGrab

import resource
from drive import box_drive64
from util import image_util, data_config_parser
from util.data_parser import read_data
from weapon import weapon, page_check, weapon_selection, left_right_correction
import environment
import threadpool
import threading
import pythoncom
import PyHook3
import logging
from util import common

# 启动线程池
_executor = environment.env.executor
# 识别的配件信息
_identifying_parts = []
# init 的参数
_lib, _handle, _init_data, _init_weapon_name_data = -1, -1, [], {}
# 配置文件数据
_config_data = {}
# 当前 - 武器配置数据
_current_config_data = None
_current_parts = None

# 是否开枪
_has_shoot = False
_shoot_task = None
# tab 操作是否打开，用于标记多次 tab 按键处理
_has_tab_open = False
# 切换武器，避免多次按
_has_open_selection = False
# 是否选中武器
_has_selection = False
# 是否已识别 武器配件
_has_identification = False
# 武器选择
_weapon_select = 1
# 射击 count
_shoot_count = 0
# 射击修正
_shoot_correction = 0
# 截屏的图片
_capture_image = None


def onMouseEvent(event):
    """
    鼠标事件
    :param event:
    :return:
    """
    global _has_shoot, _executor, _shoot_task, _has_identification
    # 鼠标滚轮建 522
    # 鼠标左键 按下
    if event.Message == 513:
        logging.debug("鼠标 513 -> {}".format(event.MessageName))
        _has_shoot = True

        # 只有已识别，才能进行鼠标操作
        # if _has_identification:
        # _shoot_task = _executor.submit(handle_shoot_correction)
        # _shoot_task = _executor.submit(handle_control_shoot)

    # 鼠标左键 弹起
    elif event.Message == 514:
        logging.debug("鼠标 514 -> {}".format(event.MessageName))
        _has_shoot = False
        if _shoot_task is not None:
            print('取消....')

    # 鼠标右键键 按下
    elif event.Message == 516:
        logging.debug("鼠标右键键 516 -> {}".format(event.MessageName))

    # 鼠标右键键 弹起
    elif event.Message == 517:
        logging.debug("鼠标右键键 517 -> {}".format(event.MessageName))

    else:
        pass
    return True


def onKeyboardEvent(event):
    """
    监听键盘事件
    :param event:
    :return:
    """
    global _has_tab_open, _executor
    keyid = event.KeyID

    # 1 49，2 50，3 51
    if keyid == 9:
        # tab 按键
        logging.debug('tab 按键')

        # 创建一个线程执行
        if not _has_tab_open:
            _has_tab_open = True
            _executor.submit(handle_tab)
    if keyid == 49 or keyid == 50 or keyid == 51:
        print('123')
        # 武器选择
        # if not _has_open_selection:
            # _executor.submit(handle_weapon_select)
    else:
        pass
    return True


def handle_capture_image():
    """
    实施截图，用于图片分析 每次截图在

    0.03366827964782715
    0.03325605392456055
    0.03352046012878418
    0.033231496810913086
    0.033119916915893555
    0.034018754959106445
    :return:
    """
    global _capture_image
    while 1:
        _capture_image = image_util.capture(None)
        time.sleep(0.2)



"""
/////////////
事件控制和切换
/////////////
"""


def handle_tab():
    """
    处理 tab 事件
    :return:
    """
    global _identifying_parts, _lib, _handle, _init_data, _init_weapon_name_data, \
        _has_tab_open, _config_data, _has_identification, _executor, _capture_image

    # time.sleep(0.5)
    # image = image_util.capture()

    try:
        # 判断是否是背包页面
        # image = image_util.capture(None)
        package_positions = page_check.package_positions()
        package_position_images = page_check.package_positions_images(_capture_image, package_positions)
        has_package_page = page_check.has_package_page(package_position_images)
        # 绘制线
        # image_util.drawing_line(image, package_positions)
        # image.show()
        # package_position_images[0].show()

        # 不是则 return
        print('是否背包页面 {}'.format(has_package_page))
        if not has_package_page:
            return

        # 获取配件信息
        main_positions = weapon.main_weapon_parts_positions()
        main_parts_images = weapon.get_weapon_parts(_capture_image, main_positions)

        # 识别配件
        now = time.time()
        identifying_parts = weapon.identifying_parts(_init_data, _init_weapon_name_data, main_parts_images)
        print(identifying_parts)
        if len(identifying_parts) <= 0:
            print('未获取到武器信息 不更新武器信息!')
            return

        _identifying_parts = identifying_parts
        print("识别耗时 {}".format(time.time() - now))

        # 识别成功
        _has_identification = True
        # 选择武器
        # _executor.submit(handle_weapon_select)

    except Exception as e:
        print(e)

    finally:
        # 处理完标记
        _has_tab_open = False


def capture_selection():
    """
    截屏
    :return:
    """
    # 截屏图片
    if environment.is_debug():
        # path = resource.resource_path(os.path.join('img', 'screenshot', '20190413085144_2.jpg'))
        # image = Image.open(path)
        image = ImageGrab.grab()
    else:
        image = ImageGrab.grab()

    return image


def handle_weapon_select():
    """
    处理武器选择，关系压枪数据
    :return:
    """
    global _identifying_parts, _lib, _handle, _init_data, _init_weapon_name_data, \
        _has_tab_open, _config_data, _current_config_data, _current_parts, \
        _has_open_selection, _has_selection, _capture_image

    weapon_positions = weapon_selection.weapon_positions()
    while True:
        try:
            # 获取选择的武器
            # image = capture_selection()
            weapon_images = weapon_selection.weapon_selection_images(_capture_image, weapon_positions)
            weapon_index = weapon_selection.get_selection(weapon_images)
            # logging.info('选择武器成功! {}'.format(weapon_index))

            if weapon_index is None:
                # 0.1 延迟
                _has_selection = False
                time.sleep(0.6)
                logging.debug('为选择武器!')
                # print('为选择武器')
                continue

            logging.info('选择武器成功! {}'.format(weapon_index))

            # 通过识别的数据 - 关联压枪数据
            index = 0
            for parts_info in _identifying_parts:
                index = index + 1
                if weapon_index != index:
                    continue

                if parts_info['name'] is None:
                    continue

                weapon_config_data = _config_data[parts_info['name']]
                if weapon_config_data is None:
                    logging.info('没有找到压枪数据 {}', parts_info)

                # 获取到的数据，和返回数据
                _current_parts = parts_info
                _current_config_data = weapon_config_data
                _has_open_selection = False
                _has_selection = True
                break

            # 0.1 延迟
            time.sleep(0.6)
        except Exception as e:
            print(e)


def handle_shoot_correction():
    """
    处理 射击修正
    :return:
    """
    global _lib, _handle, _init_data, _init_weapon_name_data, _has_identification, \
        _has_shoot, _current_config_data, _current_parts, _shoot_count, _shoot_correction

    correction_positions = left_right_correction.get_positions()
    # 先初始化位0
    _shoot_correction = 0
    # 首次数据纪律
    corr_first_diff = None
    while True:

        # 如果没有识别
        if not _has_identification:
            time.sleep(0.1)
            continue

        # 则 continue，不退出循环，重复创建线程消耗内存
        if not _has_shoot:
            time.sleep(0.1)
            # 先初始化位0
            _shoot_correction = 0
            # 首次数据纪律
            corr_first_diff = None
            continue

        now1 = time.time()
        overtime = None
        # 瞄具 信息
        has_left_right_correction = _current_config_data.left_right_correction
        # 配置超时的时间
        speed = _current_config_data.speed
        if has_left_right_correction == 1:
            overtime = now1 + speed - 0.01

        if overtime is None:
            logging.debug('error 没有起开数据修正')

        now = time.time()

        #  左右修正
        # image = image_util.capture(None)
        image = _capture_image
        if corr_first_diff is None:
            position_images = left_right_correction.get_position_images(image, correction_positions)
            corr_first_1, corr_first_2 = left_right_correction.correction(position_images)
            corr_first_diff = corr_first_1 + corr_first_2

        else:
            # 持续动作获取
            position_images = left_right_correction.get_position_images(image, correction_positions)
            corr_first_1, corr_first_2 = left_right_correction.correction(position_images)
            corr_diff = corr_first_1 + corr_first_2
            x_diff = corr_first_diff - corr_diff

            # 计算偏移值
            if x_diff < 0:
                _shoot_correction = abs(x_diff)
            elif x_diff > 0:
                _shoot_correction = -abs(x_diff)

        # 替代 sleep 方式，需要每次压枪时间要保持一致
        now2 = time.time()
        while True:
            time.sleep(0.005)
            if overtime <= time.time():
                break

        logging.info('处理图片 {} {} 修正的数据 {}'.format(now2 - now, time.time() - now, _shoot_correction))


def handle_control_shoot():
    """
    控制 射击
    :return:
    """
    global _lib, _handle, _init_data, _init_weapon_name_data, _has_identification, \
        _has_shoot, _current_config_data, _current_parts, _shoot_count, \
        _shoot_correction, _has_selection, _capture_image

    try:
        while True:

            # 如果没有识别
            if not _has_identification:
                time.sleep(0.1)
                continue

            # 则 continue，不退出循环，重复创建线程消耗内存
            if not _has_shoot:
                time.sleep(0.1)
                _shoot_count = 0
                continue

            # 没有获取到配置，则退出
            if _current_config_data is None:
                time.sleep(0.1)
                print('_current_config_data')
                continue

            if not _has_selection:
                time.sleep(0.1)
                print('_has_selection')
                continue

            y = 0
            x = 0
            # 每次开始初始化 _shoot_count
            now = time.time()
            # 计算时间，需要保证每次出发的时间一致
            overtime1 = None
            overtime2 = None

            # 检查是否可以射击
            shoot_images = page_check.shoot_images(_capture_image, page_check.shoot_positions())
            has_shoot = page_check.check_shoot(shoot_images)
            if not has_shoot:
                time.sleep(0.1)
                continue

            # 瞄具 信息
            has_left_right_correction = _current_config_data.left_right_correction
            # 配置超时的时间
            speed = _current_config_data.speed
            if has_left_right_correction == 1:
                overtime1 = now + speed - 0.02
                overtime2 = now + speed

            # 检查射击姿势
            stance_images = page_check.stance_images(_capture_image, page_check.stance_positions())
            stance = page_check.check_stance(stance_images)
            if stance is None:
                stance = 'stand'
            shoot_type = stance

            # 获取瞄具数据1
            parts5_value = _current_parts['parts5']
            if parts5_value is None:
                parts5_value = 1

            sight = _current_config_data.sight
            shoot_type_data = sight[shoot_type]
            has_parts5_value = common.arr_contain(shoot_type_data.keys(), str(parts5_value))
            if has_parts5_value:
                shoot_type_data2 = shoot_type_data[str(parts5_value)]
                y = y + mouse_calc_config_data(_shoot_count, shoot_type_data2)

            # 枪口信息
            parts1_values = _current_parts['parts1']
            if parts1_values is not None:
                muzzle = _current_config_data.muzzle
                muzzle_type_data = muzzle[shoot_type]
                has_muzzle_type_data = common.arr_contain(muzzle_type_data.keys(), str(parts1_values))
                if has_muzzle_type_data:
                    muzzle_type_data2 = muzzle_type_data[parts1_values]
                    y = y + mouse_calc_config_data(_shoot_count, muzzle_type_data2)

            # 握把
            parts2_values = _current_parts['parts2']
            if parts2_values is not None:
                grip = _current_config_data.grip
                grip_type_data = grip[shoot_type]
                has_grip_type_data = common.arr_contain(grip_type_data.keys(), str(parts2_values))
                if has_grip_type_data:
                    grip_type_data2 = grip_type_data[parts2_values]
                    y = y + mouse_calc_config_data(_shoot_count, grip_type_data2)

            # 屁股
            parts4_values = _current_parts['parts4']
            if parts4_values is not None:
                butt = _current_config_data.butt
                butt_type_data = butt[shoot_type]
                has_butt_type_data = common.arr_contain(butt_type_data.keys(), str(parts2_values))
                if has_butt_type_data:
                    butt_type_data2 = butt_type_data[parts2_values]
                    y = y + mouse_calc_config_data(_shoot_count, butt_type_data2)

            # 替代 sleep 方式，需要每次压枪时间要保持一致
            while 1:
                # now9 = time.time()
                time.sleep(0.001)
                # print('休眠时间{}'.format(time.time() - now9))
                if overtime1 <= time.time():
                    break

            # 控制鼠标移动
            x = _shoot_correction
            box_drive64.mouse_move_r(_lib, _handle, x, y)
            _shoot_count = _shoot_count + 1

            # 替代 sleep 方式，需要每次压枪时间要保持一致
            while 1:
                # now9 = time.time()
                time.sleep(0.001)
                # print('休眠时间{}'.format(time.time() - now9))
                if overtime2 <= time.time():
                    break

            logging.info("鼠标移动 射击子弹 {} 鼠标x {} 鼠标y {} 射击姿势 {} 耗时:{}"
                         .format(_shoot_count - 1, x, y, shoot_type, time.time() - now))

    except Exception as e:
        print(e)
    finally:
        print('finally')


def mouse_calc_config_data(count, data_arr):
    """
    计算鼠标 data_config data
    :return:
    """
    for i in range(len(data_arr)):
        data = data_arr[len(data_arr) - 1 - i]
        max_count = data[0]
        move_speed = data[1]
        if count >= max_count:
            # print("move_speed {}", move_speed)
            return move_speed

    return 0


"""
/////////////
数据准备
/////////////
"""


def init():
    global _lib, _handle, _init_data, _init_weapon_name_data, _config_data

    # 初始化 drive
    path = resource.resource_path('box64.dll')

    if environment.env.usb_has_default == 1:
        vid = None
        pid = None
        _lib, _handle = box_drive64.init(path, vid, pid)
    else:
        vid = 0xc230
        pid = 0x6899
        _lib, _handle = box_drive64.init(path, vid, pid)

    box_drive64.mouse_move_r(_lib, _handle, 0, 200)
    logging.info('加载 drive 成功！')

    # 读取配置文件
    if os.path.exists('data_config'):
        config_data_path = os.path.join(os.getcwd(), 'data_config')
        print('加载外部 data_config 配置文件..')
    else:
        print('加载exe data_config 配置文件..')
        config_data_path = resource.resource_path('data_config')

    _config_data = data_config_parser.parser(config_data_path)
    logging.info('加载 data_config 成功！')

    # 初始化 配件信息
    parts_path = resource.resource_path(os.path.join('img', 'parts'))
    weapon_name_path = resource.resource_path(os.path.join('img', 'weapon_name'))
    _init_data = weapon.init_parts(parts_path)
    _init_weapon_name_data = weapon.init_weapon_name(weapon_name_path)
    logging.info('加载配件图片数据成功！')

    # 设置返回数据
    return _lib, _handle, _init_data, _init_weapon_name_data


if __name__ == '__main__':
    try:
        # path = resource.resource_path(os.path.join('img', 'screenshot', '20190413085144_2.jpg'))
        # print('path {}'.format(path))
        # Image.open(path).show()

        # 设置日志信息
        if environment.is_debug():
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)

        # 初始化
        lib, handle, init_data, init_weapon_name_data = init()

        # 提前启动，开枪和 左右纠正
        # _executor.submit(handle_shoot_correction)
        # logging.info('开启左右修正!')
        _executor.submit(handle_control_shoot)
        logging.info('开启-自动压枪!')
        logging.info('开启-子弹0不压枪!')
        logging.info('开启-手雷烟雾弹识别!')
        # 选择武器
        _executor.submit(handle_weapon_select)
        logging.info('开启-选择武器!')
        # 开启实时截图
        _executor.submit(handle_capture_image)
        logging.info('开启-实时截屏!')

        # 监听事件
        hm = PyHook3.HookManager()
        hm.KeyDown = onKeyboardEvent
        hm.HookKeyboard()
        hm.MouseAll = onMouseEvent
        hm.HookMouse()
        pythoncom.PumpMessages()

    except Exception as e:
        print(e)
    finally:
        os.system('pause')