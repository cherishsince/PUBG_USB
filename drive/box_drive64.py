import sys
import logging
import ctypes.wintypes
from ctypes import *
import win32api
import win32con


def init(path, vid, pid):
    """
    初始化 驱动(64位)

    :param pid:
    :param vid:
    :param path: box 驱动 dll 地址
    :return: lib, handle
    """
    # 打开盒子
    lib, handle = open_box(path, vid, pid)

    # 设置分辨率
    sys_resolution = [win32api.GetSystemMetrics(win32con.SM_CXSCREEN),
                      win32api.GetSystemMetrics(win32con.SM_CYSCREEN)]
    setting_resolution = lib.M_ResolutionUsed(handle, sys_resolution[0], sys_resolution[1])

    logging.info("设置分辨率 {}".format(sys_resolution))
    logging.info("设置分辨率是否成功 {}".format(setting_resolution == 0))
    return lib, handle


def open_box(path, vid, pid):
    """
    打开 box 驱动
    :param path:
    :param vid:
    :param pid:
    :return:
    """
    lib = ctypes.windll.LoadLibrary(path)
    if vid is None or pid is None:
        lib.M_Open.restype = ctypes.c_uint64
        handle = lib.M_Open(1)
    else:
        lib.M_Open_VidPid.restype = ctypes.c_uint64
        handle = lib.M_Open_VidPid(vid, pid)

    print('open box drive...')
    if handle == -1 or handle == 18446744073709551615:
        print('未检测到 USB 芯片!')
        print('未检测到 USB 芯片!')
        # raise Exception("load dll fail!")
        sys.exit(-1)

    # ctypes.c_uint64(handle) 处理 64 为兼容性问题
    handle = ctypes.c_uint64(handle)
    return lib, handle


def close(lib, handle):
    """
    关闭 box 驱动

    :param lib: 初始化时 lib
    :param handle: 初始化时 open 的 handle
    :return: void
    """
    if handle == -1:
        raise Exception("dll uninitialized!")

    # closeResult = objectDLL.M_Close(ctypes.c_uint64(handle))
    lib.M_Close.restype = ctypes.c_uint64
    lib.M_Close.params = ctypes.c_uint64
    close_result = lib.M_Close(handle)
    print("close handle = " + str(close_result))


def mouse_move_r(lib, handle, x, y):
    """
    鼠标移动 - 相对移动，采用的是 box 的 move3

    注意使用这个的时候需要设置 “分辨率”，否则失效！！！

    :param lib:
    :param handle:
    :param x: 相对位置 x，+1 or -1
    :param y: 相对位置 x，+1 or -1
    :return: void
    """
    lib.M_MoveR2(handle, x, y)


def mouse_left_click(lib, handle):
    """
    鼠标 left 点击

    :param lib:
    :param handle:
    :return: void
    """
    lib.M_LeftClick(ctypes.c_uint64(handle), 1)


def mouse_position(lib):
    """
    获取鼠标 position

    注意：需要设置屏幕分辨率后使用

    :param lib:
    :return:
    """

    # 读取鼠标 position 采用的是，指针方式，需要开启内存
    _x = c_int()
    x = pointer(_x)
    _y = c_int()
    y = pointer(_y)
    lib.M_GetCurrMousePos2(x, y)
    return [x.value, y.value]
