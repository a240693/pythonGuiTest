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
        "编组",
        "结算OK",
        "战斗开始",
        "战斗结束",
        "战斗中",
        "点数报酬",
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


def autoBattleNext():
    photoMap = air.Photo()
    photoMaps = [
        "升龙2",
        "结算OK",
        "升龙2",
        "按错取消",
        "前往大厅",
        "游玩",
        "重试",
        "升龙2",
        "升龙2",
        "继续战斗",
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

    while 1:
        photoMap.loopSearch(photoMaps, time=0.3)
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
            # swipe(pos,vector = (100,0),duration = 0.3,steps = 1)
            continue

        if "升龙".__eq__(name):
            sleep(1)
            touch(pos)
            continue

        if "结算OK".__eq__(name) | "按错取消".__eq__(name) | "前往大厅".__eq__(name) | "游玩".__eq__(name):
            touch(pos)
            break

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
        "按错取消",
        "重试",
        "结算OK",
        "准备完成",
        "pvp读取",
        "主界面PVP",
    ]
    moveMaps = [
        (241, 342),
        (480, 342),
        (680, 349),
    ]
    count = 0
    while (count < time) | (time == 0):
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "pvp读取".__eq__(name):
            autoBattleNext()
            count += 1
            print("第{}次战斗结束，返回大厅。".format(count))
            continue

        if "准备完成".__eq__(name):
            for i in moveMaps:
                temp = changeXY(i)
                touch(temp)
            touch(pos)
            continue

        touch(pos)

    backMain()


def autoGet7hour():
    photoMap = air.Photo()
    photoMaps = [
        "跳过卷开始",
        "关卡标识",
        "特殊活动页",
        "重现原作",
        # "活动特别",
        "活动",
        "菜单",
    ]
    moveMaps = [
        (300, 250),  # 0 重现原作第一个。
        (670, 430),  # 1 跳过页面点“是”
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        if "特殊活动页".__eq__(name):
            temp = changeXY(moveMaps[0])
            touch(temp)
            continue

        # 傻帽玩意判定小的一批。。
        if "关卡标识".__eq__(name):
            temp = (pos[0], pos[1] - 50)
            touch(temp)
            continue

        if "跳过卷开始".__eq__(name):
            get10timesPve()
            backMain()
            break

        if "结算OK".__eq__(name):
            touch(pos)

        touch(pos)


# 2023年1月21日18:06:52 获取10次/点一次跳过最大
def get10timesPve():
    photoMap = air.Photo()
    photoMaps = [
        "结算OK",
        "跳过十次",
        "跳过卷开始",
        # "活动特别",
        "活动",
        "菜单",
    ]
    moveMaps = [
        (670, 430),  # 0 跳过页面点“是”
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "跳过十次".__eq__(name):
            touch(pos)
            temp = changeXY(moveMaps[0])
            touch(temp)
            continue

        if "结算OK".__eq__(name):
            break

        touch(pos)


# 2023年1月21日17:57:26 回到主界面。
def backMain():
    photoMap = air.Photo()
    photoMaps = [
        "主界面PVP",
        "按错取消",
        "结算OK",
        "龙珠主页",
        "主界面PVP",
        "菜单",
        "菜单2",
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
        "冒险",
        "菜单",
        "菜单2",
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
        "ZENKAI奖励",
        "推荐内容",
        "红",
        "跳过卷开始",
    ]
    colorMaps = [
        "红", # 0
        "黄", # 1
        "蓝", # 2
        "紫", # 3
        "绿", # 4
    ]
    moveMaps = [

    ]
    date = datetime.date.today().weekday() % 5
    photoMaps.insert(2,colorMaps[date])
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        print(pos)
        name = photoMap.name

        if ("红".__eq__(name)) & (date != 0):
            swipe(pos, vector=(0, -20), steps=2)
            continue

        if  "跳过卷开始".__eq__(name):
            get10timesPve()
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

        if "战斗开始".__eq__(name):
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

#自动换队 2023年1月31日19:17:14
def changeBestTeam():
    photoMap = air.Photo()
    photoMaps = [
        "百层是",
        "编组",
        "自动编组",
        "结算OK",
        "队伍标识",
        "战斗开始",
        "准备完成",
        "战斗结束",
    ]
    photoMapNext = [
        "百层是",
        "决定",
        "战斗开始",
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

        if "战斗开始".__eq__(name) | "准备完成".__eq__(name):
            break

        touch(pos)
        sleep(0.3)

#自动强化 2023年2月26日08:31:59
def autoZenkai():
    photoMap = air.Photo()
    photoMaps = [
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
        photoMap.loopSearch(photoMapsTemp)
        pos = photoMap.pos
        name = photoMap.name

        if "觉醒已选中".__eq__(name):
            photoMapsTemp = photoMapsNext
            continue

        if "解放觉醒核心" in name:
            photoMapsTemp = photoMaps

        touch(pos)
        sleep(0.3)

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

        if count > 5 :
            photoMapsTemp = photoMapsNext

        if "结算OK".__eq__(name):
            count = 0
            photoMapsTemp = photoMaps

        touch(pos)
        sleep(0.3)

def dailyAll():
    getBonus()
    autoGet7hour()
    backMain()
    getMarch()
    pvpAuto(1)

#自动钢镚 2023年3月4日12:37:32
def autoCoin():
    photoMap = air.Photo()
    photoMaps = [
        "交换十次",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        touch(pos)
        sleep(0.3)


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
    autoCoin()

