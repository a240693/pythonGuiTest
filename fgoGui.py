import easygui as gui
from games import fgo

flag = False

choices = ("请选择副本：",
           "90",
           "90+",
           "无限池",
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
    setFlag()
    while flag:
        choice = ''
        choice = main()
        if "90".__eq__(choice):
            fgo.battleStartNew(True, 2)
        elif "90+".__eq__(choice):
            fgo.battleStartNew(True, 1)
        elif "无限池".__eq__(choice):
            fgo.egg10()
        elif choice == "关闭":
            break
