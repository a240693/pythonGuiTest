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
MingChaoPath = 'F:\\pyTest\\MingChao\\'
sdOCPath = 'F:\\pyTest\\SDOC\\'
SDPath = "F:\\pyTest\\SD\\"
cbjqPath = 'F:\\pyTest\\cbjq\\'
DBLPath = "F:\\pyTest\\DBL\\"
honkaiPath = "F:\\pyTest\\honkai\\"

kgDeviceHome = "Android://127.0.0.1:5037/emulator-5566"
kgDeviceOffice = "Android://127.0.0.1:5037/emulator-5558"
kgDevice3 = "Android://127.0.0.1:5037/127.0.0.1:7555"#mumu
kgDeviceAnotherHome = "Android://127.0.0.1:5037/emulator-5558"
kgDeviceAnotherHome9 = "Android://127.0.0.1:5037/emulator-5554"
kgDevice = kgDeviceAnotherHome9

deviceNo = "emulator-5560"
honkai = "Windows:///?title_re=崩坏3"

deviceAk = "Android://127.0.0.1:5037/emulator-5554"
# device = "Android://127.0.0.1:5037/emulator-5554"
# device = "Android://127.0.0.1:5037/emulator-5560"
device = "Android://127.0.0.1:5037/emulator-5554"

DBLdeviceOffice = "Android://127.0.0.1:5037/emulator-5560"
DBLdeviceHome = "Android://127.0.0.1:5037/emulator-5564"
DBLdeviceAnotherHome = "Android://127.0.0.1:5037/emulator-5560"
DBLdeviceAnotherHome9 = "Android://127.0.0.1:5037/emulator-5556"
DBLdeviceAnotherHomeMumu = "Android://127.0.0.1:5037/127.0.0.1:7555"
DBLdevice = DBLdeviceAnotherHomeMumu

SDdeviceOffice = "Android://127.0.0.1:5037/emulator-5560"
SDdeviceHome = "Android://127.0.0.1:5037/emulator-5564"
SDdeviceAnotherHome = "Android://127.0.0.1:5037/emulator-5560"
SDdeviceAnotherHome9 = "Android://127.0.0.1:5037/emulator-5556"
SDdeviceAnotherHomeMumu = "Android://127.0.0.1:5037/127.0.0.1:7555"
SDdevice = SDdeviceAnotherHomeMumu



mrfzDeviceHome = 'Android://127.0.0.1:5037/emulator-5562'
mrfzDeviceOffice = "Android://127.0.0.1:5037/emulator-5558"
mrfzDeviceAnotherHome = "Android://127.0.0.1:5037/emulator-5558"
mrfzDevice = mrfzDeviceAnotherHome

blueDeviceHome = 'Android://127.0.0.1:5037/emulator-5562'
blueDeviceOffice = "Android://127.0.0.1:5037/emulator-5558"
blueAnotherHome = "Android://127.0.0.1:5037/emulator-5558"
blueAnotherHome9 = "Android://127.0.0.1:5037/emulator-5554"
blueDevice = blueAnotherHome9

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
