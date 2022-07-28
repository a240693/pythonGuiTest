import _thread
import time

from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from dao import airMultiPhotos as air
from dao import changeVar as cv
import logging

# 日志只输出INFO等级，debugger等级不输出。
# logger = logging.getLogger("airtest")
# logger.setLevel(logging.INFO)

cv._init()
cv.set_value("path", cv.honkaiPath)
cv.set_value("device", cv.honkai)

def selectPages():
    photoMap = air.Photo()
    photoMaps = [
        "远征",
        "家园",
        "打工",
    ]
    while True:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        touch(pos)

if __name__ == "__main__":
    selectPages()