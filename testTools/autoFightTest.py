import pyautogui
import time
import _thread
from pynput import keyboard

global flag
flag = False


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


def changeTeam():
    print("开始自动切人".format())
    while 1:
        while flag:
            for i in range(1, 4):
                pyautogui.press(str(i), presses=1, interval=1)
                pyautogui.press("e", presses=5, interval=0.5)
                time.sleep(1)
                pyautogui.press("r", presses=2, interval=1)
                time.sleep(2)
                pyautogui.press("q", presses=6, interval=0.2)
                pyautogui.press("r", presses=2, interval=1)
                time.sleep(2)
                if not flag:
                    break
        # dao.pressKey('r')11


def startAutoFight():
    try:
        print("给你两秒切过去。".format())
        time.sleep(2)
        print("自动战斗测试".format())
        _thread.start_new_thread(attackTest, ())
        _thread.start_new_thread(changeTeam, ())
        # time.sleep(60)
        # print("关闭战斗测试".format())
        # flag = False
    except:
        print("Error: 无法启动线程")


def on_press(event):
    # tmd， 没办法了，event不会自动刷新所以一直按，真铸币，2024年10月1日16:24:43
    print("输入：", event)
    global flag
    if "Key.f9".__eq__(str(event)):
        # print("结果是：","Key.f3".__eq__(str(event)))
        flag = True
        print("开启自动战斗")

    if "Key.f10".__eq__(str(event)):
        flag = False
        print("关闭自动战斗")


def on_release(event):
    # print("松开的是：", event)
    pass


def pynputTest():
    listener = keyboard.Listener(
        on_press=on_press, on_release=on_release)
    listener.start()


if __name__ == '__main__':
    # pyautogui.mouseDown(button="left")
    # time.sleep(1)
    # pyautogui.mouseUp(button="left")
    # dao.pressKey('pagedown')
    pynputTest()
    startAutoFight()
    while True:
        pass
