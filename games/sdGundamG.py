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
cv.set_value("path", cv.SDPath)
cv.set_value("device", cv.SDdevice)
# cv.set_value("device", cv.DBLdeviceHome)
flag = True

__author__ = "user"
exitFlag = 0


def cvInit(path=cv.SDPath, device=cv.SDdevice):
    cv._init()
    cv.set_value("path", path)
    cv.set_value("device", device)


# RUSH入口半自动试做 2025年4月23日
def autoRush(times = 99):
    photoMap = air.Photo()
    photoMaps = [
        "回复AP",
        "继续",
        "出击",
        "再次出击2",
        "结算关闭",
        "Tap",
    ]
    time = 0
    tempflag = 0
    while (time < times) | (times == 0):
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "继续".__eq__(name):
            tempflag = 1
            touch(pos)
            sleep(1)
            continue

        # 高低切换才算一次，切掉冗余。
        if ("出击" in name) & (tempflag == 1):
            tempflag = 0
            time += 1
            print("第{}次完成，开始重试。".format(time))

        if "回复AP".__eq__(name):
            break

        touch(pos)
        sleep(0.3)


# 半自动拉满，2025年4月23日
def autoMaxSelect():
    photoMap = air.Photo()
    photoMaps = [
        "OK",
        "执行",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        touch(pos)
        sleep(0.3)


# 半自动铁球，2025年4月26日
def autoBuyBall(times=99):
    photoMap = air.Photo()
    photoMaps = [
        "铁球Tap",
        "Tap",
        "执行",
        "执行开发",
        "铁球",
    ]
    tempflag = 0
    time = 0
    while (time < times) | (time == 0):
        photoMap.loopSearch(photoMaps,time=0.2)
        pos = photoMap.pos
        name = photoMap.name

        if "执行开发".__eq__(name):
            tempflag = 1
            touch(pos)
            continue

        # 高低切换才算一次，切掉冗余。
        if ("Tap" in name) & (tempflag == 1):
            tempflag = 0
            time += 1
            print("第{}台铁球，{}GP,已花{}金币。".format(time, 20 * time, 500 * time))

        touch(pos)

# 强敌爬塔专用。
def auto20(times=99):
    photoMap = air.Photo()
    photoMaps = [
        "出击",
        "选择关卡",
        # "回复AP",
        "继续",
        "爬塔挑战",
        "结算关闭",
        "Tap",
    ]
    time = 0
    tempflag = 0
    while (time < times) | (times == 0):
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "继续".__eq__(name):
            tempflag = 1
            touch(pos)
            sleep(1)
            continue

        # 高低切换才算一次，切掉冗余。
        if ("出击" in name) & (tempflag == 1):
            tempflag = 0
            time += 1
            print("第{}次完成，开始重试。".format(time))

        if "回复AP".__eq__(name):
            break

        touch(pos)
        sleep(0.3)

# pvp收尾用 2025年9月22日。
def afterPvP(times=99):
    photoMap = air.Photo()
    photoMaps = [
        "选择对战对手",
        "skip",
        "Tap",
    ]
    time = 0
    tempflag = 0
    while (time < times) | (times == 0):
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "选择对战对手".__eq__(name):
            tempflag = 1
            touch(pos)
            sleep(1)
            continue

        # 高低切换才算一次，切掉冗余。
        if ("skip" in name) & (tempflag == 1):
            tempflag = 0
            time += 1
            print("第{}次完成，开始重试。".format(time))

        if "回复AP".__eq__(name):
            break

        touch(pos)
        sleep(0.3)

# 自动抽活动蛋，2025年10月29日
def autoEventEgg():
    photoMap = air.Photo()
    photoMaps = [
        "奖章不足",
        "再次交换",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "奖章不足".__eq__(name):
            break

        touch(pos)
        sleep(0.3)

# 测试每日3次入口，2025年11月17日
def autoDailyThreeEnter():
    photoMap = air.Photo()
    photoMaps = [
        "金币等级5",
        "关闭",
        "金币入口",
        "强化培育关卡",
        "主界面关卡",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "金币等级5".__eq__(name):
            break

        if "金币入口".__eq__(name):
            touch(pos)
            sleep(1)
            continue


        touch(pos)
        sleep(0.3)

# 测试每日3次，2025年11月17日
def autoDailyThree():
    photoMap = air.Photo()
    photoMaps = [
        "每日达到上限",
        "OK",
        "执行",
        "略过1",
    ]
    moveMaps = [
        (945,273), # 0  向右一页。
    ]
    time = 0
    change = 0
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "每日达到上限".__eq__(name):

            if 1 == change:
                time += 1
                change = 0

            if 4 == time:
                break

            touch(moveMaps[0])
            sleep(1)
            continue

        if "OK".__eq__(name):
            change = 1

        touch(pos)
        sleep(0.3)

# 回主界面，2025年11月17日
def backToMain():
    photoMap = air.Photo()
    photoMaps = [
        "后退",
        "主界面出击",
        "主界面",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "主界面出击".__eq__(name):
            break

        touch(pos)
        sleep(0.3)



# 自动开发，2025年11月17日
def autoDevelop(times = 1):
    photoMap = air.Photo()
    photoMaps = [
        "Tap开发",
        "执行",
        "执行开发",
        "全部开发",
        "钢坦克",
        "开发高达",
        "开发",
        # "关闭",
    ]
    tempflag = 0
    time = 0
    while (time < times) | (time == 0):
        photoMap.loopSearch(photoMaps, time=0.2)
        pos = photoMap.pos
        name = photoMap.name

        if "执行开发".__eq__(name):
            tempflag = 1
            touch(pos)
            continue

        # 高低切换才算一次，切掉冗余。
        if ("Tap" in name) & (tempflag == 1):
            tempflag = 0
            time += 1
            print("第{}台钢坦克，{}GP,已花{}金币。".format(time, 20 * time, 500 * time))
            # 不点两次好像不会自己跳出，很猪头。
            touch(pos)
            sleep(0.5)

        touch(pos)

# 买商店前4个，可能有BUG 2025年11月18日
def dailyShop():
    photoMap = air.Photo()
    photoMaps = [
        "商店卖完",
        "全部购买1",
        "购买",
        # "高级",
        "商店",
        "关闭",
    ]
    moveMaps = [
        (360,80) , # 0 第一个商品。
        (540,80), # 1 第二个商品。
        (720, 80),  # 2 第三个商品。
        (900, 80),  # 3 第四个商品。

    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "全部购买1".__eq__(name):

            for moveMap in moveMaps:
                touch(moveMap)
                sleep(0.5)

            touch(pos)
            continue

        if "商店卖完".__eq__(name):
            break

        touch(pos)
        sleep(0.3)


def dailyAll():
    enterGame()
    # 自动开发钢坦克一台。
    autoDevelop()
    backToMain()

    # 自动商店。
    dailyShop()
    backToMain()

    # 每日自动三次
    autoDailyThreeEnter()
    autoDailyThree()
    backToMain()


# 进入游戏，2025年11月18日
def enterGame():
    photoMap = air.Photo()
    photoMaps = [
        "主界面出击",
        "Tap",
        "Tap开发",
        "游戏图标",
        "关闭",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "主界面出击".__eq__(name):
            break

        touch(pos)
        sleep(0.3)


def debug_coordinate_system():
        # 确保设备连接
        photoMap = air.Photo()
        """诊断横竖屏坐标系问题"""
        print("=== 坐标系诊断 ===")

        # 获取设备信息
        dev = device()
        current_resolution = dev.get_current_resolution()
        print(f"当前分辨率: {current_resolution}")

        # 测试屏幕四个角落的点击
        width, height = current_resolution
        test_points = [
            (100, 100),  # 左上
            (width - 100, 100),  # 右上
            (100, height - 100),  # 左下
            (width - 100, height - 100)  # 右下
        ]

        for i, (x, y) in enumerate(test_points):
            print(f"点击测试点 {i + 1}: ({x}, {y})")
            touch((x, y))
            time.sleep(1)

        # 检查截图方向
        snapshot("debug_screen.png")
        print("截图保存为: debug_screen.png")


if __name__ == "__main__":
    # autoRush()
    # autoBuyBall(10)
    # enterGame()
    # autoDailyThree()
    # autoEventEgg()
    # backToMain()
    # autoDevelop()
    # dailyShop()

    # 自动商店。
    # dailyShop()
    # backToMain()
    # 验证截图方向
    # debug_landscape_issue("F:\pyTest\DBL\龙珠图标横.png")
    # debug_coordinate_system()
    # 每日自动三次
    autoDailyThreeEnter()
    autoDailyThree()
    backToMain()