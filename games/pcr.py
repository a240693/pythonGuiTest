import pyautogui as py
import time
import random

from dao import dao, daoImpl, multiphotos, resultMap
from dao import  changeVar as cv
import _thread

flag = True
eventSwitch = False # 活动开关
dailyEventNo = 7

cv._init()
cv.set_value("path", cv.path)

result = resultMap.resultMap()
resultCode = 0
resultMessage = "错误"


def pcrUnderEX2():
    floor = 2
    while floor < 6:
        daoImpl.searchPhoto('{}层'.format(floor), 1)
        daoImpl.searchPhoto('挑战', 1)
        daoImpl.searchPhoto('战斗开始', 1)
        if floor == 5:
            py.keyDown('3')
        time.sleep(20)
        daoImpl.searchPhoto('下一步', 1)
        if floor == 5:
            py.keyUp('3')
        daoImpl.searchPhoto('地下城确认', 1)
        floor = floor + 1


def pcrUnderEX3(switch):
    floor = 2
    if floor == 2:
        dao.searchPhotoPcr('下一步EX3', 3, -71, 402)
        dao.searchPhotoPcr('地下城确认EX3', 3, 1, 400)
    while floor < 5:
        daoImpl.searchPhoto('{}层EX3'.format(floor), 1)
        dao.searchPhotoPcr('挑战EX3', 3, 3, 39)
        # 中号不需要3层换人。
        if (floor == 3) & (switch == 1):
            dao.searchPhotoPcr('战斗开始界面定标1EX3', 3, 211, -271)
            changeTeam5(5)
        dao.searchPhotoPcr('战斗开始界面定标1EX3', 3, 182, 93)
        # if (floor == 4) :
        #     dao.searchPhotoPcr('地下城取消AUTO', 3, 9, 395)
        time.sleep(20)
        floor = floor + 1
        dao.searchPhotoPcr('下一步EX3', 3, -71, 402)
        dao.searchPhotoPcr('地下城确认EX3', 3, 1, 400)
        if (floor == 5) & (switch == 1):
            battleFloor5()
            break
    if switch == 0:
        dao.searchPhotoPcr('地下城撤退', 1, 0, 0)
        dao.searchPhotoPcr('地下城撤退确认', 3, 118, 121)
        dao.searchPhotoPcr('主页', 1, 0, 0)
    elif switch == 1:
        dao.searchPhotoPcr('主页', 1, 0, 0)


def autoMap():
    count = 0
    while True:
        if 0 != daoImpl.searchPhotoOnce('自动推图蓝', 3):
            time.sleep(0.1)
        elif 0 != daoImpl.searchPhotoOnce('自动推图蓝2', 3):
            time.sleep(0.1)
        elif 0 != daoImpl.searchPhotoCountsPcr('推图挑战4', - 39, 124, 3, 1):
            time.sleep(0.1)
        # elif 0 != daoImpl.searchPhotoOnce('推图挑战', 3) :
        #     time.sleep(0.1)
        # elif 0 != daoImpl.searchPhotoOnce('推图挑战2', 3) :
        #     time.sleep(0.1)
        # elif 0 != daoImpl.searchPhotoOnce('推图挑战3', 3) :
        #     time.sleep(0.1)
        elif 0 != daoImpl.searchPhotoOnce('战斗开始推图', 3):
            time.sleep(0.1)
        elif 0 != daoImpl.searchPhotoOnce('推图下一步', 3):
            time.sleep(0.1)
        elif 0 != daoImpl.searchPhotoOnce('推图下一步2', 3):
            time.sleep(0.1)
        else:
            count = count + 1
        if count >= 5:
            print("找不到5次，休息两秒")
            time.sleep(2)
            count = 0


def autoMapNew():
    gamePages = multiphotos.Photo()
    while flag:
        gamePages.name = "默认"
        gamePages.x = 0
        gamePages.y = 0
        gamePagesMaps = ['推图挑战4', '战斗开始推图', '推图下一步', '胜利页下一步']
        gamePages.loopSearch(gamePagesMaps)
        # 这里拿到了上面三选一的 名字 和XY坐标
        if ("推图挑战4".__eq__(gamePages.name)):
            selfNewXY(gamePages, -42, 119)
        elif ("战斗开始推图".__eq__(gamePages.name)):
            selfNewXY(gamePages, 369, 61)
        elif ("推图下一步".__eq__(gamePages.name)):
            selfNewXY(gamePages, -76, 398)
        elif ("胜利页下一步".__eq__(gamePages.name)):
            selfNewXY(gamePages, 296, 347)
        daoImpl.moveToPcr(gamePages.x, gamePages.y, 3)


def autoMapFullAuto():
    gamePages = multiphotos.Photo()
    count = 0
    while True:
        flag = 0
        gamePages.name = "默认"
        gamePages.x = 0
        gamePages.y = 0
        gamePagesMaps = [
            'pcr已攻略',
            '推图挑战4',
            '推图下一步',
            'PCR信赖章节取消',
            '战斗开始推图',
            '胜利页下一步',
            '活动主页',
            '限时商店',
            'pcr好感',
            '剧情',
            '主页',
            'pcr升级确认',
            '推图挑战',
        ]
        gamePages.loopSearch(gamePagesMaps)
        # 这里拿到了上面三选一的 名字 和XY坐标
        if ("推图挑战4".__eq__(gamePages.name) | ("推图挑战".__eq__(gamePages.name))):
            selfNewXY(gamePages, -42, 119)
            flag = 1
        elif ("战斗开始推图".__eq__(gamePages.name)):
            selfNewXY(gamePages, 369, 61)
        elif ("推图下一步".__eq__(gamePages.name)):
            selfNewXY(gamePages, -76, 398)
        elif ("胜利页下一步".__eq__(gamePages.name)):
            selfNewXY(gamePages, 337, 341)
        elif ("限时商店".__eq__(gamePages.name)):
            selfNewXY(gamePages, 20, 108)
        elif ("PCR信赖章节取消".__eq__(gamePages.name)):
            selfNewXY(gamePages, -105, 52)
        elif '活动主页'.__eq__(gamePages.name) | '主页'.__eq__(gamePages.name):
            break;
        elif 'pcr已攻略'.__eq__(gamePages.name):
            selfNewXY(gamePages, 740, -191)
            if (count == 1):
                changeFlag()
                break
            count += 1
        daoImpl.moveToPcr(gamePages.x, gamePages.y, 3)
        if flag == 1:
            time.sleep(10)


def selfNewXY(gamePages, x, y):
    gamePages.x += x
    gamePages.y += y


def setFlag():
    count = 300
    while count != 0:
        count -= 20
        print("还剩下{}秒".format(count))
        time.sleep(20)
    changeFlag()


def changeFlag():
    global flag
    flag = False


def autoMapEnter():
    try:
        global flag
        flag = True
        _thread.start_new_thread(autoMapNew, ())
        _thread.start_new_thread(setFlag, ())
    except:
        print("Error: 无法启动线程")

    while 1:
        if flag == False:
            break
        pass


# 2022年4月27日13:57:43 修改进入游戏的逻辑
def open(choice):
    # 开雷电多开器
    daoImpl.searchPhoto('1', 2)
    if 1 == choice:
        daoImpl.searchPhotoOpen('240693')
    elif 0 == choice:
        daoImpl.searchPhotoOpen('183')
    # 开pcr
    daoImpl.searchPhoto('pcr', 5)
    time.sleep(10)
    enterGamePcr(choice)
    # daoImpl.enterGamePcr("pcr开始", 0, 0)
    # daoImpl.enterGamePcr('主界面关闭', 356, 223)
    # daoImpl.searchPhoto('button', 1)  # 开操作录制
    # dao.searchPhotoPcr('大号日常', 3, 375, 2)


def enterGamePcr(choice):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "pcr开始",
        '主界面关闭',
        '主页商店',
        'pcr竞赛开始',
    ]
    while True:
        photoMap.firstClickSearch(photoMaps)
        if '主界面关闭'.__eq__(photoMap.name):
            dao.moveToPcr(photoMap.x, photoMap.y, 1)
        elif '主页商店'.__eq__(photoMap.name):
            break
        else:
            dao.moveToPcr(photoMap.x, photoMap.y, 1)
    dailyMission(choice)


def dailyMission(switch):
    # 进入游戏 2023年1月24日19:02:35
    enterGamePcrNew()
    # 商店买经验药
    shopPcr()
    # 买玛娜 -614 20
    buyMana()
    # 扭蛋 -48 472
    dailyEgg()
    # 公会之家 -169 467
    dailyPS()
    # 行会点赞 -113 390
    group()
    # 探索(需要在冒险界面，跟着“行会点赞功能后面”)
    search()
    # 如果是小号就直接回主页。
    # dao.searchPhotoPcr('主页', 1, 0, 0)
    # 收任务
    missionAndGift()
    # 每日PVP
    dailyPvP(1)
    dailyPvP(2)
    # 活动每日试做
    dailyEvent()
    dailyEx()
    # 地下城
    underWorld(switch)
    # 心碎星球杯
    heartBreak()
    # dao.searchPhotoPcr('主页', 1, 0, 0)
    # dao.searchPhotoPcr('pcr主页', 3, -169, 467)
    # dao.searchPhotoPcr('冒险', 1, 0, 0)
    # dao.searchPhotoPcr('主页', 1, 0, 0)


def enterPvP():
    enterMap = ['主页', 'JJC防守成功', 'PJJC防守成功', 'PJJC防守成功2']
    gamePages = multiphotos.Photo()
    count = 0
    while True:
        gamePages.loopSearch(enterMap)
        if "主页".__eq__(gamePages.name):
            # dao.moveToPcr(gamePages.x, gamePages.y, 1)
            result.writeResult(1, '开始自动pvp')
            break
        elif "JJC防守成功".__eq__(gamePages.name):
            dao.moveToPcr(gamePages.x + 47, gamePages.y + 174, 1)
            count += 1
            if count == 3:
                dao.moveToPcr(gamePages.x + 48, gamePages.y + 393, 1)
                count = 0
            result.writeResult(1, 'JJC防守成功')
        elif "PJJC" in gamePages.name:
            dao.moveToPcr(gamePages.x + 62, gamePages.y + 401, 1)
            result.writeResult(1, 'PJJC防守成功')
    return print(result)


# 2022年4月2日21:10:36 1 == jjc  2 == pjjc
def dailyPvP(choice):
    time.sleep(1)
    gamePages = multiphotos.Photo()
    gamePagesMap = ['JJC结束下一步', 'JJC结束下一步2', 'JJC结束下一步3']
    gamePagesMap2 = ['PJJC结束下一步', 'PJJC结束下一步2']
    dao.searchPhotoPcr('冒险', 1, 0, 0)
    time.sleep(3)
    if 1 == choice:
        dao.searchPhotoPcr('主页', 3, 525, -108)
        time.sleep(1)
        enterPvP()
        dao.searchPhotoPcr('主页', 3, 523, -360)
        dao.searchPhotoPcr('战斗开始推图', 3, 403, 65)
        time.sleep(20)
        # dao.searchPhotoPcr('JJC结束下一步', 3, -69, 358)
        gamePages.loopSearch(gamePagesMap)
        print("JJC找到的是：{}".format(gamePages.name))
        daoImpl.moveTo(gamePages.x - 69, gamePages.y + 358)
    elif 2 == choice:
        dao.searchPhotoPcr('主页', 3, 733, -122)
        time.sleep(1)
        enterPvP()
        dao.searchPhotoPcr('主页', 3, 523, -360)
        dao.searchPhotoPcr('战斗开始推图', 4, 403, 65)
        time.sleep(20)
        # dao.searchPhotoPcr('PJJC结束下一步', 3, -76, 434)
        gamePages.loopSearch(gamePagesMap2)
        print("PJJC找到的是：{}".format(gamePages.name))
        daoImpl.moveTo(gamePages.x - 76, gamePages.y + 434)
    exitPvP()


def exitPvP():
    finalPageMaps = ['pcr升级确认', '主页']
    photoMap = multiphotos.Photo()
    while True:
        time.sleep(3)
        photoMap.loopSearch(finalPageMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        if "主页".__eq__(name):
            dao.moveToPcr(x, y, 1)
            break;
        elif "确认" in name:
            dao.moveToPcr(x, y, 1)


# 小号用阉割版
def dailyMissionSmall():
    enterGamePcrNew()
    shopPcr()
    buyMana()
    dailyEgg()
    dailyPS()
    group()
    searchSmall()
    missionAndGift()
    dailyPvP(1)
    dailyEvent()
    dailyEx()
    underWorldSmall()
    # event()


def shopPcr():
    # 商店 -189 389
    # 用主页有时候会失败，找不到，所以替换成图标
    # dao.searchPhotoPcr('pcr主页', 3, -189, 389)
    # 这里不需要主页商店了，放到开游戏NEW里面去判断。
    # dao.searchPhotoPcr('主页商店', 1, 0, 0)
    count = 0
    x, y = dao.searchPhotoPcr('商店勾选框', 1, 0, 0)
    while True:
        if count < 3:
            count = count + 1
            daoImpl.moveTo(x + 168 * count, y)
        elif count == 3:
            daoImpl.moveTo(x + 431, y + 292)
            time.sleep(0.5)
            daoImpl.moveTo(x + 184, y + 328)
            time.sleep(1.5)
            daoImpl.moveTo(x + 97, y + 322)
            dao.searchPhotoPcr('主页', 1, 0, 0)
            break


def buyMana():
    dao.searchPhotoPcr('pcr主页', 3, -614, 20)
    x, y = dao.searchPhotoPcr('玛娜取消', 3, 431, 0)
    time.sleep(2)
    daoImpl.moveTo(x + 423, y - 122)
    dao.searchPhotoPcr('玛娜取消', 1, 0, 0)


def group():
    dao.searchPhotoPcr('pcr主页', 3, -113, 390)
    dao.searchPhotoPcr('公会之家成员信息', 1, 0, 0)
    time.sleep(2)
    x, y = daoImpl.onlySearchPcr('冒险')
    daoImpl.moveTo(x + 343, y - 321)
    time.sleep(2)
    daoImpl.moveToPcr(x, y, 3)


def dailyEgg():
    dao.searchPhotoPcr('pcr主页', 3, -48, 472)
    x, y = dao.searchPhotoPcr('每日扭蛋', 3, 216, -367)
    time.sleep(2)
    dao.moveTo(x - 168 + 216, y + 277 - 367)
    time.sleep(2)
    dao.moveTo(x - 290 + 216, y + 304 - 367)
    dao.searchPhotoPcr('主页', 1, 0, 0)
    time.sleep(1)


def dailyPS():
    dao.searchPhotoPcr('pcr主页', 3, -169, 467)
    dao.searchPhotoPcr('公会收取', 4, 0, 0)
    dao.searchPhotoPcr('主页', 1, 0, 0)


def missionAndGift():
    time.sleep(1)
    x, y = dao.searchPhotoPcr('冒险', 3, 360, -87)
    dao.searchPhotoPcr('任务全部收取', 4, 0, 0)
    dao.searchPhotoPcr('主页', 1, 0, 0)
    time.sleep(2)
    daoImpl.moveTo(x + 436, y - 96)
    dao.searchPhotoPcr('礼物全部收取', 3, 688, 50)
    daoImpl.moveToPcr(x + 15, y - 48, 3)


def search():
    count = 0
    x1 = 0
    y1 = 0
    x, y = daoImpl.onlySearchPcr('主页')
    # 开探索
    daoImpl.moveTo(x + 641, y - 381)
    # 点经验值关卡
    daoImpl.moveTo(x + 489, y - 286)
    time.sleep(1)
    while True:
        # 点9级
        daoImpl.moveTo(x + 570, y - 376)
        # 点使用
        daoImpl.moveTo(x + 661, y - 202)
        # 点确认
        daoImpl.moveTo(x + 511, y - 154)
        if count == 1:
            daoImpl.moveToPcr(x1, y1, 3)
            dao.searchPhotoPcr('主页', 1, 0, 0)
            break
        x1, y1 = dao.searchPhotoPcr('探索前往玛娜', 1, 0, 0)
        count = count + 1


def searchSmall():
    count = 0
    x1 = 0
    y1 = 0
    x, y = daoImpl.onlySearchPcr('主页')
    # 开探索
    daoImpl.moveTo(x + 641, y - 381)
    # 点经验值关卡
    daoImpl.moveTo(x + 489, y - 286)
    while True:
        # 点第二个
        daoImpl.moveTo(x + 590, y - 262)
        # 点使用
        daoImpl.moveTo(x + 661, y - 202)
        # 点确认
        daoImpl.moveTo(x + 511, y - 154)
        if count == 1:
            daoImpl.moveToPcr(x1, y1, 3)
            dao.searchPhotoPcr('主页', 1, 0, 0)
            break
        x1, y1 = dao.searchPhotoPcr('探索前往玛娜', 1, 0, 0)
        count = count + 1


def underWorld(switch):
    time.sleep(1)
    dao.searchPhotoPcr('冒险', 1, 0, 0)
    time.sleep(1)
    dao.searchPhotoPcr('主页', 3, 792, -382)
    time.sleep(1)
    dao.searchPhotoPcr('主页', 3, 756, -266)
    time.sleep(1)
    underWorldEnter()
    pcrUnderEX3(switch)


def underWorldSmall():
    time.sleep(1)
    dao.searchPhotoPcr('冒险', 1, 0, 0)
    time.sleep(1)
    dao.searchPhotoPcr('主页', 3, 792, -382)
    time.sleep(1)
    dao.searchPhotoPcr('主页', 3, 509, -270)
    time.sleep(1)
    underWorldEnter()
    pcrUnderEX1()


def heartBreak():
    time.sleep(3)
    dao.searchPhotoPcr('冒险', 1, 0, 0)
    # 进入心碎页
    dao.searchPhotoPcr('主页', 3, 651, -247)
    # 开操作录制
    daoImpl.searchPhoto('button', 1)
    dao.searchPhotoPcr('心碎星球杯', 3, 361, 5)
    # dao.searchPhotoPcr('心碎星球杯', 3, 448, -321)
    dao.searchPhotoPcr('心碎星球杯', 3, 443, -405)


def autoChangeDefenceP(breakTime):
    flag = True
    temp = breakTime
    while flag:
        if 0 == breakTime:
            temp = random.randint(1, 20)
        breakTime = temp * 60
        dao.searchPhotoPcr('star\\PJJC标识', 3, 67, 58)
        clearMan()
        changeMan(breakTime)
        time.sleep(breakTime)


def changeMan(breakTime):
    # 洗牌
    items = [1, 2, 3]
    random.shuffle(items)
    pages = [0, 1, 2]
    random.shuffle(pages)
    # print("pages:",pages)
    choice = [2, 1, 0]
    random.shuffle(choice)
    # print("choice:",choice)
    count = 0
    while count < 3:
        dao.searchPhotoPcr('star\\防御页总战力', 3, 674, -344)
        choosePage(pages, choice)
        # 换人第一组 -115, 175
        # 换人第二组 -112, 349
        # 换人第三组 -109, 513  倍数170大概
        dao.searchPhotoPcr('star\\换人页标识', 3, -115, 170 * items[count])
        dao.searchPhotoPcr('star\\防御页总战力', 3, 633, 98)
        # print("正在更换第{}套阵容的第{}队".format(pages[choice[0]],count+1))
        count = count + 1
    # print("更换完成，{}秒后更换下一队。".format(breakTime))


# 2022年4月12日17:05:15
def event():
    photoMaps = []
    photoMaps.append(('冒险', 1, 0, 0))
    photoMaps.append(('主页', 3, 326, -109))
    # 第一次进活动时候的对话页
    # photoMaps.append(('活动报酬', 3, 57, 43))
    # photoMaps.append(('主页', 5, 450, -383))
    # 第二次进活动时候直接进了困难关卡页，打一次高难。
    photoMaps.append(('活动主页', 3, 773, -253))
    photoMaps.append(('高难BOSS紫', 3, 643, 418))
    photoMaps.append(('战斗开始推图', 3, 389, 62))
    photoMaps.append(('高难BOSS下一步', 3, -100, 397))
    photoMaps.append(('BOSS胜利下一步', 3, 242, 336))
    photoMaps.append(('button', 1, 242, 336))
    photoMaps.append(('活动困难', 3, 364, 3))
    photoMaps.append(('x', 1, 0, 0))
    photoMaps.append(('活动主页', 3, 820, -104))
    photoMaps.append(('主页', 4, 744, -92))
    photoMaps.append(('主页', 1, 0, 0))

    dao.dualListPhotoPcr(photoMaps)


def clearMan():
    # 清空阵容
    check = 0
    while check < 3:
        dao.searchPhotoPcr('star\\防御页总战力', 5, 194, 103)
        if check != 2:  # 不是最后的话
            # 点下一队
            dao.searchPhotoPcr('star\\防御页总战力', 3, 633, 98)
        else:
            # 返回第一队
            dao.searchPhotoPcr('star\\防御页总战力', 3, -460, -450)
        check = check + 1


def choosePage(pages, choice):
    # 最左边的坐标偏差 -1121, 0
    # 第二个偏差 -890, 1
    # 第三个偏差 -681, -1
    # 算他们差200
    # print('page:',pages)
    temp = choice[0]
    dao.searchPhotoPcr('star\\换人页标识', 3, -1121 + 200 * pages[temp], 0)


# x,y是第一关的偏移量，必须手动找，么得法子。
# 活动 1 - 11  x,y为 60,-127
# 活动 12 - 15 x,y 为 17,-150
# 活动困难 x,y 为 -21, -123
#  主线最新  x,y 为 71, -336
# 困难 x,y 为 86, -174
#  小小甜心 x,y 为 86, -184
def fullAuto(xy):
    # 主线推图第一页 303, -168
    global flag
    flag = True
    count = 4
    i = 0
    while flag:
        photoMap = multiphotos.Photo()
        photoMaps = ['主线推图第一页']
        mainMaps = ['活动主页', '主页']
        photoMap.loopSearch(mainMaps)
        mainMap = photoMap
        # 点第一个。
        dao.moveToPcr(mainMap.x + xy[1], mainMap.y + xy[2], 1)
        photoMap.loopSearch(photoMaps)
        # 点右边15次切到最新。
        dao.moveToPcr(photoMap.x + 269, photoMap.y - 171, min(i + 1, 15))
        autoMapFullAuto()
        py.moveTo(mainMap.x + 291, mainMap.y - 379)
        py.dragTo(mainMap.x + 612, mainMap.y - 370, button='left', duration=0.3)
        i += 1


def saveXY(choice):
    loadXY = []
    loadXY.append(('活动1-11', 60, -127))  # 1
    loadXY.append(('活动12 - 15', 17, -150))  # 2
    loadXY.append(('活动困难', -21, -123))  # 3
    loadXY.append(('主线最新', 71, -336))  # 4
    loadXY.append(('主线困难', 86, -174))  # 5
    loadXY.append(('小小甜心', 86, -184))  # 6
    loadXY.append(('小小甜心活动困难', 49, -260))  # 7
    loadXY.append(('初音活动', 84, -226))  # 8
    loadXY.append(('初音活动困难', -34, -257))  # 9
    loadXY.append(('四兽士', 222, -331))  # 10
    loadXY.append(('四兽士二', 52, -274))  # 11
    loadXY.append(('四兽士三', 160, -233))  # 12
    loadXY.append(('四兽士困难', 141, -320))  # 13
    loadXY.append(('伊利亚普通', 84, -201))  # 14
    loadXY.append(('伊利亚困难', 58, -263))  # 15
    loadXY.append(('和服M普通', 83, -236))  # 16
    loadXY.append(('和服M困难', 4, -151))  # 17
    loadXY.append(('仙境普通', 62, -253))  # 18
    loadXY.append(('仙境困难', 171, -307))  # 19
    loadXY.append(('35章普通', 47, -153))  # 20
    loadXY.append(('水白普通', 83, -213))  # 21
    loadXY.append(('水白困难', 4, -243))  # 22
    loadXY.append(('水老师普通', 44, -114))  # 23
    loadXY.append(('水老师困难', -12, -304))  # 24
    loadXY.append(('水流夏普通', 112, -257))  # 25
    loadXY.append(('水流夏普通2', 87, -169))  # 26
    loadXY.append(('水流夏困难', -16, -199))  # 27
    loadXY.append(('36章普通', 62, -299))  # 28
    loadXY.append(('36章困难', 110, -218))  # 29
    loadXY.append(('复刻水狗困难', 8, -300))  # 30
    loadXY.append(('水初音普通',64, -250))  # 31
    loadXY.append(('水初音困难', 12, -265))  # 32
    loadXY.append(('37章普通', 66, -129))  # 33
    loadXY.append(('油腻复刻困难', -5, -334))  # 34
    loadXY.append(('无人岛外传普通', 85, -244))  # 35
    loadXY.append(('无人岛外传困难', 9, -325))  # 36
    loadXY.append(('黑铁普通', 58, -148))  # 37
    loadXY.append(('黑铁困难', 9, -330))  # 38
    loadXY.append(('天使伊里普通',93, -150))  # 39
    loadXY.append(('天使伊里困难', 16, -317))  # 40
    loadXY.append(('瓜炸普通', 0, -144))  # 41
    loadXY.append(('38普通', 76, -90))  # 42
    loadXY.append(('万圣节普通', 56, -222))  # 43
    loadXY.append(('39普通', 79, -268))  # 44
    loadXY.append(('龙之探索者复刻普通', 57, -178))  # 45
    loadXY.append(('外传流夏', 64, -264))  # 46
    loadXY.append(('魔法少女莫妮卡普通', 76, -165))  # 47
    loadXY.append(('魔法少女莫妮卡困难', -1, -221))  # 48
    loadXY.append(('re0复刻普通', 66, -335))  # 49
    loadXY.append(('re0复刻困难', 29, -275))  # 50
    loadXY.append(('圣千普通', 194, -311))  # 51
    loadXY.append(('圣千困难', 23, -119))  # 52
    loadXY.append(('40普通', 75, -316))  # 53
    loadXY.append(('圣哈普通', 80, -155))  # 54
    loadXY.append(('圣哈困难', 21, -333))  # 55
    loadXY.append(('圣望复刻普通', -13, -182))  # 56
    loadXY.append(('圣望复刻困难', -10, -199))  # 57
    loadXY.append(('41普通', 54, -261))  # 58
    loadXY.append(('春吃普通', 67, -185))  # 59
    loadXY.append(('春吃困难', -42, -295))  # 60
    loadXY.append(('春女仆1-9', 111, -153))  # 61
    loadXY.append(('春女仆困难', -37, -203))  # 62
    loadXY.append(('42普通', 50, -283))  # 63
    loadXY.append(('礼服可可萝普通', 64, -325))  # 64
    loadXY.append(('礼服可可萝困难',28, -196))  # 65
    loadXY.append(('礼服可可萝第二章普通', -5, -318))  # 66
    loadXY.append(('礼服可可萝第二章困难', -20, -256))  # 67
    loadXY.append(('43普通', 36, -257))  # 68
    loadXY.append(('魔驴普通', 69, -143))  # 69
    loadXY.append(('魔驴困难', 5, -320))  # 70
    loadXY.append(('灰狼普通', 12, -307))  # 71
    loadXY.append(('灰狼困难', 10, -231))  # 72
    loadXY.append(('偶像大师前篇普通', 57, -187))  # 73
    loadXY.append(('偶像大师前篇困难', 18, -269))  # 74
    loadXY.append(('44章普通', 26, -335))  # 75
    loadXY.append(('44章困难', 119, -231))  # 76
    loadXY.append(('偶像大师后篇普通', 54, -218))  # 77
    loadXY.append(('偶像大师后篇困难', -26, -321))  # 78
    loadXY.append(('圣学祭普通', 84, -209))  # 79
    loadXY.append(('圣学祭困难', 0, -217))  # 80
    return loadXY[choice - 1]


# 2022年4月20日21:31:11
def changeTeam5(count):
    if count <= 2:
        dao.searchPhotoPcr('地下城我的队伍', 3, -464, 5)
        if count == 1:
            dao.searchPhotoPcr('地下城我的队伍', 3, -61, 238)
        if count == 2:
            dao.searchPhotoPcr('地下城我的队伍', 3, -82, 338)
    elif count > 2:
        dao.searchPhotoPcr('地下城我的队伍', 3, -322, -1)
        if count == 3:
            dao.searchPhotoPcr('地下城我的队伍', 3, -78, 119)
        elif count == 4:
            dao.searchPhotoPcr('地下城我的队伍', 3, -61, 238)
        elif count == 5:
            dao.searchPhotoPcr('地下城我的队伍', 3, -82, 338)
    # dao.searchPhotoPcr('战斗开始界面定标1EX3', 3, 211, -271)


# 2022年4月20日22:04:31
def battleFloor5():
    photoMap = multiphotos.Photo()
    photoMaps = ["地下城失败页"]
    # dao.searchPhotoPcr('下一步EX3', 3, -71, 402)
    # dao.searchPhotoPcr('地下城确认EX3', 3, 1, 400)
    for i in range(1, 5):
        daoImpl.searchPhoto('{}层EX3'.format(5), 1)
        dao.searchPhotoPcr('挑战EX3', 3, 3, 39)
        dao.searchPhotoPcr('战斗开始界面定标1EX3', 3, 211, -271)
        changeTeam5(i)
        dao.searchPhotoPcr('战斗开始界面定标1EX3', 3, 182, 93)
        time.sleep(60)
        # 从第二刀开始可能打赢，所以加入胜利判断
        if i == 2:
            photoMaps = ["地下城胜利","地下城失败页"]
        photoMap.loopSearch(photoMaps)
        if "地下城失败页".__eq__(photoMap.name):
            dao.moveToPcr(photoMap.x + -51, photoMap.y + 453, 1)
        elif "地下城胜利".__eq__(photoMap.name):
            time.sleep(5)
            dao.moveToPcr(photoMap.x + 361, photoMap.y + 428, 1)
            dao.searchPhotoPcr('地下城确认EX3', 3, 1, 400)
            time.sleep(3)
            break


# 2022年4月22日19:18:10
def pcrUnderEX1():
    # 地下城商店
    clickMaps = [(-478, 235), (-745, 222), (-231, 224)]
    photoMap = multiphotos.Photo()
    photoMaps = ["地下城商店", "下一步EX3"]
    count = 0
    while count < 10:
        photoMap.loopSearch(photoMaps)
        if "地下城商店".__eq__(photoMap.name):
            x = photoMap.x
            y = photoMap.y
            dao.moveToPcr(x, y, 1)
            dao.searchPhotoPcr("地下城商店返回", 3, -334, -37)
            time.sleep(2)
            for i in clickMaps:
                dao.moveToPcr(x + i[0], y + i[1], 1)
            underWorldBattle()
        elif "下一步EX3".__eq__(photoMap.name):
            dao.moveToPcr(photoMap.x + -71, photoMap.y + 402, 1)
            dao.searchPhotoPcr('地下城确认EX3', 3, 1, 400)
            count += 1
    dao.searchPhotoPcr("主页", 1, 0, 0)


# 2022年4月22日20:07:55 地下城挑战，重复了。
def underWorldBattle():
    dao.searchPhotoPcr('挑战EX3', 3, 3, 39)
    dao.searchPhotoPcr('战斗开始界面定标1EX3', 3, 182, 93)
    time.sleep(15)


# 2022年4月22日20:08:15 点击地下城后选择队伍与开始第一战，重复了
def underWorldEnter():
    dao.searchPhotoPcr('地下城进入', 3, 256, 42)
    time.sleep(5)
    dao.searchPhotoPcr('主页', 3, 596, -255)
    dao.searchPhotoPcr('挑战EX3', 3, 3, 39)
    dao.searchPhotoPcr('战斗开始界面定标1EX3', 3, 211, -271)
    dao.searchPhotoPcr('地下城我的队伍', 3, -464, 5)
    dao.searchPhotoPcr('地下城我的队伍', 3, -78, 119)
    dao.searchPhotoPcr('战斗开始界面定标1EX3', 3, 182, 93)


# 2022年5月14日16:21:57 自动过剧情。
def autoText():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "pcr剧情新内容",
        "pcr剧情跳过",
        "PCR剧情菜单",
        "pcr剧情无语音",
        "pcr剧情跳过确认",
        "pcr剧情关闭",
        "pcr连续阅读无语音",
        "pcr剧情视频跳过",
    ]
    moveMaps = [
        (107, 225),  # pcr剧情跳过确认 0
        (3, 292),  # pcr连续阅读界面，无语音选项 1
    ]
    onlyOneMaps = [

    ]
    while flag:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        if "确认" in name:
            dao.moveToPcr(x + moveMaps[0][0], y + moveMaps[0][1], 1)
        elif "pcr连续阅读无语音" in name:
            dao.moveToPcr(x + moveMaps[1][0], y + moveMaps[1][1], 1)
        else:
            dao.moveToPcr(x, y, 1)


# 2022年5月14日16:53:02 自动过信赖度。
def autoTrust():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "pcr信任新内容",
        "pcr无语音",
        "pcr选项一",
        "pcr选项二",
        "pcr选项三",
        "pcr信任结算",
        "pcr对话框",
        "pcr对话框二",
        "pcr对话框三",
        "pcr对话框四",
        "pcr信任度最大",
        "pcr信任度最大二",
        "pcr0信任",
    ]
    moveMaps = [
        (-119, -358),  # pcr信任度最大时返回 0
    ]
    onlyOneMaps = [

    ]
    while flag:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        if "对话框" in name:
            dao.moveToPcr(x, y, 2)
        elif "最大" in name:
            dao.moveToPcr(x + moveMaps[0][0], y + moveMaps[0][1], 1)
        else:
            dao.moveToPcr(x, y, 1)


# 2022年5月25日18:15:17 自动抽奖。
def autoEventEgg():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "pcr抽100次",
        "pcr查看获得道具",
        "pcr再次交换",
        "pcr再次交换2",
        "pcr扭蛋确认",
        "pcr扭蛋结束",
    ]
    moveMaps = [
        (46, -58),  # 0 初始页面抽100次。
    ]
    onlyOneMaps = [

    ]
    while flag:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        if "结束" in name:
            dao.moveToPcr(x, y, 1)
            changeFlag()
        elif "100" in name:
            dao.moveToPcr(x + moveMaps[0][0], y + moveMaps[0][1], 1)
        else:
            dao.moveToPcr(x, y, 1)

# 2022年12月11日20:27:16
# 活动打5次。
def dailyEvent(choice = dailyEventNo,switch = eventSwitch):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "主界面关闭",
        "首领挑战卷",
        "首领挑战卷2",
        "冒险",
        "主线推图第一页",
        "剧情活动",
        "pcr活动复刻",
        "活动减一",
        "pcr对话框",
        "pcr对话框二",
        "pcr对话框三",
        "pcr对话框四",
        #"主页",
    ]
    moveMaps = [
        (348, -220),  # 0 , 点击操作录制。
        (361, 5), # 1 , 点击开始
        (450, -155) , #2 , 关闭录制页
    ]
    tempXY = saveXYHard(choice)
    while switch:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "挑战" in name:
            dao.moveToPcr(x + tempXY[1], y + tempXY[2], 1)
            continue

        if "第一页" in name:
            dao.moveToPcr(x + moveMaps[0][0], y + moveMaps[0][1], 1)
            continue

        if "减一" in name:
            dao.moveToPcr(x + moveMaps[1][0], y + moveMaps[1][1], 1)
            time.sleep(1)
            dao.moveToPcr(x + moveMaps[2][0], y + moveMaps[2][1], 1)
            break

        dao.moveToPcr(x,y,1)

# 2022年12月11日21:42:44
# 活动打EX.
def dailyEx(index = dailyEventNo,switch = eventSwitch):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "首领挑战卷",
        "高难BOSS",
        "剧情活动",
        "活动减一",
        #"主页",
    ]
    moveMaps = [
        (602, 425), # 0,高难页面点击挑战
    ]
    tempXY = saveXYHard(index)
    while switch:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "挑战" in name:
            dao.moveToPcr(x + tempXY[4], y + tempXY[5], 1)
            continue

        if "BOSS" in name:
            dao.moveToPcr(x + moveMaps[0][0], y + moveMaps[0][1], 1)
            autoMapFullAuto()
            dao.searchPhotoPcr('主页', 3, 0, 0)
            photoMaps.append("冒险")

        if "冒险" in name:
            break

        dao.moveToPcr(x,y,1)

# 2022年12月11日20:27:05
# 基于 首领挑战卷 的1-5坐标记录
def saveXYHard(choice):
    loadXY = []
    loadXY.append(('圣哈1-5', 39, -105,'圣哈高难',233, -145))  # 1
    loadXY.append(('圣望复刻', 118, -212, '圣望高难', 233, -145))  # 2
    loadXY.append(('春吃', 93, -234, '春吃高难', 233, -145))  # 3
    loadXY.append(('春女仆', 57, -219, '春女仆高难', 233, -145))  # 4
    loadXY.append(('礼服可可萝', 1, -237, '礼服可可萝高难', 233, -145))  # 5
    loadXY.append(('礼服可可萝后篇', 35, -141, '礼服可可萝高难', 233, -145))  # 6
    loadXY.append(('灰狼困难', 137, -197, '灰狼高难', 233, -145))  # 7
    loadXY.append(('偶像大师前篇', 110, -129, '偶像大师前篇高难', 233, -145))  # 8
    loadXY.append(('偶像大师后篇', 91, -135, '偶像大师后篇高难', 233, -145))  # 9
    return loadXY[choice - 1]

# 换号进游戏。
def changePlayerOpen(start = 0):
    photoMap = multiphotos.Photo()
    photoMaps = [
        '账号登录',
        '切换账号',
        '切换账号',
        '眼镜厂标识',
        'pcr',
    ]
    moveMaps = [
        (112, -80) , # 0 账号登录前先点开账号下拉列表
    ]
    count = start
    while 1 :
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        x = photoMap.x
        y = photoMap.y

        if "账号登录".__eq__(name):
            dao.moveToPcr(x + moveMaps[0][0], y + moveMaps[0][1], 1)
            choosePlayer(count)
            closeGame()
            count += 1
            if count == 3:
                break
            else:
                continue

        dao.moveToPcr(x,y,1)


# 登录的时候选择账号 2023年1月24日19:17:01
def choosePlayer(playerNum = 0):
    photoMap = multiphotos.Photo()
    photoMaps = [
        '账号登录',
    ]
    playerMaps = [
        "pcr大号",
        "pcr小号",
        "pcr小小号",
    ]
    photoMaps.append(playerMaps[playerNum])
    while 1 :
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        x = photoMap.x
        y = photoMap.y
        dao.moveToPcr(x,y,1)

        if "pcr大号".__eq__(name):
            dailyMission(1)
            break

        if "pcr小小号".__eq__(name):
            dailyMissionSmall()
            break

        if "pcr小号".__eq__(name):
            dailyMission(0)
            break

# 登录游戏前置功能拆分，到了主页就停止。 2023年1月24日19:17:08
# 加了个跳过剧情。 2023年4月3日21:59:00
def enterGamePcrNew():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "账号登录",
        "pcr开始",
        '主界面关闭',
        '碎片X10',
        'pcr生日回礼',
        'pcr生日跳过',
        'pcr生日跳过2',
        'pcr剧情跳过',
        'PCR剧情菜单',
        '扭蛋广告',
        '150钻',
        '附奖扭蛋',
        '主页商店',
        "商店勾选框",
        'pcr竞赛开始',
    ]
    while 1:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        x = photoMap.x
        y = photoMap.y

        if "商店勾选框".__eq__(name):
            break

        dao.moveToPcr(x, y, 1)

def closeGame():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "回到标题界面",
        "主菜单",
        "pcr扭蛋确认",
        "眼镜厂标识",
    ]
    photoMapsTemp = [
        "pcr主页",
    ]
    while 1:
        photoMap.loopSearch(photoMapsTemp)
        name = photoMap.name
        x = photoMap.x
        y = photoMap.y

        if "眼镜厂标识".__eq__(name):
            break

        if "pcr主页".__eq__(name):
            photoMapsTemp = photoMaps
            continue

        dao.moveToPcr(x, y, 1)

def hardEvent(number = 0):
    dailyEvent(number,True)
    dailyEx(number, True)

if __name__ == '__main__':
    # autoEventEgg()
    # underWorldSmall()
    # autoTrust()
    # autoText()
    # underWorld(1)
    # underWorld(1)
    # dailyEvent()
    # 心碎星球杯
    # dailyEvent()
    # dailyEx()
    # heartBreak()
    # photoMap = multiphotos.Photo()
    # photoMaps = ["地下城失败页"]
    # photoMap.loopSearch(photoMaps)
    # if "地下城失败页".__eq__(photoMap.name):
    #     dao.moveToPcr(photoMap.x + -51, photoMap.y + 453, 1)
    # else:
    #     dao.moveToPcr(photoMap.x, photoMap.y, 1)
    # fullAuto(saveXY(7))
    # autoMapFullAuto()
    # missionAndGift()
    # changePlayerOpen(0)
    # enterGamePcrNew()
    # closeGame()
    # changePlayerOpen(start = 1)
    # dailyEvent(8,True)
    # dailyEx(8, True)
    enterGamePcrNew()