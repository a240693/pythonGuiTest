import easygui as gui
from games import dblAir as db
from dao import changeVar as cv

flag = False

choices = ("请选择脚本：",
           "自动PVP",
           "100层",
           "团队战",
           "RUSH",
           "获取每日材料",
           "获取委托",
           "获取7小时委托",
           "超激斗",
           "自动强化",
           "自动钢镚",
           "自动购买活动物品",
           "每日汇总",
           "====================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "←_→", choices=choices)


def test(name):
    gui.msgbox(name)

def inputBox():
    return gui.integerbox(msg='请输入次数,0为不限制', title='自动次数：', default=None, lowerbound=0, upperbound=9999, image=None,
                          root=None)

def setFlag():
    global flag
    flag = True


if __name__ == "__main__":
    # getTime()
    setFlag()
    db.cvInit(cv.DBLPath, cv.DBLdevice)  # 办公室
    # db.cvInit(cv.DBLPath, cv.DBLdeviceHome)  # 家
    while flag:
        choice = ''
        choice = main()
        if "自动PVP".__eq__(choice):
            index = inputBox()
            db.pvpAuto(index)
        elif "RUSH".__eq__(choice):
            db.autoRush()
        elif "100层".__eq__(choice):
            db.auto100()
        elif "团队战".__eq__(choice):
            index = inputBox()
            db.autoBattle(index)
        elif "获取每日材料".__eq__(choice):
            db.getBonus()
        elif "获取委托".__eq__(choice):
            db.getMarch()
        elif "获取7小时委托".__eq__(choice):
            db.autoGet7hour()
        elif "自动强化".__eq__(choice):
            db.autoZenkai()
        elif "超激斗".__eq__(choice):
            db.superBattle()
        elif "自动钢镚".__eq__(choice):
            db.autoCoin()
        elif "自动购买活动物品".__eq__(choice):
            db.autoBuyEvent()
        elif "每日汇总".__eq__(choice):
            db.dailyAll()
        elif choice == "关闭":
            break
