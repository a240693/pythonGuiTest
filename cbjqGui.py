import easygui as gui
from games import cbjq

flag = False

choices = ("请选择功能：",
           "打开游戏",
           "全每日试做",
           "====================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "尘白禁区", choices=choices)


def test(name):
    gui.msgbox(name)

def setFlag():
    global flag
    flag = True


if __name__ == "__main__":
    # getTime()
    setFlag()
    while flag:
        choice = ''
        choice = main()
        if "全每日试做".__eq__(choice):
            cbjq.dailyAll()
        elif "打开游戏".__eq__(choice):
            cbjq.openGame()
            cbjq.dailyAll()
        elif choice == "关闭":
            break
