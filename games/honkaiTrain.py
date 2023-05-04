import pyautogui as py
import time
import random

from dao import dao, daoImpl, multiphotos, resultMap
from dao import changeVar as cv
import _thread

cv._init()
cv.set_value("path", cv.trainPath)


def openGame():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "星铁开始游戏",
        "星铁开始图标",
    ]
    photoMapsNext = [
        "星铁进入游戏后标识",
        "星铁点击进入",
        "星铁开始游戏",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "开始图标" in name:
            dao.moveTo2(x, y)
            continue

        if "开始游戏" in name:
            dao.moveTo(x, y)
            photoMaps = photoMapsNext
            continue

        if "进入游戏后" in name:
            break

        dao.moveTo(x, y)


def getMission():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "星铁获得物品",
        "星铁任务盒子",
        "星铁活跃度已满",
        "星铁任务领取",
        "星铁任务图标",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "任务图标" in name:
            dao.moveToWithKey(x, y, 'altleft')
            continue

        if "活跃度已满" in name:
            backToMain()
            break

        dao.moveTo(x, y)

def backToMain():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "星铁页面关闭",
        "星铁任务图标",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "任务图标" in name:
            break

        dao.moveTo(x, y)

if __name__ == '__main__':
    # openGame()
    getMission()
