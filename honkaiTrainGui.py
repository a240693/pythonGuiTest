import easygui as gui
from games import honkaiTrain

flag = False

choices = ("请选择功能：",
           "打开游戏",
           "获取任务奖励",
           "自动60次花萼金",
           "半自动模拟世界",
           "自动远征获取",
           "自动重开试做",
           "自动编队 - 卡夫卡",
           "自动编队 - 克拉拉",
           "自动编队 - 静流",
           "====================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "星轨", choices=choices)


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
            honkaiTrain.skillStart("虚无")
        elif "自动远征获取".__eq__(choice):
            honkaiTrain.autoSearch()
        elif "自动编队 - 卡夫卡".__eq__(choice):
            honkaiTrain.autoTeam(0)
        elif "自动编队 - 克拉拉".__eq__(choice):
            honkaiTrain.autoTeam(1)
        elif "自动编队 - 静流".__eq__(choice):
            honkaiTrain.autoTeam(2)
        elif "自动重开试做".__eq__(choice):
            honkaiTrain.autoRestart()
        elif choice == "关闭":
            break
