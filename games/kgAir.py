# emulator-5560
import _thread
import time

from airtest.core.api import *
from dao import airMultiPhotos as air
from dao import changeVar as cv
import logging

# 日志只输出INFO等级，debugger等级不输出。
logger = logging.getLogger("airtest")
logger.setLevel(logging.INFO)

cv._init()
cv.set_value("path", cv.path)
cv.set_value("device", cv.kgDevice)

spaceFlag = False

flag = True

continueFlag = False

__author__ = "user"


def fullAutoKmx():
    count = 0
    photoMap = air.Photo()
    photoMaps = ['卡马逊主页']
    moveMaps = [
        (490, -373),  # 路线一 0
        (607, -320),  # 路线二 1
        (706, -272),  # 路线三 2
        (800, -222)  # 路线四 3
    ]
    while flag:
        photoMap.name = "默认"
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        if "卡马逊主页".__eq__(photoMap.name):
            for i in moveMaps:
                touchFix(pos , i)
            kmxAutoNew()
            if flag:
                count += 1
                # time.sleep(10)
                returnKmx()
    # 人物所在位置  394, 99


def returnKmx():
    # 退出 -52, -465
    # 返回 127, -170
    # photoMap = []
    # photoMap.append(('卡马逊主页', 1, -6, -467))
    # photoMap.append(('探险初始页', 1, 88, -189))
    # dao.dualListPhotoKg(photoMap)
    photoMap = air.Photo()
    photoMaps = [
        "卡马逊主页",
        "探险初始页",
        "坎公主页面",
    ]
    moveMaps = [
        (-6, -467),  # 0 卡马逊主页 → 探险初始页
        (88, -189),  # 1 探险初始页 → 卡马逊主页
        (-834, 237),  # 2 主页面 → 探险初始页
    ]
    while True:
        photoMap = photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "卡马逊" in name:
            touchFix(pos , moveMaps[0])
            time.sleep(1)
            continue
        if "主页面 " in name:
            touchFix(pos , moveMaps[2])
            continue
        if "初始" in name:
            touchFix(pos , moveMaps[1])
            break


def kmxAutoNew():
    count = 0
    gamePages = air.Photo()
    gamePagesMap = [
        '卡马逊黄',
        '坎公卡马逊确认',
        '坎公问号',
        '坎公卡马逊灯泡',
        '坎公泰坦战队',
        '坎公休息区',
        '坎公特惠促销',
        # '坎公保存神器',
        '坎公装备取消',
        '卡马逊商店',
        '坎公装备页',
        '卡马逊主页'
    ]
    # 坎公卡马逊选择 暂时用不上。
    moveMaps = [
        (66, 147),  # 坎公问号  0
        (0, 36),  # 坎公问号2   1
        (423, 154),  # 坎公问号3 2
        (280, -240), #  休息区  3
        (89, -195),  # 休息区  4
        (-149, -225),  # 休息区 5
        (196, 2),  # 休息区 6
        (277,109), # 坎公装备取消 7
        (493, 369),  # 坎公装备取消 8
        (-3,127), # 保存神器 9
        (132, 371),  # 保存神器 10
    ]
    while flag:
        gamePages.name = "默认"
        gamePages.loopSearch(gamePagesMap)
        count += 1
        pos = gamePages.pos
        if "卡马逊主页".__eq__(gamePages.name):
            # 如果检测到了卡马逊主页就直接退出。
            if (count > 4):
                break
            else:
                continue
        elif "坎公问号".__eq__(gamePages.name):
            touchFix(pos , moveMaps[0])
            touchFix(pos , moveMaps[1])
            touchFix(pos , moveMaps[2])
            continue
        elif "坎公休息区".__eq__(gamePages.name):
            # 先点回血，再点净化再点复活，复活优先。
            touchFix(pos,moveMaps[3])
            touchFix(pos,moveMaps[4])
            touchFix(pos, moveMaps[5])
            touchFix(pos, moveMaps[6])
            continue
        elif "坎公装备取消".__eq__(gamePages.name):
            touchFix(pos, moveMaps[7])
            time.sleep(1)
            touchFix(pos, moveMaps[8])
            continue
        # 还没空整拖动。
        # elif ("战队" in gamePages.name) | ("促销" in gamePages.name):
        #     dao.scrollKg(x + 134, y + 293)
        #     continue
        elif "坎公装备页".__eq__(gamePages.name):
            chooseEquip()
            # touch(gamePages.x + 137, gamePages.y + -206, 1)
            continue
        elif "保存神器" in gamePages.name:
            touchFix(pos,moveMaps[9])
            touchFix(pos, moveMaps[10])
            # touch(gamePages.x + 137, gamePages.y + -206, 1)
            changeFlag()
            break
        else:
            # 这里拿到了上面三选一的 名字 和XY坐标
            touch(pos)
        if (count == 1) & ("黄" in gamePages.name):
            time.sleep(6)
        elif count > 15:
            changeFlag()


def kmxAutoNewV2():
    count = 0
    gamePages = air.Photo()
    gamePagesMap = [
        '卡马逊黄',
        '坎公卡马逊确认',
        '坎公问号',
        '坎公卡马逊灯泡',
        '坎公泰坦战队',
        '坎公休息区',
        '坎公特惠促销',
        # '坎公保存神器',
        '坎公装备取消',
        '卡马逊商店',
        '坎公装备页',
        '卡马逊主页'
    ]
    # 坎公卡马逊选择 暂时用不上。
    moveMaps = [
        (66, 147),  # 坎公问号  0
        (0, 36),  # 坎公问号2   1
        (423, 154),  # 坎公问号3 2
        (280, -240), #  休息区  3
        (89, -195),  # 休息区  4
        (-149, -225),  # 休息区 5
        (196, 2),  # 休息区 6
        (277,109), # 坎公装备取消 7
        (493, 369),  # 坎公装备取消 8
        (-3,127), # 保存神器 9
        (132, 371),  # 保存神器 10
    ]
    while flag:
        gamePages.name = "默认"
        gamePages.loopSearch(gamePagesMap)
        count += 1
        pos = gamePages.pos
        if "卡马逊主页".__eq__(gamePages.name):
            # 如果检测到了卡马逊主页就直接退出。
            if (count > 4):
                break
            else:
                continue
        elif "坎公问号".__eq__(gamePages.name):
            touchFix(pos , moveMaps[0])
            touchFix(pos , moveMaps[1])
            touchFix(pos , moveMaps[2])
            continue
        elif "坎公休息区".__eq__(gamePages.name):
            # 先点回血，再点净化再点复活，复活优先。
            touchFix(pos,moveMaps[3])
            touchFix(pos,moveMaps[4])
            touchFix(pos, moveMaps[5])
            touchFix(pos, moveMaps[6])
            continue
        elif "坎公装备取消".__eq__(gamePages.name):
            touchFix(pos, moveMaps[7])
            time.sleep(1)
            touchFix(pos, moveMaps[8])
            continue
        # 还没空整拖动。
        # elif ("战队" in gamePages.name) | ("促销" in gamePages.name):
        #     dao.scrollKg(x + 134, y + 293)
        #     continue
        elif "坎公装备页".__eq__(gamePages.name):
            chooseEquip()
            # touch(gamePages.x + 137, gamePages.y + -206, 1)
            continue
        elif "保存神器" in gamePages.name:
            touchFix(pos,moveMaps[9])
            touchFix(pos, moveMaps[10])
            # touch(gamePages.x + 137, gamePages.y + -206, 1)
            changeFlag()
            break
        else:
            # 这里拿到了上面三选一的 名字 和XY坐标
            touch(pos)
        if (count == 1) & ("黄" in gamePages.name):
            time.sleep(6)
        elif count > 15:
            changeFlag()

def chooseEquip():
    equipMaps = [
        "坎公卡马逊确认",
        "坎公高阶神器",
        "坎公高阶神器",
        "坎公中阶神器",
        "坎公中阶神器2",
        "坎公低阶神器",
        "坎公获得银币",
    ]

    photoMap = air.Photo()
    photoMap.loopSearch(equipMaps)
    pos = photoMap.pos
    touch(pos)


def changeFlag():
    global flag
    flag = False

def touchFix(pos = (0,0),pos1 = (0,0)):
    print("pos:{},pos1:{}".format(pos,pos1))
    x = pos[0] + pos1[0]
    y = pos[1] + pos1[1]
    touch((x,y))


if __name__ == "__main__":
    # touchFix((3,4),(5,6))
    # fullAutoKmx()
    kmxAutoNew()