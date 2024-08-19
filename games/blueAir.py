# emulator-5560
import _thread
import datetime
import time

from airtest.core.api import *
from dao import airMultiPhotos as air
from dao import changeVar as cv
import logging

# 日志只输出INFO等级，debugger等级不输出。
logger = logging.getLogger("airtest")
logger.setLevel(logging.INFO)

cv._init()
tempDevice = cv.blueDevice  # 办公室
# tempDevice = cv.kgDevice # 家

cv.set_value("path", cv.bluePath)
cv.set_value("device", tempDevice)

flag = True

__author__ = "user"


def cvInit(path=cv.bluePath, device=cv.blueDevice):
    cv._init()
    cv.set_value("path", path)
    cv.set_value("device", device)


def autoStart():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "跳过",
        "自动",
        "确认二",
        "确认",
        "出击",
        '开始任务',
        '开始任务二',
        "剧情目录",
        "奖励信息",
        "菜单",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "自动".__eq__(name):
            time.sleep(30)
            continue

        if "剧情目录".__eq__(name):
            break

        if "奖励信息".__eq__(name):
            break

        if "菜单".__eq__(name):
            break

        touch(pos)


def autoText():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "获得奖励",
        "进入剧情",
        "出击",
        "剧情确认",
        "跳过图标",
        "菜单",
        "开始任务",
        "开始任务二",
        "活动",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "出击".__eq__(name):
            autoStart()
            continue

        if "开始任务二" in name:
            autoStart()
            continue

        if "活动" in name:
            break

        touch(pos)


def autoClan():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "设置助力者",
        "小组大厅",
        "小组",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "小组大厅".__eq__(name):
            backToMain()
            break

        if "设置助力者".__eq__(name):
            backToMain()
            break

        touch(pos)


def backToMain():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "返回",
        "业务区",
        "业务区2",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "业务区" in name:
            break

        touch(pos)


def dailyCoffee():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "领取",
        "咖啡厅收益",
        "剧情确认",
        "咖啡厅",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "领取".__eq__(name):

            for i in range(1, 5):
                touch(pos)

            backToMain()
            break

        touch(pos)


def dailyDate():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "日程耗尽",
        "开始日程",
        "选择日程",
        # "爱心", 太TM小辣。
        "日程等级",
        "全部日程",
        "评级",
        "日程",
        "等级提升",
    ]
    moveMaps = [
        (608, 132),  # 0 第1个
        (608, 132 + 100),  # 1 第2个
        (608, 132 + 100 * 2),  # 2 第3个
        (608, 132 + 100 * 3),  # 3 第4个
        (266, 199),  # 4，选择日程第一个的。
        (429, 199),  # 5，选择日程第二个的。
        (643, 199),  # 6，选择日程第三个的。
    ]
    date = datetime.date.today().weekday() % 4
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "日程等级".__eq__(name):
            touch(moveMaps[date])
            continue

        if "选择日程".__eq__(name):
            for i in range(4, 7):
                touch(moveMaps[i])
                sleep(1)
            continue

        if "日程耗尽".__eq__(name):
            backToMain()
            break

        touch(pos)


# 点击进去随便打一把经验值？
def dailySpecial():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "特别委托",
        "业务区",
        "业务区2",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "领取".__eq__(name):

            for i in range(1, 5):
                touch(pos)

            backToMain()
            break

        touch(pos)


# 目前还需要手动选一下关卡然后开始，算是能用。
def dailyReward():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "入场券不足",
        "08",
        "悬赏通缉",
        "业务区",
        "业务区2",
    ]
    photoMapOne = [
        "高架公路",
        "沙漠铁路",
        "讲堂",
    ]
    moveMaps = [
        (845, 480),  # 0 最后一个。
    ]
    count = 0
    photoMaps.insert(0, photoMapOne[count])
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "入场券不足".__eq__(name):
            backToMain()
            if count == 2:
                break
            else:
                count += 1
                photoMaps.pop(0)
                photoMaps.insert(0, photoMapOne[count])
                continue

        if "08".__eq__(name):
            touch(moveMaps[0])
            autoSkipBattleSimple()
            continue

        touch(pos)


def dailyMisson():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        # "挑战",  # 不好用。
        "前往",
        "一键领取",
        "工作任务",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "前往".__eq__(name):
            backToMain()
            break

        touch(pos)


def autoAddLv():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "升级已选择",
        "自动选择",
    ]
    photoMapsNext = [
        # "升级已结束",
        "升级",
    ]
    tempMap = photoMaps
    while 1:
        photoMap.loopSearch(tempMap)
        pos = photoMap.pos
        name = photoMap.name

        if "升级已选择".__eq__(name):
            tempMap = photoMapsNext
            continue

        if "升级".__eq__(name):
            tempMap = photoMaps
            touch(pos)
            continue

        touch(pos)


def autoSkipBattle():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "购买AP",
        "次数不足",
        "次数不足",
        "扫荡确认",
        "剧情确认",
        "开始扫荡",
    ]
    moveMaps = [
        (779, 225),  # 0 扫荡加号
        (87, 266),  # 1 向左一格
    ]
    tempMap = photoMaps
    while 1:
        photoMap.loopSearch(tempMap)
        pos = photoMap.pos
        name = photoMap.name

        if "开始扫荡".__eq__(name):
            touch(moveMaps[0], times=4)
            sleep(1)
            touch(pos)
            continue

        if "次数不足".__eq__(name):
            touch(moveMaps[1], times=2)
            continue

        if "购买AP".__eq__(name):
            backToMain()
            break

        touch(pos)


# 专门做给悬赏的自动点击，不包含向左。
def autoSkipBattleSimple(times = 1):
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "入场券不足",
        "购买AP",
        "次数不足",
        "扫荡确认",
        "剧情确认",
        "开始扫荡",
        "高架公路",
    ]
    moveMaps = [
        (779, 225),  # 0 扫荡加号
        (87, 266),  # 1 向左一格
    ]
    tempMap = photoMaps
    while 1:
        photoMap.loopSearch(tempMap,times)
        pos = photoMap.pos
        name = photoMap.name

        if "开始扫荡".__eq__(name):
            touch(moveMaps[0],2)
            sleep(1)
            touch(pos)
            continue

        if "高架公路".__eq__(name):
            break

        if "入场券不足".__eq__(name):
            # backToMain()
            break

        touch(pos)


def dailyAll():
    autoClan()  # 自动进公会
    dailyMail()
    for i in range(0,3):
        dailyWeapon(choice=i,stageChoice=0)
    daily90()
    dailyCoffee()  # 自动咖啡厅
    # dailyDate() # 自动日程
    dailyDateNew() # 自动日程，新
    dailyReward()  # 半自动悬赏
    # dailySpecial() # 还没做好，自动特别委托，这东西真有必要吗。
    dailyPVP()
    dailyMisson()  # 自动获取工作任务。


def dailyPVP():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "对战结果",
        "出击",
        "编队",
        "获得奖励",
        "领取奖励",
        "战术对抗赛",
        "业务区",
        "业务区2",
    ]
    moveMaps = [
        (264, 356),  # 0 每日获取奖励
        (274, 283),  # 1 每日获取信用点
        (555, 174),  # 2 点第一个PVP对手

    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "领取奖励".__eq__(name):
            for i in moveMaps:
                touch(i)
            continue

        if "对战结果".__eq__(name):
            backToMain()
            break

        touch(pos)


def dailyMail():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "暂无邮件",
        "一键领取",
        "邮件",
    ]
    moveMaps = [
        (264, 356),  # 0 每日获取奖励
        (274, 283),  # 1 每日获取信用点
        (555, 174),  # 2 点第一个PVP对手

    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "暂无邮件".__eq__(name):
            backToMain()
            break

        touch(pos)


def daily90():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "获得奖励",
        "确认二",
        "30体力",
        "90体力",
        "选择购买",
        "商店战术对抗赛",
        "商店",
    ]
    moveMaps = [
        (264, 356),  # 0 每日获取奖励
        (274, 283),  # 1 每日获取信用点
        (555, 174),  # 2 点第一个PVP对手

    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "30体力".__eq__(name):
            touch(pos)
            photoMaps.remove("30体力")
            continue

        if "90体力".__eq__(name):
            touch(pos)
            photoMaps.remove("90体力")
            continue

        if "获得奖励".__eq__(name):
            touch(pos)
            backToMain()
            break

        touch(pos)


# 新做日程选择,旧的需要手操一次，过于麻烦。 2024年2月16日
def dailyDateNew():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "正在参加的成员",
        "日程耗尽",
        "开始日程",
        # "选择日程",
        # "爱心", 太TM小辣。
        "日程等级",
        "全部日程",
        "评级",
        "日程",
        "等级提升",
    ]
    moveMaps = [
        (608, 132),  # 0 第1个
        (608, 132 + 100),  # 1 第2个
        (608, 132 + 100 * 2),  # 2 第3个
        (608, 132 + 100 * 3),  # 3 第4个
        (266, 199),  # 4，选择日程第一个的。
        (429, 199),  # 5，选择日程第二个的。
        (643, 199),  # 6，选择日程第三个的。
    ]
    date = datetime.date.today().weekday() % 4
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "日程等级".__eq__(name):
            touch(moveMaps[date])
            continue

        if "正在参加的成员".__eq__(name):
            dailyDateNewNext()
            backToMain()
            break

        touch(pos)


# 进具体日程页，开始处理选择页面。 2024年2月16日
def dailyDateNewNext():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "日程奖励",
        "等级提升",
        "开始日程",
        "日程耗尽",
        "正在参加的成员",
        "持有日程卷",
    ]
    moveMaps = [
        (120, 420),  # 0 选择日程 第三行第一个。
        (120 + 280, 420),  # 1 第2个
        (120 + 280 * 2, 420),  # 2 第3个
        (872, 502),  # 3 持有日程卷的时候点右下角。
    ]
    finishFlag = 0
    finishFlagOld = 1
    while 1:
        # 记得两个条件分别加括号，除非用.eq那个写法，不然判断会出错。
        if (finishFlag == finishFlagOld) & (finishFlag == 1):
            photoMaps.remove("正在参加的成员")
            finishFlagOld = 0

        if (finishFlag == finishFlagOld) & (finishFlag == 0):
            photoMaps.append("正在参加的成员")
            finishFlagOld = 1

        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "正在参加的成员".__eq__(name):
            for i in range(0, 3):
                touch(moveMaps[i])
            continue

        if "开始日程".__eq__(name):
            touch(pos)
            finishFlag = 1
            continue

        if "等级提升".__eq__(name) | "日程奖励".__eq__(name):
            dailyDateNewNextPage()
            finishFlag = 0
            continue

        if "持有日程卷".__eq__(name):
            touch(moveMaps[3])
            continue

        if "日程耗尽".__eq__(name):
            break

        touch(pos)


# 专门用来翻页。 2024年2月16日
def dailyDateNewNextPage():
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "持有日程卷",
        "等级提升",
        "正在参加的成员",
        "全部日程",
    ]
    moveMaps = [
        (930, 270),  # 0，结算后往右切换学院。
        (429, 199),  # 1，选择日程第二个的。
        (643, 199),  # 2，选择日程第三个的。
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "正在参加的成员".__eq__(name) | "全部日程".__eq__(name):
            touch(moveMaps[0])
            continue

        if "持有日程卷".__eq__(name):
            touch(moveMaps[0])
            break

        touch(pos)


# 专门做专武材料。 2024年2月17日
def dailyWeapon(choice=0,stageChoice=0):
    count = 0
    photoMap = air.Photo()
    photoMaps = [
        "关卡列表",
        "选择学院",
        "学院交流会",
        "业务区",
        "业务区2",
    ]
    moveMaps = [
        (605, 200),  # 0，结算后往右切换 学院。
        (605, 300),  # 1，选择日程第二个的。
        (605, 400),  # 2，选择日程第三个的。
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "选择学院".__eq__(name):
            touch(moveMaps[choice])
            continue

        if "关卡列表".__eq__(name):
            dailyWeaponNext(stageChoice)
            break

        touch(pos)


# 专门做专武材料。 2024年2月17日
def dailyWeaponNext(stageChoice=0):
    photoMap = air.Photo()
    photoMaps = [
        "扫荡完成",
        "确认二",
        "开始扫荡",
        "关卡列表",
    ]
    moveMaps = [
        (830, 216),  # 0，第二个。
        (830, 283),  # 1，第三个。
        (779, 225),  # 2 扫荡加号
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "开始扫荡".__eq__(name):
            touch(moveMaps[2], times=4)
            time.sleep(1)
            touch(pos)
            continue

        if "关卡列表".__eq__(name):
            touch(moveMaps[stageChoice])
            continue

        if "扫荡完成".__eq__(name):
            backToMain()
            break

        touch(pos)


# 情人节巧克力活动。
def eventChoco():
    photoMap = air.Photo()
    photoMaps = [
        "获得奖励",
        "菜单",
        "剧情确认",
        "外出按钮",
        "邀请外出",
    ]
    moveMaps = [
        (830, 216),  # 0，第二个。
        (830, 283),  # 1，第三个。
        (779, 225),  # 2 扫荡加号
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "菜单".__eq__(name):
            autoText()
            continue

        touch(pos)

# 活动掷骰子。
def eventRun():
    photoMap = air.Photo()
    photoMaps = [
        "获得奖励",
        "掷骰子",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        touch(pos)


if __name__ == "__main__":
    # autoText()
    # autoStart()
    # dailyDate()
    # dailyMisson()
    # autoAddLv()
    # dailyMail()
    # dailyMisson()
    # for i in range(0,3):
    #     dailyWeapon(choice=i,stageChoice=0)
    # dailyWeaponNext()
    # eventChoco()
    # dailyReward()  # 半自动悬赏
    # dailySpecial() # 还没做好，自动特别委托，这东西真有必要吗。
    # dailyPVP()
    # dailyMisson()  # 自动获取工作任务。
    eventRun()