import easygui as gui
from games import honkaiTrain

flag = False

choices = ("请选择功能：",
           "打开游戏",
           "获取任务奖励",
           "自动60次花萼金",
           "半自动模拟世界",
           "自动远征获取",
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
    while flag:
        choice = ''
        choice = main()
        if "获取任务奖励".__eq__(choice):
            honkaiTrain.getMission()
        elif "打开游戏".__eq__(choice):
            honkaiTrain.openGame()
        elif "自动60次花萼金".__eq__(choice):
            honkaiTrain.auto60()
        elif "半自动模拟世界".__eq__(choice):
            honkaiTrain.skillStart("欢愉")
        elif "自动远征获取".__eq__(choice):
            honkaiTrain.autoSearch()
        elif choice == "关闭":
            break
