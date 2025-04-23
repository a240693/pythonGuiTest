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
cv.set_value("path", cv.SDPath)
cv.set_value("device", cv.SDdevice)
# cv.set_value("device", cv.DBLdeviceHome)
flag = True

__author__ = "user"
exitFlag = 0


def cvInit(path=cv.SDPath, device=cv.SDdevice):
    cv._init()
    cv.set_value("path", path)
    cv.set_value("device", device)


# RUSH入口半自动试做 2025年4月23日
def autoRush():
    photoMap = air.Photo()
    photoMaps = [
        "继续",
        "再次出击",
        "Tap",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        touch(pos)
        sleep(0.3)

# 半自动拉满，2025年4月23日
def autoMaxSelect():
    photoMap = air.Photo()
    photoMaps = [
        "OK",
        "执行",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        touch(pos)
        sleep(0.3)

if __name__ == "__main__":
    # autoRush()
    autoMaxSelect()
