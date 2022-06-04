import datetime
import easygui as gui
from testTools import timeTest
from games import pcrStar

flag = False

choices = ("自动换防时间：",
           "3秒",
           "====================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "←_→", choices=choices)


def test(name):
    gui.msgbox(name)


def getTime():
    time = timeTest.get_beijin_time()
    time1 = datetime.datetime(2022, 6, 14, 00, 00, 00)
    # print("现在的时间是{}".format(time))
    # print("现在的时间是{}".format(time1))
    # print("两个相减:{}".format(time1 - time))
    if time < time1:
        setFlag()
        return;
    elif time > time1:
        print("已过期。")


def setFlag():
    global flag
    flag = True


if __name__ == "__main__":
    getTime()
    while flag:
        choice = ''
        choice = main()
        if choice == "3秒":
            pcrStar.autoChangeDefenceP(0.01)
        elif choice == "关闭":
            break
