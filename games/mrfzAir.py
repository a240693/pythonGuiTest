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
tempDevice = cv.mrfzDeviceHome # 家

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

if __name__ == "__main__":
    autoEnter()
