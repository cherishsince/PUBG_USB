
class weapon_info:
    # 主武器 1
    main1 = None
    # 主武器 2
    main2 = None

    # TODO 手枪辅助武器


class parts:
    # 武器名字
    name = None
    # 枪口：
    # 1 - 步枪消音器
    # 2 - 步枪补偿
    # 3 - 步枪/连狙 消焰器
    # 4 - 狙击补偿
    # 5 - 狙击消音
    parts1 = None
    # 握把：
    # 1 - 垂直握把 
    # 2 - 三角握把 
    # 3 - 轻便式握把
    # 4 - 半截式握把
    # 5 - 拇指握把
    # 6 - 机光瞄准器
    parts2 = None
    # 弹夹: 
    # 1 - 步枪快扩 
    # 2 - 步枪扩容
    # 3 - 步枪快速扩容
    # 4 - 冲锋快扩
    # 5 - 冲锋枪扩容
    # 6 - 冲锋枪加长快扩
    # 7 - 狙击扩容
    # 8 - 狙击快速扩容
    parts3 = None
    # 尾部：
    # 1 - 战术枪托
    # 2 - 托腮板
    # 3 - 98k子弹袋
    parts4 = None
    # 瞄具: 蹲
    # 1 - 红点
    # 2 - 全息
    # 3 - 2倍
    # 4 - 3倍
    # 5 - 4倍
    # 6 - 6倍
    # 7 - 8倍
    # 8 - 15倍
    parts5 = None
    # 瞄具: 站
    # 1 - 红点
    # 2 - 全息
    # 3 - 2倍
    # 4 - 3倍
    # 5 - 4倍
    # 6 - 6倍
    # 7 - 8倍
    # 8 - 15倍
    parts5_1 = None


class partsName:
    # 消音/狙击消音
    silencer = False
    # 消焰器
    flame_eliminate = False
    # 补偿/狙击补偿
    make_up = False
    # 消音
    silencing = False

    # 垂直握把
    vertical_grip = False
    # 半截式握把
    half_grip = False
    # 清醒握把
    sober_grip = False
    # 三角握把
    triangle_grip = False

    # 托腮板
    support_plate = False
    # 子弹带
    bullet_belt = False
