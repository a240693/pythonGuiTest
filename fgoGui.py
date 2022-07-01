import datetime
import easygui as gui
from testTools import timeTest
from games import fgo

flag = False

choices = ("请选择副本：",
           "90",
           "90+",
           "====================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "←_→", choices=choices)


def test(name):
    gui.msgbox(name)


# def getTime():
#     time = timeTest.get_beijin_time()
#     time1 = datetime.datetime(2022, 6, 14, 00, 00, 00)
#     # print("现在的时间是{}".format(time))
#     # print("现在的时间是{}".format(time1))
#     # print("两个相减:{}".format(time1 - time))
#     if time < time1:
#         setFlag()
#         return;
#     elif time > time1:
#         print("已过期。")


def setFlag():
    global flag
    flag = True


if __name__ == "__main__":
    # getTime()
    while flag:
        choice = ''
        choice = main()
        if "90".__eq__(choice):
            fgo.battleStart()
        elif "90+".__eq__(choice):
            fgo.battleStartNew()
        elif choice == "关闭":
            break
