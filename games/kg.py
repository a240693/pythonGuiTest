import pyautogui
import time
import _thread

from dao import dao, daoImpl, multiphotos

flag = True


# 暂时没用了.
class kgPhoto:
    def __init__(self):
        self.name = "默认"
        self.mode = 1
        self.x = 0
        self.y = 0

    def addPhoto(self, name, mode, x, y):
        self.name = name
        self.mode = mode
        self.x = x
        self.y = y


def open():
    # 开雷电多开器
    daoImpl.searchPhoto('1', 2)
    daoImpl.searchPhotoOpen('明日方舟')
    # 开坎公
    daoImpl.searchPhoto('kg', 5)
    time.sleep(10)
    daoImpl.enterGame()
    # daoImpl.searchPhoto('kgx',1)
    # daoImpl.searchPhoto('领取奖励.png',1)
    # daoImpl.searchPhoto('确认.png',1)
    # 开操作录制
    # daoImpl.searchPhoto('button.png',1)
    # 按操作录制X
    # daoImpl.searchPhoto('x.png',1)

    # 开脚本第三个
    # daoImpl.searchPhoto('kg3.png',1)


def kmxAuto():
    count = 0
    while True:
        if 0 == daoImpl.searchPhotoOnce('卡马逊黄', 4):
            count = count + 1
        if count == 5:
            print("找不到5次，休息0.3秒")
            time.sleep(0.1)
            count = 0
        # print("跑完一轮")


def kmxAutoNew():
    count = 0
    gamePages = multiphotos.Photo()
    gamePagesMap = ['卡马逊黄',
                    '坎公卡马逊确认',
                    '坎公问号',
                    '坎公泰坦战队',
                    '坎公休息区',
                    '坎公特惠促销',
                    '坎公保存神器',
                    '坎公装备取消',
                    '卡马逊商店',
                    '坎公装备页',
                    '卡马逊主页']
    # 坎公卡马逊选择 暂时用不上。
    while flag:
        gamePages.name = "默认"
        gamePages.loopSearch(gamePagesMap)
        count += 1
        print('{}({},{}),第{}次'.format(gamePages.name, gamePages.x, gamePages.y, count))
        x = gamePages.x
        y = gamePages.y
        if "卡马逊主页".__eq__(gamePages.name):
            # 如果检测到了卡马逊主页就直接退出。
            if (count > 8):
                break
            else:
                continue
        elif "坎公问号".__eq__(gamePages.name):
            dao.moveToKgAuto(x + 66, y + 147, 1)
            dao.moveToKgAuto(x, y + 36, 1)
            dao.moveToKgAuto(x + 423, y + 154, 1)
            continue
        elif "坎公休息区".__eq__(gamePages.name):
            # 先点回血，再点净化再点复活，复活优先。
            dao.moveToKgAuto(gamePages.x + 280, gamePages.y + -240, 1)
            dao.moveToKgAuto(gamePages.x + 89, gamePages.y + -195, 1)
            dao.moveToKgAuto(gamePages.x + -149, gamePages.y + -225, 1)
            dao.moveToKgAuto(gamePages.x + 196, gamePages.y + 2, 1)
            continue
        elif "坎公装备取消".__eq__(gamePages.name):
            dao.moveToKgAuto(gamePages.x + 277, gamePages.y + 109, 1)
            time.sleep(1)
            dao.moveToKgAuto(gamePages.x + 493, gamePages.y + 369, 1)
            continue
        elif ("战队" in gamePages.name) | ("促销" in gamePages.name):
            dao.scrollKg(x + 134, y + 293)
            continue
        elif "坎公装备页".__eq__(gamePages.name):
            chooseEquip()
            # dao.moveToKgAuto(gamePages.x + 137, gamePages.y + -206, 1)
            continue
        elif "保存神器" in gamePages.name:
            dao.moveToKgAuto(x - 3 ,y + 127,1)
            dao.moveToKgAuto(x + 132 , y + 371 , 1)
            # dao.moveToKgAuto(gamePages.x + 137, gamePages.y + -206, 1)
            changeFlag()
            break
        else:
            # 这里拿到了上面三选一的 名字 和XY坐标
            dao.moveToKgAuto(gamePages.x, gamePages.y, 1)
        if count == 1:
            time.sleep(6)
        elif count > 15:
            changeFlag()


def chooseEquip():
    equipMaps = ["坎公高阶神器",
                 "坎公高阶神器",
                 "坎公中阶神器",
                 "坎公低阶神器",
                 "坎公获得银币"]

    photoMap = multiphotos.Photo()
    # moveMaps = []
    photoMap.loopSearch(equipMaps)
    x = photoMap.x
    y = photoMap.y
    dao.moveToKgAuto(x, y, 1)


def pvpAuto():
    gamePages = multiphotos.Photo()
    gamePagesMap = [
        '坎公挑战卷不足',
        '坎公44段位更新',
        '坎公商店确认',
        '坎公初始选人页黄',
        '坎公PVP黄',
        '坎公初始选人页重试',
        '坎公卡马逊确认'
    ]
    while flag:
        gamePages.name = "默认"
        gamePages.loopSearch(gamePagesMap)
        if "坎公初始选人页重试".__eq__(gamePages.name):
            # 拿偏移坐标，点一下右上角齿轮在的位置收工。
            daoImpl.moveTo(gamePages.x + 46, gamePages.y - 72)
            dao.moveTo(gamePages.x, gamePages.y)
        elif '坎公PVP黄'.__eq__(gamePages.name):
            dao.moveTo(gamePages.x, gamePages.y)
            time.sleep(20)
        elif "不足" in gamePages.name:
            dao.moveTo(gamePages.x + - 28, gamePages.y + 154)
            changeFlag()
        elif '更新' in gamePages.name:
            dao.moveToKgAuto(gamePages.x + 3, gamePages.y + 227, 1)
        # 这里拿到了上面三选一的 名字 和XY坐标
        else:
            daoImpl.moveToKgAuto(gamePages.x, gamePages.y, 1)

    # while flag:
    #     # 注释了，反正只找得到坎公PVP黄
    #     if 1 == daoImpl.searchPhotoOnce('坎公初始选人页黄', 4):
    #         continue
    #     elif 1 == daoImpl.searchPhotoOnce('坎公PVP黄', 4):
    #         continue
    #     elif 1 == daoImpl.searchPhotoOnce('卡马逊黄', 4):
    #         continue
    #     # if 0 == daoImpl.searchPhotoOnce('坎公PVP黄', 4):
    #     count += 1
    #     if count == 5:
    #         print("找不到5次，休息0.3秒")
    #         time.sleep(0.1)
    #         count = 0
    # print("跑完一轮")


def setFlag():
    count = 420
    while ((count != 0) & (flag)):
        count -= 20
        print("还剩下{}秒".format(count))
        time.sleep(20)
    changeFlag()


def changeFlag():
    global flag
    flag = False


def pvp():
    try:
        global flag
        flag = True
        _thread.start_new_thread(pvpAuto, ())
        _thread.start_new_thread(setFlag, ())
    except:
        print("Error: 无法启动线程")

    while 1:
        if flag == False:
            break
        pass


def dailyBuy():
    time.sleep(1)
    daoImpl.searchPhotoKg('坎公主页面', 1, -338, -195)
    x, y = daoImpl.onlySearchPcr('坎公进入商店')
    # 买金币
    daoImpl.moveTo(x + 414, y + 267)
    daoImpl.searchPhotoKg('坎公购买', 1, 94, 56)  # 商店黄成功率太低了
    daoImpl.searchPhotoKg('坎公商店确认', 1, 0, 0)
    # 买锤子
    daoImpl.moveTo(x - 15, y + 238)
    daoImpl.moveTo(x + 218, y + 197)
    daoImpl.searchPhotoKg('坎公购买', 1, 94, 56)
    daoImpl.searchPhotoKg('坎公商店确认', 1, 0, 0)
    daoImpl.moveTo(x + -70, y + -42)


# 2022年4月2日17:18:10 起点是先收灵魂点
def day2buy(choice):
    dailyBuy()
    photoMap = []
    photoMap.append(('坎公主页面', 1, -422, 111))
    photoMap.append(('坎公主页面', 1, -258, 233))
    photoMap.append(('坎公主页面', 1, -834, 237))
    photoMap.append(('探险初始页', 1, -718, -341))
    if 2 == choice:
        # 第二个
        photoMap.append(('进化石页面', 1, 636, 253))
    elif 3 == choice:
        # 第三个
        photoMap.append(('进化石页面', 1, 600, 422))
    elif 1 == choice:
        # 第一个
        photoMap.append(('进化石页面', 1, 624, 103))
    photoMap.append(('进化石页面', 1, 762, 458))
    photoMap.append(('进化石扫荡', 1, -35, -147))
    photoMap.append(('进化石扫荡', 1, 0, 0))
    photoMap.append(('坎公进化石确认', 1, 0, 0))
    photoMap.append(('坎公商店确认', 1, 0, 0))
    photoMap.append(('进化石页面', 1, -89, 2))
    photoMap.append(('进化石页面', 1, -89, 2))
    photoMap.append(('探险初始页', 1, -723, -174))
    dao.dualListPhotoKg(photoMap)
    pvp()


def fullAutoKmx():
    count = 0
    photoMap = multiphotos.Photo()
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
        x = photoMap.x
        y = photoMap.y
        if "卡马逊主页".__eq__(photoMap.name):
            for i in moveMaps:
                dao.moveToKgAuto(x + i[0], y + i[1], 1)
            kmxAutoNew()
            if flag:
                count += 1
                time.sleep(10)
                returnKmx()
    # 人物所在位置  394, 99


def returnKmx():
    photoMap = []
    # 退出 -52, -465
    # 返回 127, -170
    photoMap.append(('卡马逊主页', 1, -6, -467))
    photoMap.append(('探险初始页', 1, 84, -274))
    dao.dualListPhotoKg(photoMap)


if __name__ == '__main__':
    # chooseEquip()
    #fullAutoKmx()
    kmxAutoNew()
# fullAutoKmx()
# missionAndGift()
