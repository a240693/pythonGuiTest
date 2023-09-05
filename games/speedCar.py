import pyautogui as py
import time
import random

from dao import dao, daoImpl, multiphotos, resultMap
from dao import changeVar as cv
import _thread

cv._init()
cv.set_value("path", cv.speedCarPath)


# 打开游戏。
def openGame():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "极速启动游戏",
        "游戏开始图标",
        "极速比赛",
        "极速比赛2",
    ]
    photoMapsNext = [
        "极速比赛",
        "极速比赛2",
        "活动取消",
        "极速进入游戏二",
        "极速进入游戏",
        "启动游戏",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "开始图标" in name:
            dao.moveTo2(x, y)
            continue

        if "启动游戏" in name:
            dao.moveTo(x, y)
            photoMaps = photoMapsNext
            continue

        if "极速比赛" in name:
            break

        dao.moveTo(x, y)

# 每日拿不值钱的宝箱。
def dailyBonus():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "每日宝箱已领取",
        "宝箱免费领取确认",
        "宝箱免费领取",
        "免费领取入口",
        "极速礼包",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "已领取" in name:
            backToMain()
            break

        dao.moveTo(x, y)

# 返回主页。
def backToMain():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "极速比赛",
        "返回主界面",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "极速比赛" in name:
            break

        dao.moveTo(x, y)

# 月卡领取。
def dailyMonthCard():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "月卡已领取",
        "宝箱免费领取确认",
        "月卡点击领取",
        "极速月卡",
        "极速礼包",
        "极速特惠",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "已领取" in name:
            backToMain()
            break

        dao.moveTo(x, y)


# 日常派遣人物去赛车，目前没做结束，可以用来半自动。
# 2023年6月30日
def dailyBussiness():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "选手已选择",
        "极速一键选择",
        "极速赛事中心",
        "宝箱免费领取确认",
        "极速收取1",
        "极速经营",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "已选择" in name:
            dailySendPeople()
            continue

        dao.moveTo(x, y)

# 赛车子页面功能。
def dailySendPeople():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "极速比赛完成",
        "宝箱免费领取确认",
        "极速派遣比赛确认",
        "极速派遣比赛",
        "选手已选择",
        "极速一键选择",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "完成" in name:
            break

        if "一键选择" in name:
            break

        dao.moveTo(x, y)

# 工坊点赞
def dailyGood():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "极速已点赞",
        "极速点赞",
        "工坊免费",
        "极速冲分爱车",
        "极速工坊",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "已点赞" in name:
            backToMain()
            break

        dao.moveTo(x, y)

# 每日任务自动获取
def dailyMission():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "极速合约继续",
        "宝箱免费领取确认",
        "极速一键领取",
        "极速任务",
        "极速任务已完成",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "已完成" in name:
            backToMain()
            break

        dao.moveTo(x, y)

# 每日汇总
def dailyAll():
    openGame()
    # dailyMonthCard()
    dailyBonus()
    dailyGood()
    # 暂时没想好怎么做连贯，先屏蔽。
    # dailyBussiness()
    dailyMission()

if __name__ == '__main__':
    # dailyBussiness()
    dailyAll()
    # dailyMission()
    # dailyGood()
    # dailySendPeople()
    # dailyBussiness()
    # dailyMonthCard()
    # dailyBonus()
    # openGame()