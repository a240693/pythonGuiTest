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

# poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

# auto_setup(__file__, devices=[cv.device])


spaceFlag = False

flag = True

continueFlag = False

appleFlag = True

__author__ = "user"

cv._init()


def enterGame():
    photoMap = air.Photo()
    photoMaps = [
        "fgo",
        "迦勒底之门",
        "关闭公告",
        "奖品重置关闭",
        "续关进入",
        "攻击",
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

            if "迦勒底" in name:
                # changeFlag(False, False)
                dailyExpNew()
                break

            if "攻击" in name:
                break

            # 用包体名启动，不需要点图片了。
            if "fgo".__eq__(name):
                start_app(package="com.bilibili.fatego", activity="UnityPlayerNativeActivity")
                changeFlag(True)
                waitEnterGame()
                continue

            touch(pos)


    except Exception as e:
        return 0
    # finally:
    #     # generate html report
    #     simple_report(__file__)


# 进入游戏
def waitEnterGame():
    photoMaps = [
        "关闭公告",
        "续关进入",
    ]
    moveMaps = [
        (54, 52),
    ]
    photoMap = air.Photo()
    switch = True
    while switch:
        for i in photoMaps:
            if photoMap.appearThenClick(i):
                if "卡了".__eq__(photoMap.name):
                    stop_app(package="com.bilibili.fatego")
                switch = False
                break
        if switch:
            for i in range(1, 10):
                print("点击第{}次".format(i))
                touch(moveMaps[0])
                time.sleep(3)
            photoMaps.append("卡了")


def battle():
    turn = 1
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
        (486, 152),  # 二宝具
        (310, 152),  # 一宝具
        (98, 376),  # 卡1
        (657, 152),  # 三宝具
        (289, 376),  # 卡2
        (489, 376),  # 卡3
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
            if turn == 3:
                photoMaps.insert(0, "小芬奇3")
            photoMap.loopSearch(photoMaps)
            pos = photoMap.pos
            name = photoMap.name
            # 如果读取到战斗界面就选卡，不点击直接跳过。

            if "界面" in name:
                print("第{}回合，开始选择指令卡。".format(turn))
                # 加容错，给宝具卡动画读取时间.
                time.sleep(2)
                for step in actionMaps:
                    touch(step)
                # 打完之后休息15秒，看宝具动画什么的。
                time.sleep(15)
                turn += 1
                continue

            if "已使用" in name:
                pos = moveMaps[0]
                photoMaps.remove("技能2")

            if "战斗结果" in name:
                # 多按一下，加快结算速度。
                # 太快了，等一下。
                touch(pos)
                time.sleep(1)

            # print("找到的是{},坐标是{}".format(name, pos))
            touch(pos)

            if "小芬奇" in name:
                photoMaps.remove("小芬奇3")

            if "关闭" in name:
                break

            if "结束" in name:
                break

            if "连续" in name:
                eatApple()
                break

    except Exception as e:
        return e
    # finally:
    #     # generate html report
    #     simple_report(__file__, logpath=True)


# 用来敲空格的线程。
def spaceClick():
    while 1:
        print("spaceFlag:".format(spaceFlag))
        while spaceFlag:
            # print("click Q")
            touch((100, 100))
            time.sleep(3)
        time.sleep(3)


# 进入游戏双线程，留一个敲空格。
def mulFeatures(thread1, thread2):
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


def changeFlag(switchSF=False, switchF=True, switchCF=False, switchAp=True):
    # 进游戏要不要一直点击左边的开关。
    global spaceFlag
    spaceFlag = switchSF
    # 控制进程的开关。
    global flag
    flag = switchF
    # 打完后是续关还是退出的开关。
    global continueFlag
    continueFlag = switchCF
    # 没体力了是否吃苹果开关。
    global appleFlag
    appleFlag = switchAp


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


def eatApple():
    photoMap = air.Photo()
    photoMaps = [
        "金苹果",
        "银苹果",
        "苹果确定",
        "狂阶",
    ]

    while True:
        try:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos
            if "苹果" in name:
                # 苹果按钮关了的话就只续关不吃苹果。
                if not appleFlag:
                    changeFlag(switchCF=False)
                    photoMaps = ["苹果关闭"]
                    continue
            if "狂阶" in name:
                break
            touch(pos)
            if ("确定" in name) | ("关闭" in name):
                break
        except Exception as e:
            return 0
    # support()


# 2022-06-30 20:28:02 跳过剧情。
def skipStory():
    photoMap = air.Photo()
    photoMaps = [
        "跳过剧情",
        "剧情页标",
    ]
    moveMaps = [
        (900, 27),  # 跳过剧情里面的跳过按钮。
    ]
    while True:
        try:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos
            if "页标" in name:
                touch(moveMaps[0])
            else:
                touch(pos)
        except Exception as e:
            return 0


def wCaber():
    count = 0
    count2 = 0
    photoMap = air.Photo()
    photoMaps = [
        "小芬奇1",
        "技能选择对象",
    ]
    backPhotoMaps = [
        "C呆1技能",
        "C呆3技能",
        "C呆2技能",
    ]
    moveMaps = [
        (220, 339),  # 选择对象，选一号位。
    ]
    while True:
        try:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos
            if "对象" in name:
                count2 += 1
                touch(moveMaps[0])
            elif "小芬奇" in name:
                touch(pos)
                photoMaps.remove("小芬奇1")
                photoMaps = photoMaps + backPhotoMaps
            else:
                count += 1
                print("技术使用次数为：{}".format(count))
                touch(pos)
            if (count > 5) & (count2 > 3):
                battle()
                break
        except Exception as e:
            return 0


def support():
    photoMap = air.Photo()
    photoMaps = [
        "C呆技能组",
        "开始任务",
        "攻击",
        "跳过剧情",
        "对话框",
    ]
    moveMaps = [
        (888,28), # 对话跳过
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos

        if "对话" in name:
            touch(moveMaps[0])
            continue

        if "攻击" in name:
            break

        touch(pos)

        if "开始" in name:
            time.sleep(10)
            continue



def battleStart():
    changeFlag(switchCF=True)
    global continueFlag
    count = 1
    while 1:
        print("第{}回合开始=========".format(count))
        wCaber()
        if continueFlag == True:
            print("第{}回合结束，第{}回合开始选支援=====".format(count, count + 1))
            count += 1
            support()


def egg10(pos=(338, 350)):
    photoMap = air.Photo()
    count = 0
    photoMaps = [
        # "奖品重置执行",
        "奖品重置关闭",
        "重置奖品",
        "抽奖10",
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        if "关闭" in name:
            count += 1
        elif "重置" in name:
            changeFlag(switchF=False)
        elif "抽奖" in name:
            touch(pos, times=250)
            continue
        touch(pos)


def selectSkill(skill=[10]):
    photoMap = air.Photo()
    photoMaps = [
        "技能选择对象",
        "攻击",
        "战斗结果",
    ]
    skillMaps = [
        # 技能图标1-9,每三个是一个人物
        (52, 436),
        (125, 436),
        (190, 436),
        (290, 436),
        (360, 436),
        (420, 436),
        (530, 436),
        (600, 436),
        (670, 436),
    ]
    moveMaps = []
    tagetMaps = [
        (220, 339),  # 选择对象，选一号位。
    ]
    # 10就不开技能，直接跳过释放段。
    if skill[0] == 10:
        return 0
    for i in skill:
        moveMaps.append(skillMaps[i - 1])
    for index, i in enumerate(moveMaps):
        while 1:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            if "战斗结果" in name:
                exitBattle()
                return 0
            if "对象" in name:
                touch(tagetMaps[0])
            if "攻击" in name:
                break
        print("正在释放第{}个技能。".format(index + 1))
        touch(i)
        time.sleep(0.3)
        if i == moveMaps[-1]:
            while 1:
                photoMap.loopSearch(photoMaps)
                name = photoMap.name
                if "对象" in name:
                    touch(tagetMaps[0])
                break


# 作废了，用新的selectSkill
def firstTurnSkill():
    count = 0
    count2 = 0
    photoMap = air.Photo()
    photoMaps = [
        "小芬奇1",
        "技能选择对象",
    ]
    backPhotoMaps = [
        "C呆1技能",
        "C呆3技能",
        "C呆2技能",
    ]
    moveMaps = [
        (220, 339),  # 选择对象，选一号位。
    ]
    while True:
        try:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos
            if "对象" in name:
                count2 += 1
                touch(moveMaps[0])
            elif "小芬奇" in name:
                touch(pos)
                photoMaps.remove("小芬奇1")
                photoMaps = photoMaps + backPhotoMaps
            else:
                count += 1
                print("技术使用次数为：{}".format(count))
                touch(pos)
            if (count > 2) & (count2 > 0):
                onlyBattle()
                break
        except Exception as e:
            return 0


# 作废了，用新的selectSkill
def oneCaber(skill1=0, skill2=0, skill3=0):
    count = 0
    count2 = 0
    limit = 0
    limit2 = 0
    photoMap = air.Photo()
    photoMaps = [
        "技能选择对象",
    ]
    moveMaps = [
        (220, 339),  # 选择对象，选一号位。
    ]
    if skill1 == 1:
        photoMaps.append("C呆1技能")
        limit += 1
    if skill3 == 1:
        photoMaps.append("C呆3技能")
        limit += 1
        limit2 += 1
    if skill2 == 1:
        photoMaps.append("C呆2技能")
        limit += 1
        limit2 += 1
    while True:
        try:
            photoMap.loopSearch(photoMaps)
            name = photoMap.name
            pos = photoMap.pos
            if "对象" in name:
                count2 += 1
                touch(moveMaps[0])
            else:
                count += 1
                print("技术使用次数为：{}".format(count))
                touch(pos)
            if (count >= limit) & (count2 >= limit2):
                onlyBattle()
                break
        except Exception as e:
            return 0


def onlyBattle(turn=1):
    photoMap = air.Photo()
    photoMaps = [
        "攻击",
        "战斗界面",
        "战斗界面2",
        "战斗结果",
        "报酬",
    ]
    actionMaps = [
        (310, 152),  # 一宝具
        (486, 152),  # 二宝具
        (98, 376),  # 卡1
        (657, 152),  # 三宝具
        (289, 376),  # 卡2
        (489, 376),  # 卡3
    ]

    moveMaps = [
        (324, 319),  # 技能已使用的取消按钮位置。
    ]
    skillUse = 0
    try:
        while 1:
            photoMap.loopSearch(photoMaps)
            pos = photoMap.pos
            name = photoMap.name

            # 额外放技能试做。
            if ("攻击" in name) & (skillUse == 0):
                if turn == 6 :
                    selectSkill([5,8])
                if turn == 7 :
                    selectSkill([1,4,6,7,9])
                skillUse = 1

            # 如果读取到战斗界面就选卡，不点击直接跳过。
            if "界面" in name:
                print("第{}回合，开始选择指令卡。".format(turn))
                for step in actionMaps:
                    touch(step)
                time.sleep(7)
                if turn <= 2:
                    break
                if turn > 2:
                    skillUse = 0
                    turn += 1

            # print("找到的是{},坐标是{}".format(name, pos))
            touch(pos)
            if ("战斗结果" in name) | ("报酬" in name):
                exitBattle()
                break

    except Exception as e:
        return e


def masterSkill():
    photoMap = air.Photo()
    photoMaps = [
        "御主技能",
        "技能选择对象",
    ]
    moveMaps = [
        (220, 339),  # 选择对象，选一号位。
        (744, 230),  # 选择二号技能。
    ]
    try:
        while 1:
            photoMap.loopSearch(photoMaps)
            pos = photoMap.pos
            name = photoMap.name
            # 如果读取到战斗界面就选卡，不点击直接跳过。

            if "对象" in name:
                touch(moveMaps[0])

            if "攻击" in name:
                break

            touch(pos)

            if "技能" in name:
                time.sleep(0.5)
                touch((744, 230))
                photoMaps.remove("御主技能")
                photoMaps.insert(1, "攻击")
    except Exception as e:
        return e


def exitBattle():
    photoMap = air.Photo()
    photoMaps = [
        "战斗结果",
        "战斗结束",
        "羁绊等级提升",
        "跳过剧情",
        "对话框",
        "菜单",
    ]
    moveMaps = [
        (888, 28),  # 点击跳过剧情。
    ]
    changeFlag(switchF=False)
    if continueFlag:
        photoMaps.append("续关连续")
    else:
        photoMaps.append("续关关闭")
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        pos = photoMap.pos
        # print("找到的是{},坐标是{}".format(name, pos))
        if "对话" in name:
            touch(moveMaps[0])
            continue

        if "菜单" in name:
            break

        touch(pos)

        if "关闭" in name:
            break

        if "连续" in name:
            eatApple()
            break

        if ("结束" in name) & (not continueFlag):
            break


def level90plus(turn=1):
    skill1 = [1, 6, 7, 8, 9]
    skill2 = [3, 5, 6]
    skill3 = [4]
    skillMaps = []
    skillMaps.append(skill1)
    skillMaps.append(skill2)
    skillMaps.append(skill3)
    while 1:
        selectSkill(skillMaps[turn - 1])
        if turn == 3:
            masterSkill()
        onlyBattle(turn)
        # 第三回合判定就不在这里了，在onlyBattle里
        # 打完了返回到要选助战才会回到这儿。
        if turn >= 3:
            break
        turn += 1


def level90plus(turn=1):
    skill1 = [1, 6, 7, 8, 9]
    skill2 = [3, 5, 6]
    skill3 = [4]
    skillMaps = []
    skillMaps.append(skill1)
    skillMaps.append(skill2)
    skillMaps.append(skill3)
    while 1:
        selectSkill(skillMaps[turn - 1])
        if turn == 3:
            masterSkill()
        onlyBattle(turn)
        # 第三回合判定就不在这里了，在onlyBattle里
        # 打完了返回到要选助战才会回到这儿。
        if turn >= 3:
            break
        turn += 1


def level90(turn=1):
    skill1 = [1, 4, 5, 6, 7, 8, 9]
    skill2 = [10]
    skill3 = [3]
    skillMaps = []
    skillMaps.append(skill1)
    skillMaps.append(skill2)
    skillMaps.append(skill3)
    global flag
    flag = True
    while flag:
        selectSkill(skillMaps[turn - 1])
        if turn == 3:
            masterSkill()
        onlyBattle(turn)
        # 第三回合判定就不在这里了，在onlyBattle里
        # 打完了返回到要选助战才会回到这儿。
        if turn >= 3:
            break
        turn += 1


def battleStartNew(switchCF=True, switchAp=True, select=1):
    changeFlag(switchCF=switchCF, switchAp=switchAp)
    global continueFlag
    count = 1
    while (continueFlag) | (count == 1):
        print("第{}回合开始=========".format(count))
        if select == 1:
            level90plus()
        elif select == 2:
            level90()
        else:
            level90plus()
        if continueFlag:
            print("第{}回合结束，第{}回合开始选支援=====".format(count, count + 1))
            support()
        count += 1


def custom(turn=1):
    skill1 = [10]
    skill2 = [10]
    skill3 = [7,8,9]
    skillMaps = []
    skillMaps.append(skill1)
    skillMaps.append(skill2)
    skillMaps.append(skill3)
    while 1:
        selectSkill(skillMaps[turn - 1])
        # 种火特化，暂时不扔御主技能。
        # if turn == 2:
        #     masterSkill()
        onlyBattle(turn)
        # 第三回合判定就不在这里了，在onlyBattle里
        # 打完了返回到要选助战才会回到这儿。
        if turn >= 3:
            break
        turn += 1


# 每日任务改
def dailyExpNew(switchCF=True, switchAp=False):
    photoMap = air.Photo()
    photoMaps = [
        "迦勒底之门",
        "每日任务",
        "种火40",
        "宝石翁",
        "狂阶",
        "开始任务",
        "攻击",
        "续关连续",
        "种火超量",
    ]
    moveMaps = [
        (943, 136),  # 滑动起点。
        (943, 282),  # 每日滑动终点
        (943, 177),  # 种火滑动。
    ]
    changeFlag(switchCF=switchCF, switchAp=switchAp)
    try:
        while continueFlag:
            photoMap.loopSearch(photoMaps)
            pos = photoMap.pos
            name = photoMap.name
            if "攻击" in name:
                custom(1)
                continue
                # break
            if "超量" in name:
                break
            touch(pos)



    except Exception as e:
        return 0

# 自动强化
def autoLevelUp():
    photoMap = air.Photo()
    photoMaps = [
        "种火用尽",
        "已放入种火",
        "种火确定",
        "推荐选择",
        "灵基再临",
        "圣杯转临",
        "强化结果",
    ]
    moveMaps = [
        (850,500) , # 放入种火后点确定。
        (490,30), # 没用的地方
    ]
    changeFlag(switchF=True)
    print("自动强化开始。")
    while flag:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        if "放入" in name:
            touch(moveMaps[0])
            continue
        if ("转临" in name) | ("用尽" in name) :
            break
        touch(pos)
        if "再临" in name:
            autoAdd()
            continue

# 自动灵基再临。
def autoAdd():
    photoMap = air.Photo()
    photoMaps = [
        "种火确定",
        "已放入种火",
        "上限解放",
        "强化从者",
        "新技能",
        "已开放"
        "灵基再临",
        "幕间物语",
        "强化关卡",
    ]
    moveMaps = [
        (850, 500),  # 放入种火后点确定。
    ]
    changeFlag(switchF=True)
    print("自动灵基再临开始。")
    while flag:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name
        if "放入" in name:
            touch(moveMaps[0])
            continue
        touch(pos)
        if "从者" in name:
            break

def enterStrong(switchF = True,switchAp=True):
    photoMap = air.Photo()
    photoMaps = [
        "金苹果",
        "狂阶",
        "菜单",
        "宝具强化",
        "报酬",
        "技能强化",
        "种火用尽",
    ]
    moveMaps = [
        (750, 150),  # 回到主页面后点击第一关。
    ]
    changeFlag(switchF=switchF,switchAp=switchAp)
    while flag:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if ("苹果" in name) & (switchAp):
            eatApple()
            continue
        elif ("苹果" in name) & (not switchAp):
            break

        if "狂阶" in name:
            support()
            level90()
            continue

        if "菜单" in name:
            touch(moveMaps[0])
            continue

        touch(pos)

def enterSideStory(switchF = True,switchAp=True):
    photoMap = air.Photo()
    photoMaps = [
        "金苹果",
        "狂阶",
        "关卡前选人",
        "跳过剧情",
        "对话框",
        "幕间物语进入",
        "幕间物语进入二",
        # "菜单",
        "宝具强化",
        "报酬",
        "技能强化",
        "种火用尽",
        "攻击",
        "开始任务",
        "幕间物语返回",
        "fgo",
    ]
    moveMaps = [
        (750, 150),  # 回到主页面后点击第一关。
        (888,28), # 点击跳过。
    ]
    changeFlag(switchF=switchF,switchAp=switchAp)
    # 拿来应急的。
    count = 0
    times = 3
    # while count < times :
    while 1:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if ("苹果" in name) & (switchAp):
            eatApple()
            continue
        elif ("苹果" in name) & (not switchAp):
            break

        if "狂阶" in name:
            support()
            level90()
            count += 1
            continue

        if "菜单" in name:
            touch(moveMaps[0])
            continue

        if "对话" in name:
            touch(moveMaps[1])
            continue

        if "攻击" in name:
            level90()
            count += 1
            continue

        if "fgo".__eq__(name):
            enterGame()
            continue

        touch(pos)

def dialogue():
    photoMap = air.Photo()
    photoMaps = [
        "跳过剧情",
        "对话框",
        "攻击",
    ]
    moveMaps = [
        (888,28),  # 回到主页面后点击第一关。
    ]
    while flag:
        photoMap.loopSearch(photoMaps)
        pos = photoMap.pos
        name = photoMap.name

        if "对话" in name:
            touch(moveMaps[0])
            continue

        if "攻击" in name:
            break

        if "菜单" in name:
            break

        touch(pos)

if __name__ == "__main__":
    # enterGame()
    # mulFeatures(enterGame,spaceClick)
    # dailyExp()
    # battle()
    # eatApple()
    # mulFeatures(egg10,touchPrize)
    # touchPrize()
    # egg10()
    # battleStart()
    # masterSkill()
    # selectSkill([1,3])
    # firstTurnSkill()
    # masterSkill()
    # oneCaber(0,1,1)
    # battleStartNew(False, False, 2)
    # egg10()
    # battleStartNew(True, select = 2)
    # custom()
    # enterGame()
    # dailyExpNew()
    # dailyExpNew(True, True)
    # autoLevelUp()
    # autoAdd()
    # dailyExpNew(True, False)
    # enterStrong()
    # waitEnterGame()
    enterSideStory()