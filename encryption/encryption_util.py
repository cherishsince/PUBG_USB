"""

加密 util

"""

# 密钥信息
import ctypes
from ctypes import *

import resource
from drive import box_drive64

# 用户数据
encryption = 'd36SYCQp5umQ3EDEU2Q1Ig4a4qgdlRw2oMz8Z8kDXA=='
encryption_err = 'd36SYCQp5umQ3EDEU2Q1Ig4a4qgdlRw2oMz8Z8kDXAff=='


def setting_user_data(lib, handle, user_data):
    """
    设置用户数据
    :param lib:
    :param handle:
    :param user_data:
    :return:
    """
    data_in = bytes(str(user_data).encode('utf-8'))
    encryption_len = len(data_in)
    lib.M_SetUserData.restype = ctypes.c_uint64
    res = lib.M_SetUserData(handle, encryption_len, data_in)
    print('设置用户数据 {} res {}'.format(res == 0, res))


def verification_user_data(lib, handle, user_data):
    """
    校验用户数据
    :param lib:
    :param handle:
    :param user_data:
    :return:
    """
    # data_in = c_char * len(user_data)
    data_in = bytes(str(user_data).encode('utf-8'))
    encryption_len = len(data_in)
    lib.M_VerifyUserData.restype = ctypes.c_uint64
    res = lib.M_VerifyUserData(handle, encryption_len, data_in)
    print('校验用户数据 {} res {}'.format(res == 0, res))


def modify_vid_pid(lib, handle, vid, pid):
    """
    修改盒子 vid 和 pid
    :param lib:
    :param handle:
    :param vid:
    :param pid:
    :return:
    """
    # lib.M_ChkSupportMdy.restype = ctypes.c_uint64
    # has_modify = lib.M_ChkSupportMdy(handle)
    res = lib.M_SetNewVidPid(handle, vid, pid, 0x0000, 0x0000)
    print('修改 pid vid 是否成功 {} res {}'.format(res == 0, res))


def modify_vid_pid2():
    # 初始化 drive
    path = resource.resource_path('box64.dll')

    vid = 0xc216
    pid = 0x0301
    lib, handle = box_drive64.open_box(path, vid, pid)

    # 修改 pid 和 vid
    m_vid, m_pid = 0xc230, 0x6899
    modify_vid_pid(lib, handle, m_vid, m_pid)


def setting_user_data2():
    # 初始化 drive
    path = resource.resource_path('box64.dll')

    vid = 0xc230
    pid = 0x6899
    lib, handle = box_drive64.open_box(path, vid, pid)

    # 修改 pid 和 vid
    setting_user_data(lib, handle, encryption)
    # verification_user_data(lib, handle, encryption)
    # verification_user_data(lib, handle, encryption_err)


def verification_user_data2():
    # 初始化 drive
    path = resource.resource_path('box64.dll')

    vid = 0xc230
    pid = 0x6899
    lib, handle = box_drive64.open_box(path, vid, pid)

    # 修改 pid 和 vid
    # setting_user_data(lib, handle, encryption)
    verification_user_data(lib, handle, encryption)
    verification_user_data(lib, handle, encryption_err)


if __name__ == '__main__':
    # modify_vid_pid2()
    # setting_user_data2()
    verification_user_data2()
