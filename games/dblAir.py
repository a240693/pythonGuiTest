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
cv.set_value("path", cv.DBLPath)
# cv.set_value("device", cv.DBLdevice)
cv.set_value("device", cv.DBLdeviceHome)
flag = True

__author__ = "user"

def cvInit():
    cv._init()
    cv.set_value("path", cv.DBLPath)
    # cv.set_value("device", cv.kgDevice3)
    # cv.set_value("device", cv.DBLdevice)
    cv.set_value("device", cv.DBLdeviceHome)

# RUSH入口
# 2023年1月2日16:37:59
def autoRush():
    photoMap = air.Photo()
    photoMaps = [
        "编组",
        "自动编组",
        "结算OK",
        "战斗结束",
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

        if "结算OK".__eq__(name) :
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
            sleep(20)
            continue
        touch(pos)
        sleep(0.3)

# 2023年1月2日16:37:18
# 自动团队战入口
def autoBattle():
    photoMap = air.Photo()
    photoMaps = [
        "战斗开始",
        "结算OK",
        "寻找",
        "准备完成",
        "按错取消",
        "前往大厅",
        "读取中",
        "寻找",
        "准备完成",
        "重试",
    ]
    moveMaps = [
        (),
    ]
    count = 0
    while 1:
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
        "结算OK",
        "升龙",
        "升龙2",
        "按错取消",
        "前往大厅",
        "重试",
        "战斗中",
        "战斗开始",
    ]
    moveMaps = [
        (370,470), # 0 第1张卡
        (520,420), # 1 第2张卡
        (680,400), # 2 第3张卡
        (850,400), # 3 第4张卡
        (130,460), # 主动
        (120,377), # 拉仇恨
        (99,322), #点击队友
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
            swipe(pos,vector = (100,0),duration = 0.3,steps = 1)
            continue

        if "升龙".__eq__(name):
            sleep(1)
            touch(pos)
            continue

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

if __name__ == "__main__":
    # startRush()
    # autoRush()
    # auto100()
    autoBattle()
    # autoBattleNext()