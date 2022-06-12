import _thread

import easygui as gui
from games import pcrStar

flag = True
choices = (
    "自动",
    "碎CD",
    "间隔调整",
    "默认",
    "=================================",
    "关闭",
)


def main():
    return gui.multchoicebox("脚本选择", "瞎写的随便", choices=choices)


def test(name):
    gui.msgbox(name)


def inputBox():
    return gui.integerbox(msg='请输入间隔', title='间隔：', default=None, lowerbound=0, upperbound=9999, image=None, root=None)


def jjcStart(auto, cdCheck, sleepTime):
    try:
        global flag
        flag = True
        _thread.start_new_thread(pcrStar.newJJCenter, (auto, cdCheck, sleepTime))
        _thread.start_new_thread(start, ())
    except:
        print("Error: 无法启动线程")

    while 1:
        if flag == False:
            break
        pass


def start():
    flag1 = True
    while flag1:
        try:
            choice = ''
            choice = main()
            print(choice)
            for i in choice:
                if "关闭".__eq__(i):
                    flag1 = False
                    break
                elif "自动".__eq__(i):
                    auto = 1
                elif "碎CD".__eq__(i):
                    cdCheck = 1
                elif "间隔调整".__eq__(i):
                    sleepTime = inputBox()
            if flag1:
                jjcStart(auto, cdCheck, sleepTime)
        except:
            auto = 0
            cdCheck = 0
            sleepTime = 5 * 60
            jjcStart(auto, cdCheck, sleepTime)
            print("默认")


if __name__ == "__main__":
    start()
    # pcrStar.newJJCenter()
