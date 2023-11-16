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
        "月卡领取",
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

# 获取任务奖励
# 2023年5月5日22:40:13
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
        "星铁退出关卡",
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


def auto60():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "星铁传送",
        "星铁地址传送",
        "星铁光锥经验",
        "星铁花朵金",
        "星铁花朵跳转",
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

        if "星铁传送" in name:
            auto60Next()
            backToMain()
            break

        dao.moveTo(x, y)


def auto60Next():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "星铁战斗标识1",
        "星铁开始挑战",
        "星铁挑战",
        "星铁传送",
        "星铁任务图标",
    ]
    moveMaps = [
        (78, -59),  # 0 挑战前先点6次
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "任务图标" in name:
            dao.pressKey('f')
            continue

        if "星铁挑战" in name:
            dao.moveTo(x + moveMaps[0][0], y + moveMaps[0][1])
            time.sleep(1)
            dao.moveTo(x, y)
            continue

        if "战斗标识1" in name:
            break

        dao.moveTo(x, y)


def autoGetSkill(SkillName = "巡猎"):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "祝福加载",
        "模拟宇宙确认",
        SkillName,
        SkillName,
        SkillName,
        "祝福加载",
        "重置祝福", #现在用这个的话还没加载出来就直接重置了。
        "主界面标识1",

    ]
    moveMaps = [
        (78, -59),  # 0 挑战前先点6次
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "重置祝福".__eq__(name):
            dao.moveTo(x, y)
            autoGetSkillSecond(SkillName)
            break

        if "祝福加载".__eq__(name):
            time.sleep(2)
            continue

        if "主界面标识1".__eq__(name):
            print("选祝福一，返回——————————————————。")
            break

        dao.moveTo(x, y)


def autoGetSkillSecond(SkillName = "欢愉",SkillName1 = "巡猎", SkillName2 = "毁灭"):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "重置祝福",
        "模拟宇宙确认",
        SkillName,
        SkillName,
        SkillName,
        SkillName1,
        SkillName2,
        "主界面标识1",
    ]

    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        print("重置选祝福开始。")
        if "主界面标识1".__eq__(name) :
            print("重置选祝福结束，返回——————————————————。")
            break

        if "模拟宇宙确认".__eq__(name):
            dao.moveTo(x,y)
            print("重置选祝福结束2，返回——————————————————。")
            break

        dao.moveTo(x, y)

def autoSearch():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "远征领取",
        "远征红点",
        "再次派遣",
    ]

    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "主界面标识1".__eq__(name):
            break

        dao.moveTo(x, y)

def skillStart(SkillName = "巡猎"):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "祝福一星",
        "祝福一星2",
        "祝福二星",
        "祝福三星",
    ]

    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        if "祝福" in name:
            autoGetSkill(SkillName)
            continue

# 没做完，自动检查每日。
def checkMission():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "每日侵蚀隧道",
        "星铁任务图标",
    ]

    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "每日侵蚀隧道".__eq__(name):
            backToMain()
            continue

        if "任务图标" in name:
            dao.moveToWithKey(x, y, 'altleft')
            continue

# 没做完，自动做每日。
def autoMission():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "每日侵蚀隧道",
        "星铁任务图标",
    ]

    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "每日侵蚀隧道".__eq__(name):
            backToMain()
            continue

        if "任务图标" in name:
            dao.moveToWithKey(x, y, 'altleft')
            continue

def autoTeam(teamNo = 0):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "鸭鸭",
        "白露",
        "卡夫卡",
        "停云",
    ]
    photoMaps2 = [
        "罗刹",
        "驭空",
        "克拉拉",
        "托帕",
    ]
    if teamNo == 0:
        teamMaps = photoMaps
    elif teamNo == 1:
        teamMaps = photoMaps2
    while 1:
        photoMap.loopSearch(teamMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        dao.moveTo(x,y)


if __name__ == '__main__':
    # openGame()
    # getMissio、n()
    # auto60()
    # backToMain()
    # openGame()
    # auto60()
    # autoGetSkill("巡猎")
    # autoGetSkillSecond()
    autoTeam()