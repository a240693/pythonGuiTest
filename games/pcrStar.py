import pyautogui as py
import time
import random

from dao import dao, daoImpl, multiphotos, resultMap
import _thread


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
    changeUpDown(upDown[0])
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
def changeUpDown(upDown):
    dao.searchPhotoPcr('star\\防御页总战力', 3, 674, -344)
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


if __name__ == "__main__":
    autoChangeDefenceP(2)
    # changeUpDown(1)
