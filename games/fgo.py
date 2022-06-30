# emulator-5560
import _thread
import time

from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from dao import airMultiPhotos as air
from dao import changeVar as cv
import logging
# 日志只输出INFO等级，debugger等级不输出。
logger = logging.getLogger("airtest")
logger.setLevel(logging.INFO)

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__, devices=[cv.device])

path = cv.FgoPath

spaceFlag = False

flag = True

continueFlag = False

__author__ = "user"


def enterGame():
    photoMap = air.Photo()
    photoMaps = [
        "fgo",
        "迦勒底之门",
        "关闭公告",
    ]
    moveMaps = [
        (943, 136),  # 滑动起点。
        (943, 282),  # 每日滑动终点
        (943, 177),  # 种火滑动。
    ]
    try:
        while 1:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos
            if "fgo".__eq__(name):
                changeSpaceFlag(True)
            if "迦勒底" in name:
                changeSpaceFlag(False, False)
                break
            touch(pos)
    except Exception as e:
        return 0
    # finally:
    #     # generate html report
    #     simple_report(__file__)


def battle():
    photoMap = air.Photo()
    photoMaps = [
        "技能已使用",
        "技能2",
        "攻击",
        "战斗界面",
        "战斗结束",
        "战斗结果",
    ]
    actionMaps = [
        (310, 152),  # 一宝具
        (486, 152),  # 二宝具
        (657, 152),  # 三宝具
        (98, 376),  # 卡1
        (289, 376),  # 卡2
    ]

    moveMaps = [
        (324, 319),  # 技能已使用的取消按钮位置。
    ]
    if continueFlag:
        photoMaps.append("续关连续")
    else:
        photoMaps.append("续关关闭")
    try:
        while 1:
            photoMap.loopSearch(photoMaps)
            pos = photoMap.pos
            name = photoMap.name
            # 如果读取到战斗界面就选卡，不点击直接跳过。

            if "界面" in name:
                print("开始选择指令卡。")
                for step in actionMaps:
                    touch(step)
                continue

            if "已使用" in name:
                pos = moveMaps[0]
                photoMaps.remove("技能2")

            print("找到的是{},坐标是{}".format(name, pos))
            touch(pos)

            if "关闭" in name:
                break

    except Exception as e:
        return e
    # finally:
    #     # generate html report
    #     simple_report(__file__, logpath=True)


# 用来敲空格的线程。
def spaceClick():
    while 1 :
        print("spaceFlag:".format(spaceFlag))
        while spaceFlag:
            # print("click Q")
            touch((100,100))
            time.sleep(3)
        time.sleep(3)


# 进入游戏双线程，留一个敲空格。
def openGame(thread1, thread2):
    try:
        global flag
        flag = True
        _thread.start_new_thread(thread1, ())
        _thread.start_new_thread(thread2, ())
    except:
        print("Error: 无法启动线程")

    while 1:
        if flag == False:
            break
        pass


def changeSpaceFlag(switch=False, switch2=True):
    global spaceFlag
    spaceFlag = switch
    global flag
    flag = switch2


def dailyExp():
    photoMap = air.Photo()
    photoMaps = [
        "迦勒底之门",
        "每日任务",
        "种火40",
        "宝石翁",
        "狂阶",
        "开始任务",
        "攻击",
        "银苹果",
        "体力不足",
    ]
    moveMaps = [
        (943, 136),  # 滑动起点。
        (943, 282),  # 每日滑动终点
        (943, 177),  # 种火滑动。
    ]
    try:
        while 1:
            photoMap.loopSearch(photoMaps)
            pos = photoMap.pos
            name = photoMap.name
            if ("不足" in name) & (not continueFlag):
                break
            touch(pos)
            if "每日" in name:
                photoMaps.append("种火30")
            if "30" in name:
                back()
                photoMaps.remove("种火30")
            if ("开始任务".__eq__(name)) | ("攻击".__eq__(name)):
                battle()
            if ("苹果" in name) & continueFlag:
                eatApple()

    except Exception as e:
        return 0


def back():
    photoMap = air.Photo()
    photoMaps = [
        "返回",
    ]
    try:
        while 1:
            photoMap.loopSearch(photoMaps)
            touch(photoMap.pos)
    except Exception as e:
        return 0


def changePos(pos=(0, 0), moveMap=(0, 0)):
    for i in pos:
        pos[i] = pos[i] + moveMap[i]
    return pos

def eatApple(appleFlag = False):
    photoMap = air.Photo()
    photoMaps = [
        "银苹果",
        "苹果确定",
    ]
    if appleFlag :
        photoMaps.append("金苹果")
    while True:
        try:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos
            touch(pos)
            if "确定" in name :
                break
        except Exception as e:
            return 0

# 2022-06-30 20:28:02 跳过剧情。
def skipStory():
    photoMap = air.Photo()
    photoMaps = [
        "跳过剧情",
        "剧情页标",
    ]
    moveMaps = [
        (900,27), # 跳过剧情里面的跳过按钮。
    ]
    while True:
        try:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos
            if "页标" in name :
                touch(moveMaps[0])
            else:
                touch(pos)
        except Exception as e:
            return 0

if __name__ == "__main__":
    # enterGame()
    # openGame(enterGame,spaceClick)
    # dailyExp()
    # battle()
    # eatApple()
    skipStory()
