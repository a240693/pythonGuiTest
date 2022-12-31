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
cv.set_value("device", cv.DBLdevice)

flag = True

__author__ = "user"

def cvInit():
    cv._init()
    cv.set_value("path", cv.DBLPath)
    # cv.set_value("device", cv.kgDevice3)
    cv.set_value("device", cv.DBLdevice)

def autoRush():
    photoMap = air.Photo()
    photoMaps = [
        "编组",
        "自动编组",
        "结算OK",
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
        "战斗开始",
        "结算OK",
        "战斗结束",
        "战斗中",
        "点数报酬",
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
            break

        touch(pos)
        sleep(0.3)

if __name__ == "__main__":
    # startRush()
    autoRush()