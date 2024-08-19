import pyautogui as py
import time
import random

from dao import dao, daoImpl, multiphotos, resultMap
from dao import changeVar as cv
import _thread

cv._init()
cv.set_value("path", cv.cbjqPath)


def openGame():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "尘白开始游戏",
        "尘白游戏图标",
    ]
    photoMapsNext = [
        "尘白进场模糊抽奖",
        "尘白模糊共鸣",
        "尘白取消",
        "获得道具",
        "尘白进入游戏后",
        "16提示",
    ]
    while 1:
        # photoMap.loopSearch(photoMapsNext)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "游戏图标" in name:
            dao.moveTo2(x, y)
            continue

        if "开始游戏" in name:
            dao.moveTo(x, y)
            photoMaps = photoMapsNext
            continue

        if "进入游戏后" in name:
            break

        if "16提示" in name:
            dao.moveTo(x + 100, y)
            continue

        dao.moveTo(x, y)


# 获取好友点数。
# 2024年4月19日22:10:40
def getFriend():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "已赠送感知",
        "尘白一键收赠",
        "尘白好友",
        "赠送感知",
        "完成标识1",
        "完成标识2",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "已赠送感知" in name:
            backToMain()
            break

        dao.moveTo(x, y)


def backToMain():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "尘白对话框取消",
        "获得道具",
        "尘白进入游戏后",
        "尘白主页",
        "尘白后退",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "尘白进入游戏后" in name:
            break

        dao.moveTo(x, y)


# 购买日常补给箱 2024年4月19日22:33:26
def dailyFree():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "物资箱已购买",
        "获得道具",
        "尘白购买",
        "每日物资配给箱",
        "尘白供应站",
        "尘白补给箱",
        "日常补给箱",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "获得道具" in name:
            dao.moveTo(x, y)
            backToMain()
            break

        if "物资箱已购买".__eq__(name):
            backToMain()
            break

        if "日常补给箱".__eq__(name):
            dao.pressKey('pagedown')
            continue

        dao.moveTo(x, y)


# 日常碎片角色前置 2024年4月19日22:41:00
def dailyCharacterPre():
    characterMaps = [
        "尘白琴诺",
        "尘白芬妮",
    ]
    # 嵌套循环，每个角色走一遍。
    for i in characterMaps:
        dailyCharacter(i)


# 日常碎片 2024年4月19日22:41:00
def dailyCharacter(character):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "尘白速战",
        "尘白行为02",
        "尘白个人故事",
        "尘白战斗2",
        "尘白战斗",
    ]
    photoMaps.insert(0, character)
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "尘白速战" in name:
            autoBattle()
            break

        dao.moveTo(x, y)


# 自动速战开始 2024年4月19日23:00:18
def autoBattle():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "尘白关卡次数限制",
        "尘白最大",
        "尘白速战",
    ]
    photoMapsNext = [
        "尘白完成",
        "尘白开始作战",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        # photoMap.loopSearch(photoMapsNext)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "尘白最大" in name:
            dao.moveToPcr(x, y, 3)
            photoMaps = photoMapsNext
            continue

        if "尘白关卡次数限制" in name:
            backToMain()
            break

        if "尘白完成" in name:
            dao.moveTo(x, y)
            backToMain()
            break

        dao.moveTo(x, y)


# 自动获取任务 2024年4月19日23:17:37
def dailyMission():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "获得道具",
        "尘白等级提升",
        "尘白一键领取",
        "尘白任务",
        "尘白任务2",
        "日常已完成部分",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "获得道具" in name:
            dao.moveTo(x, y)
            backToMain()
            break

        if "日常已完成部分" in name:
            backToMain()
            break

        dao.moveTo(x, y)


# 自动获取战令任务 2024年4月19日23:17:37
def dailyWarOrder():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "获得道具",
        "尘白战令一键领取",
        "尘白每日任务",
        "尘白每日任务1",
        "尘白战令",
        "尘白战令2",
        "尘白战令已领取",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "获得道具" in name:
            dao.moveTo(x, y)
            backToMain()
            break

        if "尘白战令已领取" in name:
            backToMain()
            break

        dao.moveTo(x, y)


# 自动购买 2024年4月19日23:17:37
def dailyShop():
    photoMap = multiphotos.Photo()
    photoMaps = [


        "购买页标识",
        "尘白商店",
        "尘白商店2",
        "蓝色塑料",
        "光纤轴突",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "获得道具" in name:
            dao.moveTo(x, y)
            backToMain()
            break

        if ("购买页标识" in name):
            dailyShopNext()
            break

        dao.moveTo(x, y)


def dailyShopNext():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "已选择最大数量",
        "购买最大",
    ]
    photoMapsNext = [
        "购买",
        "获得道具",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "获得道具" in name:
            dao.moveTo(x, y)
            backToMain()
            break

        if "已选择最大数量" in name:
            photoMaps = photoMapsNext
            continue

        dao.moveTo(x, y)

def dailyEvent(eventName = "空都演绎"):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "速战",
        "最高难度",
        "材料",
        "入口",
    ]

    for i in range(photoMaps.__len__()):
        photoMaps[i] = eventName + photoMaps[i]
        # print(photoMaps[i])

    photoMaps.append("尘白恢复感知")
    photoMaps.append("尘白快速作战")

    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "尘白恢复感知" in name:
            backToMain()
            break

        if "尘白快速作战" in name:
            autoBattle()
            break

        dao.moveTo(x, y)

def dailyAll():
    # dailyMission()
    getFriend()
    dailyFree()
    dailyCharacterPre()
    dailyShop()
    dailyEvent(eventName="空都演绎")
    dailyMission()
    dailyWarOrder()


if __name__ == '__main__':
    # openGame()
    # getFriend()
    # dailyFree()
    # autoBattle()
    # getFriend()
    # dailyFree()
    # dailyCharacterPre()
    # dailyMission()
    # dailyShop()
    # dailyWarOrder()
    # dailyEvent()
    # autoBattle()
    dailyMission()
    dailyWarOrder()