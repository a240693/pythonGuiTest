# emulator-5560
from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from dao import airMultiPhotos as air
from dao import changeVar as cv

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__,devices=[cv.device])

path = cv.path

def enterGame():
    photoMap = air.Photo()
    photoMaps = [
        "fgo",
    ]
    moveMaps = [
        (943, 136),  # 滑动起点。
        (943, 282),  # 每日滑动终点
        (943, 177),  # 种火滑动。
    ]
    try:
        photoMap.loopSearch(photoMaps)
        print(photoMap.name)
    finally:
        # generate html report
        simple_report(__file__, logpath=True)

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
            # touch(temp)
    finally:
        # generate html report
        simple_report(__file__, logpath=True)

if __name__ == "__main__":
    enterGame()

