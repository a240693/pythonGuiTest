import _thread
import time
from dao import changeVar as cv

# pyautogui没法点击
# from dao import multiphotos as mp
# from dao import dao

# 这个注销是从airTest切换成pyautoGui
from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import logging
from dao import airMultiPhotos as air

# 日志只输出INFO等级，debugger等级不输出。
logger = logging.getLogger("airtest")
logger.setLevel(logging.INFO)


def airInit():
    cv._init()
    cv.set_value("path", cv.honkaiPath)
    cv.set_value("device", cv.honkai)


def init():
    cv._init()
    cv.set_value("path", cv.honkaiPath)
    cv.set_value("device", cv.honkai)


def selectPages():
    photoMap = air.Photo()
    photoMaps = [
        "远征",
        "家园",
        "打工",
    ]
    while True:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        touch(pos)


# 家园拿资源和金币后进远征。
def home():
    photoMap = air.Photo()
    photoMaps = [
        "已取出体力",
        "金币",
        "金币1",
        "体力",
        "体力2",
        "取出体力",
        "家园",
        # "远征",
        # "打工",
    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "已取出" in name:
            photoMaps.insert(0, "远征")
            photoMaps.insert(1, "远征页面")
            continue
        if "页面" in name:
            break
        touch(pos)


def expedition():
    photoMap = air.Photo()
    photoMaps = [
        # "远征最近",
        "体力上限",
        "远征满足要求",
        "一键远征",
        "远征确定",
        "完成远征",
        "远征中",
    ]
    moveMaps = [
        (795, 63),  # 0 看到最近点开始远征。
        (399, 275),  # 1 满足要求后开始远征。
    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "最近" in name:
            touchFix(pos, moveMaps[0])
            continue

        if "满足要求" in name:
            touchFix(pos, moveMaps[1])
            continue

        if "上限" in name:
            backToPage()
            break

        if "远征中" in name:
            swipe(pos, vector=[-0.0316, -0.3311], duration=1, steps=6)
            continue

        touch(pos)


def backToPage():
    photoMap = air.Photo()
    photoMaps = [
        "家园",
        "打工",
        "返回",
    ]
    moveMaps = [

    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if ("家园" in name) | ("打工" in name):
            break

        touch(pos)

def backToMain():
    photoMap = air.Photo()
    photoMaps = [
        "出击",
        "主菜单",
        "返回",
    ]
    moveMaps = [

    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if ("出击" in name):
            break

        touch(pos)


def work():
    photoMap = air.Photo()
    photoMaps = [
        "打工完成",
        "一键远征",
        "打工入口",
        "远征确定",
        "打工",
        "打工展开列表",
    ]
    moveMaps = [

    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        touch(pos)
        if "一键" in name:
            goToWork()
            break



def goToWork():
    photoMap = air.Photo()
    photoMaps = [
        # "右箭头",
        "饭团未满足",
        "打工未满足",
        "无合适",
        "一键远征",
        "打工入口",
        # "开始打工灰",
    ]
    moveMaps = [
        (268, 0),  # 0 点完远征后自动点一次开始打工。
        (586, -4),  # 1 没找到合适的女武神就下一个。
        (830, 1),  # 2 同上，但检测点不同，打工未满足专用。
        (1225, 386), #3 右箭头坐标，不用2了，因为体力不满足和打工不满足的坐标会错位。
    ]
    count = 0
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if count >= 3 :
            # 打工失败三次直接认为打工分配结束，回主菜单。
            backToMain()
            break

        if "无合适" in name:
            touchFix(pos, moveMaps[1])
            continue

        if "远征" in name:
            touch(pos, times=2)
            touchFix(pos, moveMaps[0])
            continue

        touch(pos)

        if "入口" in name:
            continue

        if "未满足" in name:
            touch(moveMaps[3])
            count += 1
            continue


def materiels():
    photoMap = air.Photo()
    photoMaps = [
        "已减负",
        "减负",
        "一键减负",
        "材料远征",
        "出击",
    ]
    moveMaps = [

    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "已减负".__eq__(name):
            photoMaps.insert(0, "主菜单")
            photoMaps.insert(1, "家园")
        if "家园" in name:
            break
        touch(pos)


def group():
    photoMap = air.Photo()
    photoMaps = [
        "接受新委托",
        # 没法分辨，PASS。
        "已申请委托",
        "舰团新委托",
        "委托回收",
        "舰团",
    ]
    moveMaps = [

    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "接受" in name:
            photoMaps.remove("舰团新委托")
        if "已申请" in name:
            giveGroup()
            break
        touch(pos)


def giveGroup():
    photoMap = air.Photo()
    photoMaps = [
        "次数耗尽",
        "提交委托",
        "舰团提交",
        "已申请委托",
    ]
    moveMaps = [

    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "耗尽" in name:
            photoMaps.insert(0, "主菜单")
            photoMaps.append("出击")

        touch(pos)

        if "出击" in name:
            break


def daily():
    # 初始化句柄
    init()
    # 家园，获取金币和体力
    home()
    # 远征
    expedition()
    # 打工
    work()
    # 一键材料
    materiels()
    # 舰团
    group()


def touchFix(pos=(0, 0), pos1=(0, 0)):
    x = pos[0] + pos1[0]
    y = pos[1] + pos1[1]
    print("pos:{},pos1:{},新坐标：{}".format(pos, pos1, (x, y)))
    touch((x, y))
    time.sleep(0.3)

def mission():
    photoMaps = [
        "任务",
        "一键领取",
    ]
    moveMaps = [

    ]
    photoMap = air.Photo()
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        touch(pos)


if __name__ == "__main__":
    # daily()
    init()
    # home()
    # expedition()
    # goToWork()
    # work()
    # backToMain()
    # materiels()
    # group()
    mission()
