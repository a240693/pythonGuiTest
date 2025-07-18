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
tempDevice = cv.kgDevice  # 办公室
# tempDevice = cv.kgDevice # 家

cv.set_value("path", cv.kgAirPath)
cv.set_value("device", tempDevice)

flag = True

__author__ = "user"


def fullAutoKmx():
    count = 0
    photoMap = air.Photo()
    photoMaps = ['卡马逊主页']
    moveMaps = [
        (490, -373),  # 路线一 0
        (607, -320),  # 路线二 1
        (706, -272),  # 路线三 2
        (800, -222)  # 路线四 3
    ]
    while flag:
        photoMap.name = "默认"
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        if "卡马逊主页".__eq__(photoMap.name):
            for i in moveMaps:
                touchFix(pos, i)
            searchPage()
            # kmxAutoNew()
            if flag:
                count += 1
                # time.sleep(10)
                returnKmx()
    # 人物所在位置  394, 99


def returnKmx():
    photoMap = air.Photo()
    photoMaps = [
        "探险初始页",
        "卡马逊主页",
        "坎公主页面",
    ]
    moveMaps = [
        (-6, -467),  # 0 卡马逊主页 → 探险初始页
        (75, -186),  # 1 探险初始页 → 卡马逊主页
        # (88, -270),  # 1 探险初始页 → 卡马逊主页
        (-834, 237),  # 2 主页面 → 探险初始页
    ]
    while True:
        photoMap = photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "卡马逊" in name:
            touchFix(pos, moveMaps[0])
            time.sleep(1)
        if "主页面" in name:
            touchFix(pos, moveMaps[2])
            continue
        if "初始" in name:
            touchFix(pos, moveMaps[1])
            break


def chooseEquip():
    equipMaps = [
        "坎公高阶神器",
        "坎公高阶神器",
        "坎公中阶神器",
        "坎公中阶神器2",
        "坎公低阶神器",
        "坎公获得银币",
    ]
    photoMaps = [
        "坎公卡马逊确认",
        "替换神器",
        "装备选择",
        "卡马逊主页",
    ]
    switch = 1
    while 1:
        photoMap = air.Photo()
        if switch == 1:
            photoMap.loopSearch(equipMaps)
        elif switch == 2:
            photoMap.loopSearch(photoMaps)
        switch = 2
        pos = photoMap.pos
        name = photoMap.name
        if "替换" in name:
            changeEquip()
            break
        elif "主页" in name:
            break
        touch(pos)


def changeFlag():
    global flag
    flag = False


def touchFix(pos=(0, 0), pos1=(0, 0)):
    x = pos[0] + pos1[0]
    y = pos[1] + pos1[1]
    print("pos:{},pos1:{},新坐标：{}".format(pos, pos1, (x, y)))
    touch((x, y))
    time.sleep(0.3)


def changeEquip():
    photoMaps = [
        "处理装备",
        "坎公卡马逊确认",
        "装备选择",
        "替换神器",
        "卡马逊主页",
    ]
    moveMaps = [
        (486, 191),  # 第一个神器在的位置。
    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "替换神器" in name:
            pos = moveMaps[0]
        if "主页" in name:
            break
        touch(pos)


def searchPage():
    photoMaps = [
        "战斗页",
        "坎公心号",
        "坎公商店",
        # "问号标识一",
        "坎公战队",
        # "问号标识二",
        # "问号标识三",
        "事件标识",
        "卡马逊主页",
    ]
    moveMaps = [
        (486, 191),  # 第一个神器在的位置。
    ]
    global flag
    while flag:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "战斗" in name:
            battle()
            break
        if "心号" in name:
            heart()
            break
        if "事件" in name:
            question()
            break
        if "商店" in name:
            shop()
            break
        if "战队" in name:
            team()
            break
        if "主页" in name:
            break


def battle():
    photoMaps = [
        "战斗进入",
        "坎公卡马逊确认",
        "坎公装备页",
        "挑战成功",
    ]
    moveMaps = [
        (486, 191),  # 第一个神器在的位置。
    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        touch(pos)
        if "进入" in name:
            time.sleep(30)
        if "装备" in name:
            chooseEquip()
            break
        if "成功" in name:
            global flag
            flag = False
            break


def heart():
    photoMaps = [
        "坎公卡马逊确认",
        "坎公心号",
        "卡马逊主页",
    ]
    moveMaps = [
        (750, 250),  # 回血。
        (450, 250),  # 解诅咒。
        (150, 250),  # 复活。
    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "心号" in name:
            for i in moveMaps:
                touchFix(i)
            photoMaps.insert(0, "装备选择")
        if "主页" in name:
            break
        touch(pos)


def shop():
    photoMaps = [
        "装备选择",
        "坎公卡马逊确认",
        "商店退出",
        "坎公商店",
        "卡马逊主页",
    ]
    moveMaps = [

    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "主页" in name:
            break
        touch(pos)


def question():
    photoMaps = [
        "战斗进入",  # 用来容错。
        "坎公卡马逊确认",
        "装备选择",
        "问号标识一",
        "问号标识二",
        "卡马逊主页",
    ]
    moveMaps = [

    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "主页" in name:
            break
        if "选择" in name:
            photoMaps.remove("问号标识一")
            photoMaps.remove("问号标识二")
        touch(pos)


def team():
    photoMaps = [
        "坎公卡马逊确认",
        "装备选择",
        "坎公战队",
        "卡马逊主页",
    ]
    moveMaps = [
        (780, 360),  # 开始滑动的坐标。
        (780, 30),  # 结束滑动的坐标。
    ]
    while 1:
        photoMap = air.Photo()
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "主页" in name:
            break
        if "战队" in name:
            swipe(moveMaps[0], moveMaps[1], duration=1, steps=6)
            photoMaps.remove("坎公战队")
            photoMaps.append("问号标识二")
            continue
        touch(pos)


def pvpAuto():
    gamePages = air.Photo()
    gamePagesMap = [
        "获得活动积分",
        '坎公挑战卷不足',
        '坎公44段位更新',
        '坎公PVP确认',
        '坎公初始选人页黄',
        '坎公PVP休息',
        '坎公初始选人页重试',
        '坎公卡马逊确认',
        "坎公图标",
        "界面提示",
        "界面提示2",
        "界面提示3",
        "开始战斗",
        "pvp重试",
        "探险初始页",
    ]
    moveMaps = [
        (903, 171),  # 0 重试右上角的小齿轮
        (60, 310),  # 1 pvp竞技场
        (78, 472),  # 2 主页 → 探险页
    ]
    global flag
    flag = True
    while flag:
        gamePages.name = "默认"
        gamePages.loopSearch(gamePagesMap)
        name = gamePages.name
        pos = gamePages.pos

        if "获得活动积分".__eq__(name):
            touchFix(pos, (0, -100))
            continue

        if "坎公初始选人页重试".__eq__(name):
            # 拿偏移坐标，点一下右上角齿轮在的位置收工。
            touchFix(moveMaps[0])
            touch(pos)
        elif '坎公PVP休息'.__eq__(name):
            time.sleep(20)
        elif "不足" in name:
            touchFix(pos, (-28, 154))
            changeFlag()
            backToMain()
        elif '更新' in name:
            touchFix(pos, (3, 227))
        elif '探险初始页'.__eq__(name):
            touch(moveMaps[1])
        elif '界面提示' in name:
            touch(moveMaps[2])
        # 这里拿到了上面三选一的 名字 和XY坐标
        elif "坎公图标" in name:
            openGame()
        else:
            touch(pos)


def levelStone():
    photoMap = air.Photo()
    photoMaps = [
        '进化石扫荡',
        "进化石副本",
        "获得活动积分",
        '坎公PVP确认',
        '坎公卡马逊确认',
        '进化石扫荡',
        '自动战斗完毕',
        '进化石页面',
    ]
    moveMaps = [
        (660, 266),  # 0 点扫荡前先把进度条拉到最大。
        (660, 300),  # 1 点扫荡前先把进度条拉到最大，疑似UI改动。
        (660, 270),  # 2 点扫荡前先把进度条拉到最大，疑似UI改动。
        (656, 340),  # 3 点扫荡前先把进度条拉到最大，新UI。
    ]
    while True:
        photoMap.name = "默认"
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "扫荡" in name:
            for i in moveMaps:
                touch(i)
            time.sleep(1)

        if "获得活动积分" in name:
            touchFix(pos, (0, -100))
            continue

        if "进化石副本" in name:
            break

        touch(pos)


# 回到探险初始页
def backToMain():
    photoMap = air.Photo()
    photoMaps = [
        '坎公卡马逊确认',
        "圆形角斗场",
        "游玩指南",
        "界面提示",
        "界面提示2",
        "界面提示3",
        "界面提示4",
        '坎公初始选人页黄',
        '坎公初始选人页重试',
        '坎公卡马逊确认',
        '坎公pvp确认',
        '坎公后退',
    ]
    moveMaps = [
        (60, 310),  # pvp竞技场
    ]
    while True:
        photoMap.name = "默认"
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "初始页" in name:
            touch(moveMaps[0])
            continue

        if "界面提示" in name:
            break

        touch(pos)


def dailyAir(choice=1):
    cvInit()
    openGame()
    getEmail()
    # dailyBuy()
    dailyPoints()
    day2buyNew(choice)
    levelStone()
    backToMain()
    day2buyNewUp()
    levelUpStone()
    pvpAutoPre()
    pvpAuto()
    backToMain()


def cvInit(path=cv.kgAirPath, device=tempDevice):
    cv._init()
    cv.set_value("path", path)
    # cv.set_value("device", cv.kgDevice3)
    cv.set_value("device", device)


# 2022年9月14日10:36:32 日常购买后台化
def day2buy(choice):
    photoMaps = [
        "坎公图标",
        "进化石页面",
        "裂痕总览",
        "领取灵魂点",
        "灵魂点已领取",
        "探险初始页",
        "坎公主页面",
    ]
    photoMap = air.Photo()
    moveMaps = [
        (-422, 111),  # 0点中间的房子

        # (-834, 237), # 1主页面 → 探险初始页
        (71, 475),  # 1主页面 → 探险初始页

        # (-718, -341), # 2探险初始页 → 进化石
        (56, 140),  # 2探险初始页 → 进化石
    ]
    choiceMaps = [
        (780, 120),  # 进化石一
        (780, 290),  # 进化石二
        (780, 450),  # 进化石三
    ]
    while 1:
        photoMap.loopSearch(photoMaps)

        name = photoMap.name
        pos = photoMap.pos

        if "主页面" in name:
            touchFix(pos, moveMaps[0])
            continue

        if "初始页" in name:
            # 我以前特么是猪头还是怎么的，怎么会想到这种算偏移的法子。。？是因为之前用的不是air么。
            # touchFix(pos,moveMaps[2])
            touch(moveMaps[2])
            continue

        if "已领取" in name:
            touch(moveMaps[1])
            continue

        if "总览" in name:
            touch(choiceMaps[choice - 1])
            continue

        if "进化石" in name:
            break

        if "坎公图标" in name:
            openGame()
            continue

        touch(pos)

    # photoMap = []
    # photoMap.append(('坎公主页面', 1, -422, 111))
    # photoMap.append(('坎公主页面', 1, -258, 233))
    # photoMap.append(('坎公主页面', 1, -834, 237))
    # photoMap.append(('探险初始页', 1, -718, -341))
    # if 2 == choice:
    #     # 第二个
    #     photoMap.append(('进化石页面', 1, 636, 253))
    # elif 3 == choice:
    #     # 第三个
    #     photoMap.append(('进化石页面', 1, 600, 422))
    # elif 1 == choice:
    #     # 第一个
    #     photoMap.append(('进化石页面', 1, 624, 103))


# 日常商城购买
def dailyBuy():
    photoMaps = [
        "金币购买",
        "坎公图标",
        "坎公PVP确认",
        "金币卖完",
        "金币",
        # "问号标识二",
        "商店标识",
        "坎公主页面",
    ]
    photoMaps2 = [
        "坎公PVP确认",
        "装备",
        "锤子卖完",
        "锤子1000",
        "已购买",  # 这个有问题。
        # "坎公PVP确认",
        "强化锤",
        # "商店标识",
    ]
    photoMap = air.Photo()
    moveMaps = [
        (18, 21),  # 卡马逊左上角返回
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        # photoMap.loopSearch(photoMaps2)

        name = photoMap.name
        pos = photoMap.pos

        if "金币卖完" in name:
            touch(pos)
            photoMaps = photoMaps2
            continue

        if "锤子卖完" in name:
            touch(moveMaps[0])
            break

        if "已购买" in name:
            touchFix(pos,(0,-100))
            continue

        if "坎公图标" in name:
            openGame()
            continue

        touch(pos)


# 2023年1月22日17:09:25 坎公重开游戏。
def openGame():
    photoMap = air.Photo()
    photoMaps = [
        "坎公图标",
        "坎公图标新",
        "12提示",
        "界面提示",
        "界面提示2",
        "界面提示3",
        "界面提示4",
    ]
    moveMaps = [
        (400, 100),  # 0 随便点一个没东西的地方。
    ]
    count = 0
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "12提示".__eq__(name):
            count = 1
            touch(moveMaps[0])
            continue

        if "界面提示" in name:
            if count == 1:
                break
            else:
                count = 1
                continue

        touch(pos)


# 获取邮件 2023年1月22日17:12:18
def getEmail():
    photoMap = air.Photo()
    photoMaps = [
        '坎公卡马逊确认',
        "领取奖励",
        "全部接收并删除",
        "界面提示",
        "已全部接收",
        "界面提示1",
        "界面提示2",
        "界面提示3",
        "界面提示4",
    ]
    moveMaps = [
        (880, 25),  # 0 获取邮件内容
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "领取奖励" in name:
            touch(moveMaps[0])
            continue

        if "界面提示" in name:
            touch(moveMaps[0])
            continue

        if ("确认" in name) | ("已全部接收".__eq__(name)):
            backToStart()
            break

        touch(pos)


# 获取设计图（未做时间管理） 2023年1月22日18:09:21
def getEquipItem():
    photoMap = air.Photo()
    photoMaps = [
        "进化石扫荡",
        "选中你有通行证吗",
        "你有通行证吗",
        "指挥中心",
        "世界探索",
        "世界探险船",
        "世界探险船2",
        "界面提示",
        "界面提示2",
        "界面提示3",
        "坎公PVP确认",
    ]
    moveMaps = [
        (780, 480),  # 0 开始探索
        (640, 320),  # 1 周边扫荡拉满
    ]
    date = datetime.date.today().weekday() % 2
    # print(datetime.date.today().weekday(),date)
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "界面提示" in name:
            swipe(pos, vector=(400, 0), steps=6)
            continue

        if "指挥中心".__eq__(name):
            swipe(pos, vector=(0, -10), steps=6)
            continue

        if "选中你有通行证吗".__eq__(name):
            touch(moveMaps[0])
            continue

        if "进化石扫荡".__eq__(name):
            touch(moveMaps[1])
            time.sleep(1)
            touch(pos)
            continue

        if "坎公PVP确认".__eq__(name):
            backToStart()
            break

        touch(pos)


# 回到最开始的界面 2023年1月22日20:11:42
def backToStart():
    photoMap = air.Photo()
    photoMaps = [
        '坎公卡马逊确认',
        '坎公pvp确认',
        '坎公后退',
        "世界探险船",
        "世界探险船2",
        "界面提示",
        "界面提示2",
        "界面提示3",
    ]
    moveMaps = [
        (60, 310),  # pvp竞技场
    ]
    while True:
        photoMap.name = "默认"
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "世界探险船" in name:
            break

        if "界面提示" in name:
            break

        touch(pos)


# 获取周边 2023年1月22日20:31:06 (未完成）
def getEquipTool():
    photoMap = air.Photo()
    photoMaps = [
        '坎公卡马逊确认',
        "选择设计图",
        "开始制造",
        "周边闲置",
        "周边完成",
    ]
    moveMaps = [
        (320, 10),  # 0 周边闲置的偏移量
        (530, 140),  # 1 “开始制造”前先选择设计图。
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "周边闲置".__eq__(name):
            touchFix(pos, moveMaps[0])
            continue

        if "选择设计图".__eq__(name):
            touch(moveMaps[1])
            continue

        touch(pos)


# 2024年8月19日20:17:25，到进化石那儿。
def day2buyNew(choice=0):
    photoMaps = [
        "自动战斗设置",
        "进化石副本",
        "裂痕",
        "游玩标识",
        "坎公图标",
    ]
    photoMap = air.Photo()
    choiceMaps = [
        (250, 300),  # 0进化石,第一排第一个
        (500, 300),  # 1进化石二 第一排第二个
        (800, 300),  # 2进化石三 第一排第三个
        (250, 480),  # 3进化石四,第二排第一个
        (500, 480),  # 4进化石五 第二排第二个
        (800, 480),  # 5进化石六 第二排第三个
    ]
    while 1:
        photoMap.loopSearch(photoMaps)

        name = photoMap.name
        pos = photoMap.pos

        if "进化石" in name:
            touch(choiceMaps[choice])
            continue

        if "自动战斗设置" in name:
            levelStone()
            break

        if "坎公图标" in name:
            openGame()
            continue

        touch(pos)


# 收浮游城点，但我觉得之后肯定会有问题。 2024年8月19日
def dailyPoints():
    photoMaps = [
        "商店标识",
    ]
    photoMap = air.Photo()
    moveMaps = [
        (486, 216),  # 0点中间的房子
    ]
    while 1:
        photoMap.loopSearch(photoMaps)

        name = photoMap.name
        pos = photoMap.pos

        if "商店标识" in name:
            touch(moveMaps[0])
            break

        touch(pos)

# 移动到PVP页面。 2024年8月19日
def pvpAutoPre():
    photoMaps = [
        "站位设置",
        "决斗场背景",
        "圆形决斗场",
        "pvp",
        "游玩标识",
    ]
    photoMap = air.Photo()
    moveMaps = [
        (486, 216),  # 0点中间的房子
    ]
    while 1:
        photoMap.loopSearch(photoMaps)

        name = photoMap.name
        pos = photoMap.pos

        if "站位设置".__eq__(name):
            break

        touch(pos)


# 2025年3月21日，到进化石那儿，给觉醒用的,更新了一下，给PVP用。
def day2buyNewUp(choice = 1):
    photoMaps = [
        "觉醒扫荡",
        "资源觉醒",
        "自动战斗设置",
        "进化石副本",
        "裂痕",
        "游玩标识",
        "坎公图标",
    ]
    photoMap = air.Photo()
    while 1:
        photoMap.loopSearch(photoMaps)

        name = photoMap.name
        pos = photoMap.pos

        if "觉醒扫荡" in name:
            # levelUpStone()
            break

        if "坎公图标" in name:
            openGame()
            continue

        touch(pos)

def levelUpStone():
    photoMap = air.Photo()
    photoMaps = [
        '进化石扫荡',
        "觉醒扫荡",
        "进化石副本",
        "获得活动积分",
        '坎公PVP确认',
        '坎公卡马逊确认',
        '自动战斗完毕',
        'pvp',
    ]
    while True:
        photoMap.name = "默认"
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        # if "扫荡" in name:
        #     for i in moveMaps:
        #         touch(i)
        #     time.sleep(1)

        if "获得活动积分" in name:
            touchFix(pos, (0, -100))
            continue

        if "进化石副本" in name:
            break

        if "pvp" in name:
            break

        touch(pos)

if __name__ == "__main__":
    # touchFix((3,4),(5,6))
    # returnKmx()
    # chooseEquip()
    # question()
    # shop()
    # fullAutoKmx()
    # searchPage()
    # team()
    # pvpAuto()
    # levelStone()
    # backToMain()
    # dailyAir()
    # dailyAir(3) #小号
    # dailyAir(1)  # 大号
    # dailyBuy()
    # openGame()
    # getEmail()
    # backToStart()
    # getEquipItem()
    # getEquipTool()
    # levelStone()
    # levelStone()
    # backToMain()
    # pvpAuto()
    # openGame()
    # getEmail()
    # dailyBuy()
    # dailyPoints()
    # day2buyNew()
    # levelStone()
    # backToMain()
    # pvpAutoPre()
    # pvpAuto()
    # day2buyNewUp()
    # levelUpStone()
    backToMain()
