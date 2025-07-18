# emulator-5560
import _thread
import datetime

from airtest.core.api import *
from dao import airMultiPhotos as air
from dao import changeVar as cv
import logging

# 日志只输出INFO等级，debugger等级不输出。
logger = logging.getLogger("airtest")
logger.setLevel(logging.INFO)

cv._init()
cv.set_value("path", cv.DBLPath)
cv.set_value("device", cv.DBLdevice)
# cv.set_value("device", cv.DBLdeviceHome)
flag = True

__author__ = "user"
exitFlag = 0


def cvInit(path=cv.DBLPath, device=cv.DBLdevice):
    cv._init()
    cv.set_value("path", path)
    cv.set_value("device", device)
    # cv.set_value("device", cv.DBLdeviceHome)


# RUSH入口
# 2023年1月2日16:37:59
def autoRush():
    photoMap = air.Photo()
    photoMaps = [
        "编组",
        "自动编组",
        "结算OK",
        "战斗结束",
        "rush立刻挑战",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "编组".__eq__(name):
            touch(pos)
            startRush()
            continue

        touch(pos)
        sleep(0.3)


def startRush():
    photoMap = air.Photo()
    photoMaps = [
        "战斗结束",
        "结算OK",
        "战斗开始",
        "战斗中",
        "点数报酬",
        "编组",
        "自动编组",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "编组".__eq__(name):
            touch(pos)
            continue

        if "战斗开始".__eq__(name):
            touch(pos)
            sleep(60)
            continue

        if "战斗中".__eq__(name):
            touch(pos)
            sleep(20)
            continue

        if "战斗结束".__eq__(name) | "点数报酬".__eq__(name):
            touch(pos)
            continue

        if "结算OK".__eq__(name):
            touch(pos)
            break

        touch(pos)
        sleep(0.3)


# 自动百重塔入口
# 2023年1月2日16:37:40
def auto100():
    photoMap = air.Photo()
    photoMaps = [
        "百层是",
        "战斗结束",
        "前往下个层级",
        "再次对战",
        "战斗中",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        if "战斗中".__eq__(name):
            touch(pos)
            sleep(60)
            continue
        touch(pos)
        sleep(0.3)


# 2023年1月2日16:37:18
# 自动团队战入口
def autoBattle(time=0):
    photoMap = air.Photo()
    photoMaps = [
        "战斗开始",
        "前往战斗",
        "按错取消",
        "结算OK",
        "准备完成",
        "前往大厅",
        "读取中",
        "寻找",
        "游玩",
        "准备完成",
        "限定报酬",
        "重试",
    ]
    moveMaps = [
        (),
    ]

    try:
        print("开启监控升龙".format())
        _thread.start_new_thread(autoBattleDragon, ())
    except:
        print("Error: 无法启动线程")

    count = 0

    while (count < time) | (time == 0):
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        if "读取中".__eq__(name):
            autoBattleNext()
            count += 1
            print("第{}次战斗结束，返回大厅。".format(count))
            continue
        touch(pos)
    exitFlag = 1


def autoBattleNext():
    photoMap = air.Photo()
    photoMaps = [
        "结算OK",
        "按错取消",
        "前往大厅",
        "游玩",
        "重试",
        "继续战斗",
        "准备完成",
        "准备完成2",
        "准备完成3",
        "战斗中",
        # "战斗开始",
    ]
    moveMaps = [
        (370, 470),  # 0 第1张卡
        (520, 420),  # 1 第2张卡
        (680, 400),  # 2 第3张卡
        (850, 400),  # 3 第4张卡
        (130, 460),  # 主动
        # (120,377), # 拉仇恨
        (99, 322),  # 点击队友
        # (919,461),
    ]
    moveMapsMumu =[
        (504, 875),  # 0 开主动
        (200, 730),  # 1 第1张卡
        (300, 730),  # 2 第2张卡
        (400, 730),  # 3 第3张卡
        (480, 730),  # 4 第4张卡
        (65, 730+100),  # 主动
        # (120,377), # 拉仇恨
        (32, 529),  # 点击队友
    ]
    moveMaps1 = [
        (721, 300),  # 0 第四个
        (721, 360),  # 1 第四个
        (721, 420),  # 2 第四个
    ]
    # 临时措施 2025年5月14日
    moveMaps = moveMapsMumu
    while 1:
        photoMap.loopSearch(photoMaps, time=0.3)
        pos = photoMap.pos
        name = photoMap.name
        # print(G.DEVICE.display_info["orientation"])

        # if "升龙2".__eq__(name):
        #     touch(pos)
        #     touch(pos)
        #     touch(pos)
        #     continue

        if "战斗中" in name:
            for i in moveMaps:
                # 竖屏和横屏的XY反过来。
                # temp = changeXY(i)
                # print("原坐标:{},{},TEMP是{},{}。".format(i[0],i[1],temp[0],temp[1]))
                # print("模拟器大小是{}  x {}。".format(G.DEVICE.display_info["width"],G.DEVICE.display_info["height"]))
                # touch(temp)
                touch(i)
            # swipe(pos,vector = (100,0),duration = 0.3,steps = 1)
            continue

        if "准备完成" in name:
            # for i in moveMaps:
            for i in moveMaps1:
                temp = changeXY(i)
                touch(temp)
            touch(pos)
            continue

        if "结算OK".__eq__(name) | "按错取消".__eq__(name) | "前往大厅".__eq__(name) | "游玩".__eq__(name):
            touch(pos)
            break

        touch(pos)


#    升龙监控。
def autoBattleDragon():
    photoMap = air.Photo()
    photoMaps = [
        "升龙2",
    ]

    while exitFlag == 0:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        if "升龙2".__eq__(name):
            touch(pos)
            continue
        touch(pos)


#    退出战斗。
def autoBattleExit():
    photoMap = air.Photo()
    photoMaps = [
        "结算OK",
        "按错取消",
        "前往大厅",
        "重试",
    ]

    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        if "结算OK".__eq__(name) | "按错取消".__eq__(name) | "前往大厅".__eq__(name):
            touch(pos)
            break
        touch(pos)


# 绝对坐标转换，竖屏XY换成百分比
# 2023年1月2日16:38:42
# x换成横坐标的百分比然后给竖坐标，Y换成竖坐标百分比给横坐标。
def changeXY(pos):
    width = G.DEVICE.display_info["width"]
    height = G.DEVICE.display_info["height"]
    temp = (height * pos[0] / width, width * pos[1] / height)
    return temp


def missTest():
    photoMap = air.Photo()
    photoMaps = [
        "战斗中",
    ]
    moveMaps = [
        (370, 470),  # 0 第1张卡
        (520, 420),  # 1 第2张卡
        (680, 400),  # 2 第3张卡
        (850, 400),  # 3 第4张卡
        (130, 460),  # 主动
        (120, 377),  # 拉仇恨
        (99, 322),  # 点击队友
        # (919,461),
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        # print(G.DEVICE.display_info["orientation"])
        if "战斗中" in name:
            for i in moveMaps:
                # 竖屏和横屏的XY反过来。
                temp = changeXY(i)
                # print("原坐标:{},{},TEMP是{},{}。".format(i[0],i[1],temp[0],temp[1]))
                # print("模拟器大小是{}  x {}。".format(G.DEVICE.display_info["width"],G.DEVICE.display_info["height"]))
                touch(temp)
            swipe(pos, vector=(100, 0), duration=0.3, steps=1)
            continue


# 2023年1月3日20:47:40
# 自动PVP入口
def pvpAuto(time=0):
    photoMap = air.Photo()
    photoMaps = [
        "pvp入口",
        "pvp入口2",
        "pvp入口3",
        "pvp入口4",
        "pvp入口5",
        "pvp入口6",
        "寻宝入口",
        "标准规则",
        # "proud规则",
        "按错取消",
        "pvp读取2",
        "重试",
        "结算OK",
        "正在寻找对手",
        "准备完成",
        "准备完成2",
        "pvp读取",
        "pvp读取2",
        "主界面PVP",
    ]
    moveMaps = [
        (241, 342),
        (480, 342),
        (680, 349),
    ]
    moveMaps1 = [
        (721, 126),
        (721, 175),
        (721, 240),
        # (721, 300),
        # (721, 360),
        # (721, 420),
    ]
    moveMapsMuMu = [
        (398,230),
        (401,327),
        (390,441),
    ]
    moveMaps1 = moveMapsMuMu
    count = 0
    while (count < time) | (time == 0):
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "pvp读取" in name:
            autoBattleNext()
            count += 1
            print("第{}次战斗结束，返回大厅。".format(count))
            continue

        if "准备完成" in name:
            # for i in moveMaps:
            sleep(3)
            for i in moveMaps1:
                # temp = changeXY(i)
                # touch(temp)
                touch(i)
                sleep(0.3)
            touch(pos)
            continue

        touch(pos)

    backMain()


def autoGet7hour(eventName = "EX6"):
    photoMap = air.Photo()
    photoMaps = [
        eventName,
        # "EX6",
        # "EX5",
        "跳过卷开始2",
        "关卡标识",
        "特殊活动页",
        "原作重现",
        "原作重现2",
        "重现原作",
        # "活动特别",
        "活动入口2025",
        "菜单3",
    ]
    moveMaps = [
        (300, 250),  # 0 重现原作第一个。
        (670, 430),  # 1 跳过页面点“是”
        # (331,580),  # 2 地图型关卡最后的那关。
        (240, 580),  # 2 地图型关卡最后的那关。
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        if "特殊活动页".__eq__(name):
            # temp = changeXY(moveMaps[0])
            touch(moveMaps[0])
            continue

        if "原作重现" in name:
            touch(moveMaps[2])
            continue

        # 傻帽玩意判定小的一批。。
        if "关卡标识".__eq__(name):
            temp = (pos[0], pos[1] - 50)
            touch(temp)
            continue

        if "跳过卷开始2".__eq__(name):
            get10timesPve()
            backMain()
            break

        if "结算OK".__eq__(name):
            touch(pos)

        touch(pos)


# 2023年1月21日18:06:52 获取10次/点一次跳过最大
# 2024年5月13日 加个次数，默认点一次。
def get10timesPve(times=1):
    photoMap = air.Photo()
    photoMaps = [
        "结算OK",
        "跳过十次",
        "跳过卷开始2",
        # "活动特别",
        "活动",
        "菜单",
        "百层是",
    ]
    moveMaps = [
        # (670, 430),  # 0 跳过页面点“是”
        (385, 885),  # 0 跳过页面点“是”,新版UI
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "跳过十次".__eq__(name):
            touch(pos, times)
            # 2025年5月16日，换成MUMU的话不用转换。
            # temp = changeXY(moveMaps[0])
            touch(moveMaps[0])
            continue

        if "结算OK".__eq__(name):
            break

        touch(pos)


# 2023年1月21日17:57:26 回到主界面。
def backMain():
    photoMap = air.Photo()
    photoMaps = [
        "主界面PVP",
        "结算OK",
        "按错取消",
        "龙珠主页",
        "主界面PVP",
        "菜单",
        "菜单2",
        "菜单3",
    ]
    moveMaps = [

    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "龙珠主页".__eq__(name):
            touch(pos)
            continue

        # if "菜单".__eq__(name):
        #     break

        if "主界面PVP".__eq__(name):
            break

        touch(pos)


# 2023年1月21日17:57:18 获取委托。
def getMarch():
    photoMap = air.Photo()
    photoMaps = [
        "再次接受委托",
        "冒险2",
        "菜单",
        "菜单2",
        "菜单3",
        "冒险页内",
    ]
    moveMaps = [

    ]
    count = 0
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "龙珠主页".__eq__(name):
            touch(pos)
            continue

        if "再次接受委托".__eq__(name):
            touch(pos)
            backMain()
            break

        if "冒险页内".__eq__(name):
            count += 1
            if count > 10:
                backMain()
                break
            else:
                continue

        touch(pos)


# 2023年1月21日17:56:58 获取每日觉醒材料。
def getBonus():
    photoMap = air.Photo()
    photoMaps = [
        "红",
        "ZENKAI奖励",
        "奖励战斗",
        "推荐内容",
        "跳过卷开始",
        "推荐内容入口",
    ]
    colorMaps = [
        "红",  # 0
        "黄",  # 1
        "蓝",  # 2
        "紫",  # 3
        "绿",  # 4
    ]
    moveMaps = [
        (190,320), # 屏幕中央
    ]
    date = datetime.date.today().weekday() % 5
    photoMaps.insert(2, colorMaps[date])
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        print(pos)
        name = photoMap.name

        if ("红".__eq__(name)) & (date != 0):
            swipe(pos, vector=(0, -20), steps=2)
            continue

        if "推荐内容".__eq__(name):
            swipe(moveMaps[0], vector=(0, -20), steps=2)
            continue

        if "跳过卷开始".__eq__(name):
            get10timesPve(5)
            backMain()
            break

        touch(pos)

# 2025年5月16日，获取每日材料。
def getBonus2025():
    photoMap = air.Photo()
    photoMaps = [
        "跳过卷开始2",
        "奖励战斗索尼",
        "来场胜负",
        "活动入口2025",
        "强化入口",
    ]
    moveMaps = [
        (190,320), # 屏幕中央
    ]
    date = datetime.date.today().weekday() % 5
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        print(pos)
        name = photoMap.name

        if "来场胜负".__eq__(name):
            swipe(moveMaps[0], vector=(0, -0.65), steps=2)
            continue

        if "跳过卷开始2".__eq__(name):
            get10timesPve(2)
            backMain()
            break

        touch(pos)

# 超激斗 2023年1月31日19:04:06
def superBattle():
    photoMap = air.Photo()
    photoMaps = [
        "结算OK",
        "准备完成",
        "战斗开始",
        "战斗开始2",
        "超激斗能量",
        "战斗结束",
        "战斗中",
    ]
    moveMaps = [
        (241, 330),
        (480, 330),
        # (744, 349),
        (680, 330),
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "战斗中".__eq__(name):
            sleep(20)
            continue

        if "战斗开始" in name:
            changeBestTeam()
            touch(pos)
            continue

        if "准备完成".__eq__(name):
            for i in moveMaps:
                temp = changeXY(i)
                touch(temp)
                time.sleep(0.3)
            touch(pos)
            continue

        touch(pos)
        sleep(0.3)


# 自动换队 2023年1月31日19:17:14
def changeBestTeam():
    photoMap = air.Photo()
    photoMaps = [
        "百层是",
        "编组",
        "自动编组",
        "结算OK",
        "队伍标识",
        "战斗开始",
        "战斗开始2",
        "准备完成",
        "战斗结束",
    ]
    photoMapNext = [
        "百层是",
        "决定",
        "战斗开始",
        "战斗开始2",
        "准备完成",
        "战斗结束",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "百层是".__eq__(name):
            photoMaps = photoMapNext
            touch(pos)
            continue

        if ("战斗开始" in name) | "准备完成".__eq__(name):
            break

        touch(pos)
        sleep(0.3)


# 自动强化 2023年2月26日08:31:59
def autoZenkai():
    photoMap = air.Photo()
    photoMaps = [
        "觉醒强化完成",
        "百层是",
        "觉醒强化",
        "觉醒已选中",
        # "觉醒核心",
        "结算OK",
        "解放觉醒核心",
        "解放觉醒核心2",
    ]

    photoMapsNext = [
        "觉醒强化",
        "解放觉醒核心",
        "解放觉醒核心2",
        "结算OK",
    ]

    photoMapsTemp = [
    ]

    photoMapsTemp = photoMaps
    while 1:
        photoMap.loopSearch(photoMapsTemp, 0.2)
        pos = photoMap.pos
        name = photoMap.name

        if "觉醒已选中".__eq__(name):
            photoMapsTemp = photoMapsNext
            continue

        if "解放觉醒核心" in name:
            photoMapsTemp = photoMaps

        if "觉醒强化完成" in name:
            touch(pos)
            time.sleep(1)
            continue

        touch(pos)


# 自动购买活动物品 2023年2月26日11点38分
def autoBuyEvent():
    photoMap = air.Photo()
    photoMaps = [
        "跳过十次",
        "结算OK",
        "交换2",
        "交换",
    ]

    photoMapsNext = [
        "结算OK",
        "交换2",
        "交换",
        "跳过十次",
    ]

    photoMapsTemp = [
    ]
    photoMapsTemp = photoMaps
    count = 0
    while 1:
        photoMap.loopSearch(photoMapsTemp)
        pos = photoMap.pos
        name = photoMap.name

        if "跳过十次".__eq__(name):
            count += 1

        if count > 5:
            photoMapsTemp = photoMapsNext

        if "结算OK".__eq__(name):
            count = 0
            photoMapsTemp = photoMaps

        touch(pos)
        sleep(0.3)


def dailyAll():
    # getBonus() 旧的不用了。
    getBonus2025()
    autoGet7hour()
    backMain()
    getMarch()
    # 暂时出问题了，不用。
    pvpAuto(1)


# 自动钢镚 2023年3月4日12:37:32
def autoCoin():
    photoMap = air.Photo()
    photoMaps = [
        "结算OK",
        "交换十次",
        "交换10次",
        "交换十次2",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        touch(pos)
        sleep(0.3)


# 简单自动重开
# 2023年7月11日22:42:10
def autoStartEasy(times=0):
    photoMap = air.Photo()
    photoMaps = [
        "再次对战",
        "结算OK",
        "百层是",
        "继续跳过",
        "战斗中",
    ]
    i = 0;
    onlyOnce = 0;
    while i < times:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "战斗中".__eq__(name):
            sleep(10)
            touch(pos)
            onlyOnce = 0;
            continue

        if "继续跳过".__eq__(name):
            touch(pos)
            if onlyOnce == 0:
                i += 1;
                onlyOnce = 1;
            continue

        onlyOnce = 0;
        touch(pos)
        sleep(0.3)


# 简单自动转蛋
# 2023年7月11日22:42:10
def autoEgg():
    photoMap = air.Photo()
    photoMaps = [
        "连续转蛋",
        "扭蛋跳过",
        "百层是",
        "转蛋战斗力",
    ]
    i = 0;
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        touch(pos)


if __name__ == "__main__":
    # startRush()
    # autoRush()
    # auto100()
    # autoBattle(2)
    # autoBattleNext()
    # missTest()
    # pvpAuto()
    # autoGet7hour()
    # backMain()
    # getMarch()
    # autoBuyEvent()
    autoEgg()
    # getBonus2025()
    # getMarch()
    # pvpAuto(1)