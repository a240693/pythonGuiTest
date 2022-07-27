import easygui as gui
from games import fgo

flag = False

choices = ("请选择副本：",
           "90",
           "90+",
           "无限池",
           "自回体90",
           "单次",
           "种火",
           "种火单次",
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
            fgo.battleStartNew(True,select = 2)
        elif "90+".__eq__(choice):
            fgo.battleStartNew(True, select = 1)
        elif "无限池".__eq__(choice):
            fgo.egg10()
        elif "自回体90".__eq__(choice):
            fgo.battleStartNew(True, False, 2)
        elif "单次".__eq__(choice):
            fgo.battleStartNew(False, False, 2)
        elif "种火".__eq__(choice):
            # fgo.custom(1)
            fgo.enterGame()
        elif "种火单次".__eq__(choice):
            fgo.custom(1)
        elif choice == "关闭":
            break
