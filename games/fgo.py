# emulator-5560
import _thread
import time

from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from dao import airMultiPhotos as air
from dao import changeVar as cv

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__,devices=[cv.device])

path = cv.FgoPath

spaceFlag = False

flag = True

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
        while 1 :
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos
            touch(pos)
            if "迦勒底" in name:
                changeSpaceFlag(False)
                break
    except Exception as e:
        return 0
    # finally:
    #     # generate html report
    #     simple_report(__file__)

def battle():
    photoMaps = [
        # "技能2",
        # "攻击",
        "战斗界面",
    ]
    moveMaps = [
        (310,152), # 一宝具
        (486,152), # 二宝具
        (657,152), # 三宝具
        (98,376), # 卡1
        (289,376), # 卡2
    ]
    try:
        # print(poco.adb_client.get_device_info())  # 获取设备信息
        for i in photoMaps:
            # 获取图片，不操作。
            temp = Template(path + i + ".png")
            # print(temp)
            if "界面" in i:
                for step in moveMaps:
                    touch(step)
            if not exists(temp):
                continue
            touch(temp)
    except Exception as e:
        return e
    # finally:
    #     # generate html report
    #     simple_report(__file__, logpath=True)

# 用来敲空格的线程。
def spaceClick():
    while spaceFlag:
        keyevent("q")
        time.sleep(3)

# 进入游戏双线程，留一个敲空格。
def openGame(thread1,thread2):
    try:
        global flag
        flag = True
        changeSpaceFlag(True)
        _thread.start_new_thread(thread1, ())
        _thread.start_new_thread(thread2, ())
    except:
        print("Error: 无法启动线程")

    while 1:
        if flag == False:
            break
        pass

def changeSpaceFlag(switch = False):
    global spaceFlag
    spaceFlag = switch

if __name__ == "__main__":
    # enterGame()
    openGame(enterGame,spaceClick)

