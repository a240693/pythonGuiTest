import pyHook
import pythoncom
# 用不了，只能用pyHook3
# 但pyHook3太麻烦了所以寄。

# 监听鼠标调用
def onMouseEvent(event):
    if (event.MessageName != "mouse move"):
        print(event.MessageName)
    return True


def onKeyboardEvent(event):
    print(event.Key)
    return True


def main():
    hm = pyHook.HookManager()
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # hm.MouseAll = onMouseEvent
    # hm.HookMouse()
    pythoncom.PumpMessages()


if __name__ == "__main__":
    main()
