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
tempDevice = cv.blueDevice # 办公室
# tempDevice = cv.kgDevice # 家

cv.set_value("path", cv.bluePath)
cv.set_value("device", tempDevice)

flag = True

__author__ = "user"


def autoStart():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "跳过",
        "自动",
        "确认二",
        "确认",
        "出击",
        '开始任务',
        '开始任务二',
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "自动".__eq__(name):
            time.sleep(30)
            continue

        touch(pos)



if __name__ == "__main__":
    autoStart()
