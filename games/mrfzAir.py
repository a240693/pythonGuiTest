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
# tempDevice = cv.mrfzDeviceOffice # 办公室
tempDevice = cv.mrfzDevice  # 家

cv.set_value("path", cv.mrfzPath)
cv.set_value("device", tempDevice)

flag = True

__author__ = "user"


def autoEnter():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        '捕猎区',
        '资源区',
        '今日日报',
        '演算开始',
        '全队补充',
        '开始演算',
        '选择干员',
    ]
    moveMaps = [
        (490, -373),  # 路线一 0
        (607, -320),  # 路线二 1
        (706, -272),  # 路线三 2
        (800, -222)  # 路线四 3
    ]
    while flag:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        touch(pos)


def autoStart(time=0):
    photoMap = air.Photo()
    photoMaps = [
        '结算信赖提升',
        "开始行动",
        "开始行动2",
        "剿灭结束标识一",
        "剿灭结束标识二",
        "作战中",
    ]
    moveMaps = [

    ]
    count = 0
    startFlag = False
    while (count < time) | (time == 0):
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "作战中".__eq__(name):
            startFlag = True
            sleep(20)
            continue

        if ("结算信赖提升".__eq__(name) & (startFlag == True)):
            count += 1
            print("作战结束，完成第{}次,开始第{}次。".format(count, count + 1))
            startFlag = False
            continue

        if "剿灭结束标识二".__eq__(name) & (startFlag == True):
            count += 1
            print("剿灭结束，完成第{}次,开始第{}次。".format(count, count + 1))
            startFlag = False
            continue

        touch(pos)


if __name__ == "__main__":
    # autoEnter()
    autoStart(5)
