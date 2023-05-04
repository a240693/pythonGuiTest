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
cv.set_value("path", cv.pcrAirPath)
cv.set_value("device", cv.pcrAirDevice)
flag = True

__author__ = "user"


def cvInit(path=cv.pcrAirPath, device=cv.pcrAirDevice):
    cv._init()
    cv.set_value("path", path)
    cv.set_value("device", device)
    # cv.set_value("device", cv.DBLdeviceHome)


# 自动推图
# 2023年5月4日23:19:36
def autoFight():
    photoMap = air.Photo()
    photoMaps = [
        "地图已攻略",
        "关卡未攻略",
        "关卡已攻略",
        "战斗开始",
        "主页",
    ]
    startMaps = [
        (127,251), # 0,45图初始
        (205, 307),  # 1,45图困难
    ]
    moveMaps = [
        (930,270), # 0 ,关卡已攻略，下一张。
        (840, 450),  # 1 ,关卡未攻略，开始挑战。
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "主页".__eq__(name):
            for i in startMaps:
                touch(i)
            continue

        if "关卡已攻略".__eq__(name):
            touch(moveMaps[0])
            continue

        if "关卡未攻略".__eq__(name):
            touch(moveMaps[1])
            continue

        if "战斗开始".__eq__(name):
            startBattle()
            continue

        touch(pos)
        sleep(0.3)

def startBattle():
    photoMap = air.Photo()
    photoMaps = [
        "pcr对话框一",
        "主页",
        "关闭",
        "下一步",
        "战斗标识1",
        "战斗开始",
        "取消",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "战斗标识1".__eq__(name):
            sleep(10)
            continue

        if "主页".__eq__(name):
            break

        touch(pos)
        sleep(0.3)

if __name__ == "__main__":
    # startBattle()
    autoFight()

