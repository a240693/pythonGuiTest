import easygui as gui
from games import pcrAir

flag = False

choices = ("请选择功能：",
           "自动推图",
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
        if "自动推图".__eq__(choice):
            pcrAir.autoFight()
        elif "自动推图".__eq__(choice):
            pcrAir.autoFight()
        elif choice == "关闭":
            break
