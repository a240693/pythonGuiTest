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
        (134, 327),  # 4,弓香菜活动普通。
        (129, 185),  # 6,弓香菜活动普通。
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
            continue

        if "pcr小小号".__eq__(name):
            count = 2
            playerTempMaps = photoMaps
            continue

        if "pcr小号".__eq__(name):
            count = 1
            playerTempMaps = photoMaps
            continue

        if "账号登录".__eq__(name):
            # 大号0 小号1 小小号2
            dailyMission(count)
            break

# 日常入口
# 2023年5月8日20:06:59
def dailyMission(count,bug = False):
    enterGame()
    dailyKokoro()
    # getMana()
    # 为了以后抽免费十连，还是要的。
    dailyEgg()
    # get10Power()
    # dailyClan()
    # dailyExp()
    # dailyUnderCity()
    if bug == False :
        dailyJJC()
        if count != 2:
            dailyPJJC()
    getMission()
    getGift()

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
        "赛跑收取",
        "竞赛开始",
        "附奖扭蛋",
        "开局扭蛋",
        "确认",
        "关闭",
        "跳过",
        "登录活动",
        "碎片10",
        "好感度跳过",
        "庆典举办中",
        "庆典举办中2",
        "pcr主页",
        "菜单",
        "pcr对话框一",
        "pcr对话框二",
        "钻石",
        "特别庆典扭蛋",
        "特别扭蛋",
        "举办中",
    ]
    moveMaps = [
        (786,311), # 0 赛跑，选最右边.
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "竞赛开始".__eq__(name):
            touch(moveMaps[0])
            sleep(1)
            touch(pos)
            continue

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
        "取消",
        "关闭",
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
        "探索首页",
        "返回",
        "确认",
        "主页",
        "pcr主页",
        "取消",
        "关闭",
        "关闭2",
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
        "附奖",
        "转蛋点击",
        "关闭",
        "扭蛋选择",
        "扭蛋完成抽取",
        "白色确认",
        "确认",
        "转蛋免费1",
        "转蛋免费",
        "转蛋普通",
        "转蛋普通2",
        "转蛋普通3",
        "每日转蛋",
        "好感度跳过",
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
        "关闭",
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

# 探索 2023年5月22日22:52:57
def dailyExp():
    photoMap = air.Photo()
    photoMaps = [
        "探索已完成",
        "探索首页",
        "前往玛娜关卡",
        "使用跳过卷",
        "经验11级",
        "经验值关卡",
        "探索",
        "冒险",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "使用跳过卷".__eq__(name):
            autoSkipBattle()
            continue

        if ("探索首页".__eq__(name))|("探索已完成".__eq__(name)):
            backToMain()
            break

        touch(pos)

# 自动跳过（共用） 2023年5月22日23:06:50
def autoSkipBattle(times = 1):
        photoMap = air.Photo()
        photoMaps = [
            "探索已完成",
            "扫荡完成",
            "确认",
            "使用跳过卷",
        ]
        moveMaps = [
            (880, 330),  # 先点五次
        ]
        while 1:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos

            if "使用跳过卷".__eq__(name):

                for i in range(times) :
                    touch(moveMaps[0])

                touch(pos)
                continue

            if ("扫荡完成".__eq__(name)) | ("探索已完成".__eq__(name)):
                break

            touch(pos)

# 地下城 2023年5月22日23:26:28
def dailyUnderCity():
    photoMap = air.Photo()
    photoMaps = [
        "地下城已完成",
        "扫荡完成",
        "地下城跳过",
        "极难3",
        "地下城",
        "冒险",
    ]

    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if ("扫荡完成".__eq__(name)) | ("地下城已完成".__eq__(name)):
            backToMain()
            break

        touch(pos)

# 日常心碎 2023年5月22日23:45:30
def dailyHeart():
    photoMap = air.Photo()
    photoMaps = [
        "使用跳过卷",
        "3级",
        "心碎",
        "心碎星球杯",
        "冒险",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "使用跳过卷".__eq__(name):
            autoSkipBattle(5)
            continue

        if ("扫荡完成".__eq__(name)) | ("地下城已完成".__eq__(name)):
            backToMain()
            break

        touch(pos)

# 日常任务 2023年8月6日18:21:41
def getMission():
    photoMap = air.Photo()
    photoMaps = [
        "收取结束3",
        "收取结束2",
        "收取结束",
        "关闭",
        "全部收取",
        "任务",
        "白色确认",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "收取结束" in name:
            backToMain()
            break

        touch(pos)

# 日常礼物 2023年8月6日18:21:35
def getGift():
    photoMap = air.Photo()
    photoMaps = [
        "礼物收取结束",
        "持有上限",
        "关闭",
        "确认",
        "全部收取",
        "礼物",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "收取结束" in name:
            backToMain()
            break

        if "持有上限" in name:
            backToMain()
            break

        touch(pos)

# 日常JJC
# 2023年8月6日19:07:07
def dailyJJC():
    count = 0;
    photoMap = air.Photo()
    photoMaps = [
        "JJC已收取",
        # "竞技场入口",
        "白色确认",
        "JJC收取",
        "取消",
        "JJC",
        "冒险",
        "战斗开始",
    ]
    photoMapsNext = [
        "JJC已打",
        "JJC下一步",
        "白色确认",
        "JJC跳过",
        "战斗开始",
        "队伍编组",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        # photoMap.loopSearch(photoMapsNext)
        name = photoMap.name
        pos = photoMap.pos

        if (("JJC已收取" in name) | ("战斗开始".__eq__(name))) & (count == 0):
            photoMaps = photoMapsNext
            count = 1
            continue

        if "JJC已打".__eq__(name):
            backToMain()
            break

        touch(pos)

# 日常PJJC
# 2023年8月6日19:08:45
def dailyPJJC():
    count = 0;
    photoMap = air.Photo()
    photoMaps = [
        "JJC已收取",
        # "竞技场入口",
        "白色确认",
        "JJC收取",
        "取消",
        "PJJC",
        "冒险",
        "战斗开始",
    ]
    photoMapsNext = [
        "JJC已打",
        "JJC下一步",
        "战斗开始",
        "PJJC队伍",
        "白色确认",
        "PJJC总战力",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        # photoMap.loopSearch(photoMapsNext)
        name = photoMap.name
        pos = photoMap.pos

        if (("JJC已收取" in name) | ("战斗开始".__eq__(name))) & (count == 0):
            photoMaps = photoMapsNext
            count = 1
            continue

        if "JJC已打".__eq__(name):
            backToMain()
            break

        touch(pos)

# 日常日程表
# 2024年4月16日22:14:37
def dailyKokoro():
    count = 0;
    photoMap = air.Photo()
    photoMaps = [
        "日常结束",
        "公会点赞标识",
        "确认",
        "白色确认",
        "一键自动",
        "日程表",
        "关闭",
    ]
    moveMaps =[
        (460,360), # 0，确认在前，公会点赞不行，在后，地下城不行，真菜。
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        # photoMap.loopSearch(photoMapsNext)
        name = photoMap.name
        pos = photoMap.pos

        if "日常结束".__eq__(name):
            backToMain()
            break

        if "公会点赞标识".__eq__(name):
            touch(moveMaps[0])
            continue

        touch(pos)

def dailyMissionTest():
    dailyKokoro()
    dailyEgg()
    dailyJJC()
    # dailyPJJC()
    getMission()
    getGift()


if __name__ == "__main__":
    # startBattle()
    # autoFight()
    # dailyMission(0)
    # closeGame()
    # get10Power()
    # enterGame()
    # backToMain()
    # dailyClan()
    # openGame()
    # dailyHeart()
    dailyMission(2)