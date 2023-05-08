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
cv.set_value("path", cv.pcrAirPath)
cv.set_value("device", cv.pcrAirDevice)
flag = True

__author__ = "user"


def cvInit(path=cv.pcrAirPath, device=cv.pcrAirDevice):
    cv._init()
    cv.set_value("path", path)
    cv.set_value("device", device)
    # cv.set_value("device", cv.DBLdeviceHome)


# 自动推图
# 2023年5月4日23:19:36
def autoFight():
    photoMap = air.Photo()
    photoMaps = [
        "地图已攻略",
        "关卡未攻略",
        "关卡已攻略",
        "战斗开始",
        "关闭",
        "活动关卡",
        # "返回",
        "主页",
        "取消",
        "pcr对话框一",
    ]
    startMaps = [
        (127,251), # 0,45图初始
        (205, 307),  # 1,45图困难
        (200, 360),  # 2,祈梨SOS活动。
        (130, 360),  # 3,祈梨SOS活动普通后半。
    ]
    moveMaps = [
        (930,270), # 0 ,关卡已攻略，下一张。
        (840, 450),  # 1 ,关卡未攻略，开始挑战。
    ]
    print("目前的任务是:{}".format("autoFight"))
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "主页".__eq__(name):
            for i in startMaps:
                touch(i)
            continue

        if "关卡已攻略".__eq__(name):
            touch(moveMaps[0])
            continue

        if "关卡未攻略".__eq__(name):
            touch(moveMaps[1])
            continue

        if "战斗开始".__eq__(name):
            startBattle()
            continue

        touch(pos)
        sleep(0.3)

# 自动推图战斗部分 2023年5月8日20:07:34
def startBattle():
    photoMap = air.Photo()
    photoMaps = [
        "pcr对话框一",
        "主页",
        "关闭",
        "下一步",
        "好感度跳过",
        "战斗标识1",
        "战斗开始",
        "取消",
    ]
    print("目前的任务是:{}".format("startBattle"))
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "战斗标识1".__eq__(name):
            sleep(10)
            continue

        if "主页".__eq__(name):
            break

        touch(pos)
        sleep(0.3)

# 打开游戏入口 2023年5月8日20:07:14
def openGame(start = 0):
    photoMap = air.Photo()
    photoMaps = [
        '账号登录',
        '切换账号',
        '切换账号',
        '眼镜厂标识',
        '开始游戏',
    ]
    moveMaps = [
        (590, 230) , # 0 账号登录前先点开账号下拉列表
    ]
    count = start
    while 1 :
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "账号登录".__eq__(name):
            touch(moveMaps[0])
            # ADB太快了，不加这个压根等不到UI弹出来。
            time.sleep(2)
            choosePlayer(count)
            closeGame()
            count += 1
            if count == 3:
                break
            else:
                continue

        touch(pos)

# 登录的时候选择账号 2023年5月7日23:28:12
def choosePlayer(playerNum = 0):
    photoMap = air.Photo()
    photoMaps = [
        '账号登录',
    ]
    playerMaps = [
        "pcr大号",
        "pcr小号",
        "pcr小小号",
    ]
    playerTempMaps = [
    ]
    count = 0
    playerTempMaps.append(playerMaps[playerNum])
    while 1 :
        photoMap.loopSearch(playerTempMaps)
        name = photoMap.name
        pos = photoMap.pos
        touch(pos)

        if "pcr大号".__eq__(name):
            count = 0
            playerTempMaps = photoMaps
            # dailyMission(1)
            continue

        if "pcr小小号".__eq__(name):
            count = 2
            playerTempMaps = photoMaps
            # dailyMissionSmall()
            continue

        if "pcr小号".__eq__(name):
            count = 1
            playerTempMaps = photoMaps
            # dailyMission(0)
            continue

        if "账号登录".__eq__(name):
            dailyMission(count)
            break

# 日常入口
# 2023年5月8日20:06:59
def dailyMission(count):
    enterGame()
    getMana()
    dailyEgg()
    get10Power()
    dailyClan()

# 换号
# 2023年5月8日20:06:39
def closeGame():
    photoMap = air.Photo()
    photoMaps = [
        "回到标题界面",
        "主菜单",
        "确认",
        "关闭",
        "眼镜厂标识",
    ]
    photoMapsTemp = [
        "pcr主页",
    ]
    while 1:
        photoMap.loopSearch(photoMapsTemp)
        name = photoMap.name
        pos = photoMap.pos

        if "眼镜厂标识".__eq__(name):
            break

        if "pcr主页".__eq__(name):
            photoMapsTemp = photoMaps
            continue

        touch(pos)

# 进入游戏
# 2023年5月8日20:06:30
def enterGame():
    photoMap = air.Photo()
    photoMaps = [
        "确认",
        "关闭",
        "好感度跳过",
        "pcr主页",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "pcr主页".__eq__(name):
            break

        touch(pos)

# 2023年5月8日20:06:14
# 获得玛娜
def getMana():
    photoMap = air.Photo()
    photoMaps = [
        "确认",
        "免费10",
        "pcr主页",
        "取消"
    ]
    moveMaps = [
        (185,62) , # 0 点击mana入口
        (582,478) , # 1 点击购买。
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "pcr主页".__eq__(name):
            touch(moveMaps[0])
            continue

        if "免费10".__eq__(name):
            touch(moveMaps[1])
            continue

        if "取消".__eq__(name):
            backToMain()
            break

        touch(pos)

# 2023年5月8日20:06:06
# 返回首页
def backToMain():
    photoMap = air.Photo()
    photoMaps = [
        "返回",
        "确认",
        "主页",
        "pcr主页",
        "取消"
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "pcr主页".__eq__(name):
            break

        touch(pos)

# 日常抽普通扭蛋 2023年5月8日20:18:32
def dailyEgg():
    photoMap = air.Photo()
    photoMaps = [
        "扭蛋完成抽取",
        "白色确认",
        "确认",
        "转蛋免费",
        "转蛋普通",
        "每日转蛋",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "扭蛋完成抽取".__eq__(name):
            backToMain()
            break

        touch(pos)

# 日常抽行会点赞 2023年5月8日20:18:32
def get10Power():
    photoMap = air.Photo()
    photoMaps = [
        "已点赞",
        "确认",
        "行会点赞",
        "行会成员信息",
        "行会",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if ("确认".__eq__(name)) | ("已点赞".__eq__(name)):
            backToMain()
            break

        touch(pos)

# 日常公会收体力 2023年5月8日20:45:53
def dailyClan():
    photoMap = air.Photo()
    photoMaps = [
        "公会已收取",
        "关闭",
        "公会全部收取",
        "公会之家",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "公会已收取".__eq__(name):
            backToMain()
            break

        touch(pos)

if __name__ == "__main__":
    # startBattle()
    autoFight()
    # dailyMission(0)
    # closeGame()
    # get10Power()
    # enterGame()
    # backToMain()
    # dailyClan()