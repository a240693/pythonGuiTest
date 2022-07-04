path = 'F:\\pyTest\\'
# path = 'D:\\pyTest\\'
Fpath = 'F:\\pyTest\\'
Dpath = 'D:\\pyTest\\'
FgoPath = 'F:\\pyTest\\fgo\\'
kgDevice = "Android://127.0.0.1:5037/emulator-5566"
deviceNo = "emulator-5560"
device = "Android://127.0.0.1:5037/emulator-5560"


# device = "Android://127.0.0.1:5037/emulator-5554"
# device = "Android://127.0.0.1:5037/127.0.0.1:5555"
def _init():  # 初始化
    global gloVar
    gloVar = {"device": device, "path": FgoPath}


def set_value(key, value):
    # 定义一个全局变量
    gloVar[key] = value


def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return gloVar[key]
    except:
        print('读取' + key + '失败\r\n')
