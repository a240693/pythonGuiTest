import easygui as gui
from games import kgAir as kgA
from dao import changeVar as cv

flag = False

choices = ("请选择脚本：",
           "自动PVP",
           "坎公日常第一个",
           "坎公日常第二个",
           "坎公日常第三个",
           "====================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "←_→", choices=choices)


def test(name):
    gui.msgbox(name)


def setFlag():
    global flag
    flag = True


if __name__ == "__main__":
    # getTime()
    setFlag()
    kgA.cvInit(cv.kgAirPath, cv.kgDevice2)  # 办公室
    # kgA.cvInit(cv.kgAirPath, cv.kgDevice3)  # 家
    while flag:
        choice = ''
        choice = main()
        if "自动PVP".__eq__(choice):
            kgA.pvpAuto()
        elif "坎公日常第一个".__eq__(choice):
            kgA.dailyAir(1)
        elif "坎公日常第二个".__eq__(choice):
            kgA.dailyAir(2)
        elif "坎公日常第三个".__eq__(choice):
            kgA.dailyAir(3)
        elif choice == "关闭":
            break