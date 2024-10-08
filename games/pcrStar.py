import datetime

import pyautogui as py
import time
import random

from dao import dao, daoImpl, multiphotos, resultMap,changeVar as cv
import _thread
from testTools import timeTest

flag = False
loseFlag = 0

cv._init()
cv.set_value("path",cv.path)

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
    upDown = [0, 1]
    random.shuffle(upDown)
    items = [1, 2, 3]
    random.shuffle(items)
    pages = [0, 1, 2]
    random.shuffle(pages)
    # print("pages:",pages)
    choice = [2, 1, 0]
    random.shuffle(choice)
    # print("choice:",choice)
    count = 0
    print("目标顺序是：{},0升，1降.".format(upDown[0]))
    changeUpDown(upDown[0], 0)
    while count < 3:
        dao.searchPhotoPcr('star\\防御页总战力', 3, 674, -344)
        choosePage(pages, choice)
        # 换人第一组 -115, 175
        # 换人第二组 -112, 349
        # 换人第三组 -109, 513  倍数170大概
        if upDown[0] == 0:
            dao.searchPhotoPcr('star\\换人页标识升序', 3, -115, 170 * items[count])
        elif upDown[0] == 1:
            dao.searchPhotoPcr('star\\换人页标识降序', 3, -115, 170 * items[count])
        dao.searchPhotoPcr('star\\防御页总战力', 3, 633, 98)
        # print("正在更换第{}套阵容的第{}队".format(pages[choice[0]],count+1))
        count = count + 1
    # print("更换完成，{}秒后更换下一队。".format(breakTime))


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
    photoMap = multiphotos.Photo()
    photoMaps = [
        "star\\换人页标识升序",
        "star\\换人页标识降序",
    ]
    photoMap.loopSearch(photoMaps)
    moveMaps = [(-1121 + 200 * pages[temp], 0)]
    dao.moveToPcr(photoMap.x + moveMaps[0][0], photoMap.y + moveMaps[0][1], 1)


# 2022年6月4日11:28:39 换人页更改顺序
# 2022年6月10日22:04:05 新增来源
def changeUpDown(upDown, jjc):
    if 0 == jjc:
        dao.searchPhotoPcr('star\\防御页总战力', 3, 674, -344)
    elif 1 == jjc:
        dao.searchPhotoPcr('star\\防御页总战力', 3, 669, -445)
    photoMap = multiphotos.Photo()
    photoMaps = [
        "star\\换人页标识升序",
        "star\\换人页标识降序",
    ]
    photoMap.loopSearch(photoMaps)
    x = photoMap.x
    y = photoMap.y
    name = photoMap.name
    if ("升序" in name) & (upDown != 0):
        dao.moveToPcr(x, y, 1)
    if ("降序" in name) & (upDown != 1):
        dao.moveToPcr(x, y, 1)
    dao.searchPhotoPcr("star\\主界面关闭", 3, 0, 0)


# 查找JJC目标 2022年6月10日22:02:35
# 更换查找逻辑，现在支持打两个仇人 2022年8月30日20:47:39
def searchTarget(auto, cdCheck, sleepTimeS, sleepTimeE, changeDefence):
    photoMap = multiphotos.Photo()
    photoMaps = [
        "star\\仇人ID",
        "star\\仇人整块",
    ]
    onlyOneMap = [
        "star\\jjc刷新",  # 0
        "star\\jjc结束下一步",  # 1
        "star\\jjc五次次数",  # 2
        "star\\jjc碎钻",  # 3
        "star\\jjc碎钻二次确认",
    ]
    moveMaps = [
        (158, 213),  # 0 买5次次数确认。
        (146, 193),  # 1 碎钻二次确认，直接碎钻。
    ]
    # 不为0，就自动开始战斗。
    if auto != 0:
        onlyOneMap.append("star\\jjc战斗开始")
    # 不为0，就碎钻。
    if cdCheck != 0:
        moveMaps.append((151, 137))
    # 为0，不碎钻
    elif cdCheck == 0:
        moveMaps.append((-179, 146))
        sleepTimeS = max(300, sleepTimeS)
        sleepTimeE = min(302, sleepTimeE)
        if sleepTimeS > sleepTimeE:
            temp = sleepTimeS
            sleepTimeS = sleepTimeE
            sleepTimeE = temp
    sleepTime = random.randint(sleepTimeS, sleepTimeE)
    while flag:
        switch = 1
        for i in photoMaps:
            result = photoMap.onlySearchOnce(i, 0, 0)
            print("{}：{}".format(i, result))
            if 1 != result:
                switch = 0
                break
        # 没找到就重新刷新。
        if 0 == switch:
            photoMap.searchPhoto(onlyOneMap[0])
            click(photoMap)
        else:
            # 找到了就点击仇人。
            # 新逻辑，点击仇人之前先换人。
            # 新逻辑，如果勾上才能换防。  2022年6月14日23:28:49
            if changeDefence == 1:
                changeManEnter()
            click(photoMap)
            time.sleep(10)
            while True:
                photoMap.loopSearch(onlyOneMap)
                if "五次" in photoMap.name:
                    click(photoMap, moveMaps[0])
                elif "二次" in photoMap.name:
                    click(photoMap, moveMaps[1])
                elif "star\\jjc碎钻".__eq__(photoMap.name):
                    click(photoMap, moveMaps[2])
                else:
                    click(photoMap)
                if "战斗开始" in photoMap.name:
                    break;
                if "结束" in photoMap.name:
                    break
                if ("碎钻" in photoMap.name) & (cdCheck == 0):
                    print("不碎钻，开始休眠{}秒。".format(sleepTime))
                    time.sleep(sleepTime)
                    break
            backSearchTarget()


def changeManEnter():
    dao.searchPhotoPcr("star\\jjc防守", 3, 0, 0)
    changeManJJC()

# 更换进攻 2022年8月30日21:06:12
def changeAttackTeam():
    defenceMaps = [
        "star\\仇人防守1",
        "star\\仇人防守2",
    ]
    photoMap = multiphotos.Photo()
    while 1 :
        photoMap.loopSearch(defenceMaps)
        name = photoMap.name
        if name in "防守1":
            changeAttackTeamEx(1)
        if name in "防守2":
            changeAttackTeamEx(2)
        break

def changeAttackTeamEx(teamNo = 2):
    photoMaps = [
        "star\\防御页我的队伍",
        "star\\换人页标识升序",
        "star\\换人页标识降序",
    ]
    moveMaps = [
        (-266, 9), # 0 找到升序后点击编组5
        (-105, 176), # 1 点击编组5后点击进攻组1
        (-134, 350), # 2 点击编组5后点击进攻组2

    ]
    photoMap = multiphotos.Photo()
    while 1 :
        photoMap.loopSearch(photoMaps)
        name = photoMap.name

        if "升序" in name:
            click(photoMap,moveMaps[0])
            click(photoMap,moveMaps[teamNo])
            break

        click(photoMap,(0,0))


# 从战斗结束页面返回主页面 2022年6月10日22:19:08
def backSearchTarget():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "star\\jjc胜利",
        "star\\jjc失败",
        "star\\jjc确认",
        # "star\\jjc结束下一步",
        "star\\jjc防守",
    ]
    moveMaps = [
        (518, 649),  # 胜利页面点下一步。
        (621, 577),  # 失败页面下一步。
    ]
    while True:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        if "防守" in name:
            # changeManEnter()
            break;
        # 胜利就重置。
        elif "胜利" in name:
            click(photoMap, moveMaps[0])
            if loseFlag == 1:
                changeLoseFlag(0)
        # 失败就置1，再失败就关闭。
        elif "失败" in name:
            click(photoMap, moveMaps[1])
            if loseFlag == 1:
                print("警告：进攻失败，进程关闭。")
                exit()
            else:
                changeLoseFlag(1)
        else:
            click(photoMap)


def click(photoMap, xy=(0, 0)):
    x = photoMap.x + xy[0]
    y = photoMap.y + xy[1]
    dao.moveToPcr(x, y, 1)


# 旧JJC击剑入口，现测试击剑入口。
def jjcStart(auto=1, cdCheck=1, sleepTimeS=60, sleepTimeE=300, changeDefence=1):
    try:
        global flag
        flag = True
        _thread.start_new_thread(searchTarget, (auto, cdCheck, sleepTimeS, sleepTimeE, changeDefence))
        _thread.start_new_thread(setFlag, ())
    except:
        print("Error: 无法启动线程")

    while 1:
        if flag == False:
            break
        pass


def setFlag():
    count = 3600 * 5
    while count != 0:
        print("还剩下{}秒".format(count))
        count -= 20
        time.sleep(20)
    changeFlag()


def changeFlag():
    global flag
    flag = False


# 阉割版换人，JJC用。
def changeManJJC():
    # 洗牌
    upDown = [0, 1]
    random.shuffle(upDown)
    items = [1, 2, 3]
    random.shuffle(items)
    pages = [0, 1, 2]
    random.shuffle(pages)
    # print("pages:",pages)
    choice = [2, 1, 0]
    random.shuffle(choice)
    # print("choice:",choice)
    count = 0
    print("目标顺序是：{},0升，1降.".format(upDown[0]))
    changeUpDown(upDown[0], 1)
    while count < 1:
        dao.searchPhotoPcr('star\\防御页总战力', 3, 669, -445)
        choosePage(pages, choice)
        # 换人第一组 -115, 175
        # 换人第二组 -112, 349
        # 换人第三组 -109, 513  倍数170大概
        if upDown[0] == 0:
            dao.searchPhotoPcr('star\\换人页标识升序', 3, -115, 170 * items[count])
        elif upDown[0] == 1:
            dao.searchPhotoPcr('star\\换人页标识降序', 3, -115, 170 * items[count])
        dao.searchPhotoPcr('star\\防御页总战力', 3, 631, 98)
        # print("正在更换第{}套阵容的第{}队".format(pages[choice[0]],count+1))
        count = count + 1


def newJJCenter(auto, cdCheck, sleepTime):
    global flag
    flag = True
    while 1:
        print(auto, cdCheck, sleepTime)
        time.sleep(2)
    # searchTarget()


def changeLoseFlag(num):
    global loseFlag
    loseFlag = num


if __name__ == "__main__":
    # jjcStart()
    # searchTarget()
    # backSearchTarget()
    # changeUpDown(1)
    # sleepTimeS = max(300, 60)
    # sleepTimeE = min(302, 304)
    # sleepTime = random.randint(sleepTimeS, sleepTimeE)
    # print(sleepTime)
    changeAttackTeamEx()
