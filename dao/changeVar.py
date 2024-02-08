path = 'F:\\pyTest\\'
# path = 'D:\\pyTest\\'
Fpath = 'F:\\pyTest\\'
Dpath = 'D:\\pyTest\\'
FgoPath = 'F:\\pyTest\\fgo\\'
kgAirPath = 'F:\\pyTest\\kgAir\\'
mrfzPath = 'F:\\pyTest\\mrfz\\'
bluePath = 'F:\\pyTest\\blue\\'
trainPath = 'F:\\pyTest\\honkaiTrain\\'
speedCarPath = 'F:\\pyTest\\speedCar\\'
pcrAirPath = 'F:\\pyTest\\pcrAir\\'

kgDeviceHome = "Android://127.0.0.1:5037/emulator-5566"
kgDeviceOffice = "Android://127.0.0.1:5037/emulator-5558"
kgDevice3 = "Android://127.0.0.1:5037/127.0.0.1:7555"#mumu
kgDeviceAnotherHome = "Android://127.0.0.1:5037/emulator-5558"
kgDeviceAnotherHome9 = "Android://127.0.0.1:5037/emulator-5554"
kgDevice = kgDeviceAnotherHome9

deviceNo = "emulator-5560"
honkai = "Windows:///?title_re=崩坏3"
honkaiPath = "F:\\pyTest\\honkai\\"
deviceAk = "Android://127.0.0.1:5037/emulator-5554"
# device = "Android://127.0.0.1:5037/emulator-5554"
# device = "Android://127.0.0.1:5037/emulator-5560"
device = "Android://127.0.0.1:5037/emulator-5554"

DBLdeviceOffice = "Android://127.0.0.1:5037/emulator-5560"
DBLdeviceHome = "Android://127.0.0.1:5037/emulator-5564"
DBLdeviceAnotherHome = "Android://127.0.0.1:5037/emulator-5560"
DBLdevice = DBLdeviceAnotherHome

DBLPath = "F:\\pyTest\\DBL\\"

mrfzDeviceHome = 'Android://127.0.0.1:5037/emulator-5562'
mrfzDeviceOffice = "Android://127.0.0.1:5037/emulator-5558"
mrfzDeviceAnotherHome = "Android://127.0.0.1:5037/emulator-5558"
mrfzDevice = mrfzDeviceAnotherHome

blueDeviceHome = 'Android://127.0.0.1:5037/emulator-5562'
blueDeviceOffice = "Android://127.0.0.1:5037/emulator-5558"
blueAnotherHome = "Android://127.0.0.1:5037/emulator-5558"
blueDevice = mrfzDeviceAnotherHome

pcrAirDeviceAnotherHome = "Android://127.0.0.1:5037/emulator-5556"
pcrAirDeviceHome = ''
pcrAirDeviceOffice = ''
pcrAirDevice = pcrAirDeviceAnotherHome

FgoDeviceHome = "Android://127.0.0.1:5037/emulator-5566"
FgoDeviceOffice = "Android://127.0.0.1:5037/emulator-5558"
FgoDeviceAnotherHome = "Android://127.0.0.1:5037/emulator-5558"
FgoDevice = FgoDeviceAnotherHome


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
