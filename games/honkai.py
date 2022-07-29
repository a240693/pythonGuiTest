import _thread
import time
from dao import multiphotos as mp
from dao import dao
from dao import changeVar as cv

# 这个注销是从airTest切换成pyautoGui
from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
# from dao import airMultiPhotos as air
import logging
# 日志只输出INFO等级，debugger等级不输出。
# logger = logging.getLogger("airtest")
# logger.setLevel(logging.INFO)
# def airInit():
#     cv._init()
#     cv.set_value("path", cv.honkaiPath)
#     cv.set_value("device", cv.honkai)

def init():
    cv._init()
    cv.set_value("path", cv.honkaiPath)
    cv.set_value("device", cv.honkai)

def selectPages():
    photoMap = mp.Photo()
    photoMaps = [
        "远征",
        "家园",
        "打工",
    ]
    while True:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        dao.moveTo(x,y)

def home():
    photoMap = mp.Photo()
    photoMaps = [
        "体力取完",
        "体力",
        "体力2",
        "金币",
        "取出体力",
        # "远征",
        # "打工",
    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        x = photoMap.x
        y = photoMap.y
        if "取完" in name:
            break
        dao.moveTo(x,y)

if __name__ == "__main__":
    # selectPages()
    init()
    home()