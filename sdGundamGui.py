import easygui as gui
from games import sdGundamG as sd
from dao import changeVar as cv

flag = False

choices = ("请选择脚本：",
           "自动PVP",
           "半自动拉满",
           "====================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "SD高达G世纪", choices=choices)


def test(name):
    gui.msgbox(name)

def inputBox():
    sd.cvInit(cv.DBLPath, cv.SDPath)  # 办公室
    # db.cvInit(cv.DBLPath, cv.DBLdeviceHome)  # 家
    return gui.integerbox(msg='请输入次数,0为不限制', title='自动次数：', default=None, lowerbound=0, upperbound=9999, image=None,
                          root=None)

def setFlag():
    global flag
    flag = True


if __name__ == "__main__":
    # getTime()
    setFlag()
    while flag:
        choice = ''
        choice = main()
        if "自动PVP".__eq__(choice):
            sd.autoRush()
        elif "半自动拉满".__eq__(choice):
            sd.autoMaxSelect()
        elif choice == "关闭":
            break
