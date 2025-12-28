import pyautogui
import time
import random
import pydirectinput


from dao import dao, daoImpl, multiphotos, resultMap
from dao import changeVar as cv
import _thread
import keyboard
# from pynput import keyboard

cv._init()
cv.set_value("path", cv.sdOCPath)

global flag
flag = False

global keys
keys = []

global oldKey
oldKey = "0"

global h

global testFlag
testFlag = 0

def attackTest():
    print("开始自动重击".format())
    while 1:
        while flag:
            # 深夜脑残不知道怎么自定义了，直接这么用着吧。 2024年10月1日01:53:09
            pyautogui.tripleClick(button="left", interval=0.5)
            pyautogui.doubleClick(button="left", interval=0.5)
            pyautogui.mouseDown(button="left")
            time.sleep(0.5)
            pyautogui.mouseUp(button="left")
        time.sleep(1)


def changeTeam():
    print("开始自动切人".format())
    while 1:
        while flag:
            for i in range(1, 4):
                if 2 == i:
                    pyautogui.press("q", presses=2, interval=0.1)
                pyautogui.press(str(i), presses=3, interval=1)
                pyautogui.press("e", presses=5, interval=0.5)
                pyautogui.press("r", presses=2, interval=1)
                # pyautogui.press("q", presses=6, interval=0.2)
                # pyautogui.press("r", presses=2, interval=1)
                time.sleep(4)
                if not flag:
                    break


        # dao.pressKey('r')
        time.sleep(2)
def startAutoFight():
    try:
        print("自动战斗测试".format())
        _thread.start_new_thread(attackTest, ())
        _thread.start_new_thread(changeTeam, ())
        _thread.start_new_thread(autoFightEnd, ())
        # time.sleep(60)
        # print("关闭战斗测试".format())
        # flag = False
    except:
        print("Error: 无法启动线程")


def on_press(event):
    global keys
    global oldKey
    # print(event)
    if str(event) != oldKey:
        oldKey = str(event)
        keys.append(str(event))

def duelKeys():
    global flag
    while 1:
        if keys.__len__() != 0:
            key = keys.pop()
            print("当前值为：{}".format(key))
            # if "Key.f9".__eq__(key):
            #     # print("结果是：","Key.f3".__eq__(str(event)))
            #     flag = True
            #     print("开启自动战斗")
            #     continue
            #
            # if "Key.f10".__eq__(key):
            #     flag = False
            #     print("关闭自动战斗")
            #     continue

def on_release(event):
    # print("松开的是：", event)
    pass


def pynputTest():
    # listener = keyboard.Listener(
    #     on_press=on_press,
    #     # on_release=on_release
    # )
    # listener.start()
    # 第二种
    # with keyboard.Listener(on_press=on_press) as listener:
    #     listener.join()
    # 第三种 热键获取
    # with keyboard.GlobalHotKeys({
    #     '<f9>': f9test,
    #     '<f10>': f10test,
    # }) as h:
    #     h.join()
    # 第四种 热键获取
    global h
    print("线程开启。")
    h = keyboard.GlobalHotKeys({
        # 'a': pressSpace,
        # 's': pressSpace,
        # 'w': pressSpace,
        # 'd': pressSpace,
        '<f9>': f9test,
        '<f10>': f10test,
    })
    h.start()

def f9test():
    global flag
    flag = True
    print("开启自动战斗。")
    # h.stop()
    # time.sleep(10)
    global testFlag
    testFlag = 1

def f10test():
    global flag
    flag = False
    # print("关闭自动战斗,线程休眠3秒。")
    print("关闭自动战斗。")
    # h.stop()ree
    # time.sleep(10)
    # 已选择，线程休眠3秒。
    global testFlag
    testFlag = 1

def pressSpace():
    # h.stop()
    print("检测到方向键,线程休眠3秒。")
    time.sleep(10)
    global testFlag
    testFlag = 1

def keyboardTest():
    while 1:
        if keyboard.is_pressed("f9"):
            # print("检测到F9。")
            f9test()
            break

        if keyboard.is_pressed("f10"):
            # print("检测到F10。")
            f10test()
            break

        time.sleep(1)



# 自动剧情。
def autoText():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "LV主界面标识",
        "推进选项",
        "对话选项",
        "F键",
    ]
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if name.__eq__("F键"):
            dao.pressKey("F")
            continue

        if name.__eq__("对话选项"):
            dao.pressKey("F")
            continue

        if name.__eq__("LV主界面标识"):
            break

        dao.moveTo(x, y)

def startAutoFightEntry():
    startAutoFight()
    while 1:
        keyboardTest()
    while True:

        pass

# 自动剧情。
def autoFightEnd():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "挑战成功",
        "挑战成功2",
        "挑战成功3-2k",
        "挑战成功4-2k",
        "深渊挑战成功",
    ]
    print("开始检测是否打完。".format())
    while 1:
        # photoMap.loopSearch(photoMaps)
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if  "挑战成功" in name:
            f10test()
            continue

        # dao.moveTo(x, y)

# 抽蛋。
def autoGacha():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "ESC",
        "确认",
        "购买",
        "抽取扭蛋",
    ]
    print("开始检测是否打完。".format())
    while 1:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name

        if "ESC".__eq__(name):
            pyautogui.press("esc", presses=3, interval=1)
            pydirectinput.keyDown("esc")
            time.sleep(0.02)
            pydirectinput.keyUp("esc")
            continue

        dao.moveToNew(x, y)
        # pyautogui.mouseDown()
        # time.sleep(0.02)  # 短暂按下延迟
        # pyautogui.mouseUp()

if __name__ == '__main__':
    autoGacha()
    # _thread.start_new_thread(startAutoFight,())
    # _thread.start_new_thread(duelKeys,())
