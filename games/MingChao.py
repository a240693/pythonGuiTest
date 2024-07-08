import pyautogui as py
import time
import random

from dao import dao, daoImpl, multiphotos, resultMap
from dao import changeVar as cv
import _thread

cv._init()
cv.set_value("path", cv.MingChaoPath)


# 自动剧情。
def autoText():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "LV主界面标识",
        "推进选项",
        "对话选项",
        "F键",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if name.__eq__("F键"):
            dao.pressKey("F")
            continue

        if name.__eq__("对话选项"):
            dao.pressKey("F")
            continue

        if name.__eq__("LV主界面标识"):
            break

        dao.moveTo(x, y)



if __name__ == '__main__':
    # dailyBussiness()
    # dailyAll()
    # dailyMission()
    # dailyGood()
    # dailySendPeople()
    # dailyBussiness()
    # dailyMonthCard()
    # dailyBonus()
    # openGame()
    # dailySendPeople1024()
    # dailyBussiness1024()
    autoText()