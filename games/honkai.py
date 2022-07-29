import _thread
import time
from dao import changeVar as cv

# pyautogui没法点击
# from dao import multiphotos as mp
# from dao import dao

# 这个注销是从airTest切换成pyautoGui
from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import logging
from dao import airMultiPhotos as air
# 日志只输出INFO等级，debugger等级不输出。
logger = logging.getLogger("airtest")
logger.setLevel(logging.INFO)
def airInit():
    cv._init()
    cv.set_value("path", cv.honkaiPath)
    cv.set_value("device", cv.honkai)

def init():
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

def home():
    photoMap = air.Photo()
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
        pos = photoMap.pos
        if "取完" in name:
            break
        touch(pos)

def touchFix(pos=(0, 0), pos1=(0, 0)):
    x = pos[0] + pos1[0]
    y = pos[1] + pos1[1]
    print("pos:{},pos1:{},新坐标：{}".format(pos, pos1, (x, y)))
    touch((x, y))
    time.sleep(0.3)

if __name__ == "__main__":
    # selectPages()
    init()
    home()