import easygui as gui
from games import blueAir as blue
from dao import changeVar as cv

flag = False

choices = ("请选择脚本：",
           "自动剧情",
           "自动战斗",
           "自动升级",
           "自动每日",
           "自动奖励",
           "自动情人节活动",
           "自动-1",
           "自动-1省略",
           "====================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "碧蓝档案", choices=choices)


def test(name):
    gui.msgbox(name)


def setFlag():
    global flag
    flag = True


if __name__ == "__main__":
    # getTime()
    setFlag()
    blue.cvInit(cv.bluePath, cv.blueDevice)  # 家
    # kgA.cvInit(cv.kgAirPath, cv.kgDevice)  # 家
    while flag:
        choice = ''
        choice = main()
        if "自动战斗".__eq__(choice):
            blue.autoStart()
        elif "自动剧情".__eq__(choice):
            blue.autoText()
        elif "自动升级".__eq__(choice):
            blue.autoAddLv()
        elif "自动每日".__eq__(choice):
            blue.dailyAll()
        elif "自动-1".__eq__(choice):
            blue.autoSkipBattle()
        elif "自动-1省略".__eq__(choice):
            blue.autoSkipBattleSimple(0.1)
        elif "自动情人节活动".__eq__(choice):
            blue.eventChoco()
        elif "自动奖励".__eq__(choice):
            blue.eventRun()
        elif choice == "关闭":
            break
