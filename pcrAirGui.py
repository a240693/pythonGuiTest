import easygui as gui
from games import pcrAir

flag = False

choices = ("请选择功能：",
           "自动推图",
           "三号轮流",
           "====================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "PCR", choices=choices)


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
        if "自动推图".__eq__(choice):
            pcrAir.autoFight()
        elif "三号轮流".__eq__(choice):
            pcrAir.openGame(0)
        elif choice == "关闭":
            break
