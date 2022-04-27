import easygui as gui
from games import pcr

choices = ("自动换防时间：",
           "不等",
           "3分钟",
           "10分钟",
           "20分钟",
           "随机(1-20)",
           "====================",
           "关闭")

def main():
    return gui.choicebox("脚本选择", "瞎写的随便", choices=choices)


def test(name):
    gui.msgbox(name)

while True:
    choice = ''
    choice = main()
    if choice == "3分钟":
        pcr.autoChangeDefenceP(3)
    elif choice == "10分钟":
        pcr.autoChangeDefenceP(10)
    elif choice == "不等":
        pcr.autoChangeDefenceP(0.01)
    elif choice == "20分钟":
        pcr.autoChangeDefenceP(20)
    elif choice == "随机(1-20)":
        pcr.autoChangeDefenceP(0)
    elif choice == "关闭":
        break

