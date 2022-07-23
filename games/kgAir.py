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
cv.set_value("path", cv.kgAirPath)
cv.set_value("device", cv.kgDevice)

flag = True

__author__ = "user"


def fullAutoKmx():
    count = 0
    photoMap = air.Photo()
    photoMaps = ['卡马逊主页']
    moveMaps = [
        (490, -373),  # 路线一 0
        (607, -320),  # 路线二 1
        (706, -272),  # 路线三 2
        (800, -222)  # 路线四 3
    ]
    while flag:
        photoMap.name = "默认"
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        if "卡马逊主页".__eq__(photoMap.name):
            for i in moveMaps:
                touchFix(pos, i)
            searchPage()
            # kmxAutoNew()
            if flag:
                count += 1
                # time.sleep(10)
                returnKmx()
    # 人物所在位置  394, 99


def returnKmx():
    photoMap = air.Photo()
    photoMaps = [
        "探险初始页",
        "卡马逊主页",
        "坎公主页面",
    ]
    moveMaps = [
        (-6, -467),  # 0 卡马逊主页 → 探险初始页
        (88, -189),  # 1 探险初始页 → 卡马逊主页
        (-834, 237),  # 2 主页面 → 探险初始页
    ]
    while True:
        photoMap = photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "卡马逊" in name:
            touchFix(pos, moveMaps[0])
            time.sleep(1)
            continue
        if "主页面" in name:
            touchFix(pos, moveMaps[2])
            continue
        if "初始" in name:
            touchFix(pos, moveMaps[1])
            break


def chooseEquip():
    equipMaps = [
        "坎公高阶神器",
        "坎公高阶神器",
        "坎公中阶神器",
        "坎公中阶神器2",
        "坎公低阶神器",
        "坎公获得银币",
    ]
    photoMaps = [
        "坎公卡马逊确认",
        "替换神器",
        "装备选择",
        "卡马逊主页",
    ]
    switch = 1
    while 1:
        photoMap = air.Photo()
        if switch == 1 :
            photoMap.loopSearch(equipMaps)
        elif switch == 2:
            photoMap.loopSearch(photoMaps)
        switch = 2
        pos = photoMap.pos
        name = photoMap.name
        if "替换" in name:
            changeEquip()
            break
        elif "主页" in name:
            break
        touch(pos)


def changeFlag():
    global flag
    flag = False


def touchFix(pos=(0, 0), pos1=(0, 0)):
    x = pos[0] + pos1[0]
    y = pos[1] + pos1[1]
    print("pos:{},pos1:{},新坐标：{}".format(pos, pos1, (x, y)))
    touch((x, y))
    time.sleep(0.3)


def changeEquip():
    photoMaps = [
        "处理装备",
        "坎公卡马逊确认",
        "装备选择",
        "替换神器",
        "卡马逊主页",
    ]
    moveMaps = [
        (486, 191),  # 第一个神器在的位置。
    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "替换神器" in name:
            pos = moveMaps[0]
        if "主页" in name:
            break
        touch(pos)

def searchPage():
    photoMaps = [
        "战斗页",
        "坎公心号",
        "坎公商店",
        # "问号标识一",
        "坎公战队",
        # "问号标识二",
        # "问号标识三",
        "事件标识",
        "卡马逊主页",
    ]
    moveMaps = [
        (486, 191),  # 第一个神器在的位置。
    ]
    global flag
    while flag:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "战斗" in name:
            battle()
            break
        if "心号" in name:
            heart()
            break
        if "事件" in name:
            question()
            break
        if "商店" in name:
            shop()
            break
        if "战队" in name:
            team()
            break
        if "主页" in name:
            break


def battle():
    photoMaps = [
        "战斗进入",
        "坎公卡马逊确认",
        "坎公装备页",
        "挑战成功",
    ]
    moveMaps = [
        (486, 191),  # 第一个神器在的位置。
    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        touch(pos)
        if "进入" in name:
            time.sleep(30)
        if "装备" in name:
            chooseEquip()
            break
        if "成功" in name:
            global flag
            flag = False
            break

def heart():
    photoMaps = [
        "坎公卡马逊确认",
        "坎公心号",
        "卡马逊主页",
    ]
    moveMaps = [
        (750,250),  # 回血。
        (450,250),  # 解诅咒。
        (150,250),  # 复活。
    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "心号" in name:
            for i in moveMaps:
                touchFix(i)
            photoMaps.insert(0,"装备选择")
        if "主页" in name:
            break
        touch(pos)

def shop():
    photoMaps = [
        "装备选择",
        "坎公卡马逊确认",
        "商店退出",
        "坎公商店",
        "卡马逊主页",
    ]
    moveMaps = [

    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "主页" in name:
            break
        touch(pos)

def question():
    photoMaps = [
        "战斗进入",  # 用来容错。
        "坎公卡马逊确认",
        "装备选择",
        "问号标识一",
        "问号标识二",
        "卡马逊主页",
    ]
    moveMaps = [

    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "主页" in name:
            break
        if "选择" in name:
            photoMaps.remove("问号标识一")
            photoMaps.remove("问号标识二")
        touch(pos)

def team():
    photoMaps = [
        "坎公卡马逊确认",
        "装备选择",
        "坎公战队",
        "卡马逊主页",
    ]
    moveMaps = [
        (780,360), # 开始滑动的坐标。
        (780,30), # 结束滑动的坐标。
    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "主页" in name:
            break
        if "战队" in name:
            swipe(moveMaps[0],moveMaps[1],duration = 1 , steps = 6)
            photoMaps.remove("坎公战队")
            photoMaps.append("问号标识二")
            continue
        touch(pos)

def pvpAuto():
    gamePages = air.Photo()
    gamePagesMap = [
        '坎公挑战卷不足',
        '坎公44段位更新',
        '坎公PVP确认',
        '坎公初始选人页黄',
        '坎公PVP休息',
        '坎公初始选人页重试',
        '坎公卡马逊确认'
    ]
    moveMaps = [
        (903,171),  # 重试右上角的小齿轮
    ]
    global flag
    flag = True
    while flag:
        gamePages.name = "默认"
        gamePages.loopSearch(gamePagesMap)
        name = gamePages.name
        pos = gamePages.pos
        if "坎公初始选人页重试".__eq__(name):
            # 拿偏移坐标，点一下右上角齿轮在的位置收工。
            touchFix(moveMaps[0])
            touch(pos)
        elif '坎公PVP休息'.__eq__(name):
            time.sleep(20)
        elif "不足" in name:
            touchFix(pos,(-28,154))
            changeFlag()
        elif '更新' in name:
            touchFix(pos,(3,227))
        # 这里拿到了上面三选一的 名字 和XY坐标
        else:
            touch(pos)

def levelStone():
    photoMap = air.Photo()
    photoMaps = [
        '坎公PVP确认',
        '坎公卡马逊确认',
        '自动战斗完毕',
        '进化石扫荡',
        '进化石页面',
    ]
    moveMaps = [
        (601,266), # 点扫荡前先把进度条拉到最大。
    ]
    while True:
        photoMap.name = "默认"
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "扫荡" in name:
            touch(moveMaps[0])
        if "完毕" in name:
            break
        touch(pos)



if __name__ == "__main__":
    # touchFix((3,4),(5,6))
    # returnKmx()
    # chooseEquip()
    # question()
    # shop()
    # fullAutoKmx()
    # searchPage()
    # team()
    pvpAuto()
    # levelStone()