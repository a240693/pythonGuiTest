# emulator-5566
from airtest.core.api import *
from airtest.report.report import simple_report

path = 'F:\\pyTest\\kgAir\\'
fgoPath = 'F:\\pyTest\\fgo\\'

def testPhotoFgo(name = "幕间物语进入"):
    try:
        auto_setup(__file__, devices=["Android://127.0.0.1:5037/emulator-5560"])
        temp = Template(fgoPath + name + ".png",rgb=False)
        pos = exists(temp)
        touch(pos)
        print("{}找到了,坐标为：{}".format(name, pos))
    except Exception as e:
        return 0
    # finally:
    #     # generate html report
    #     simple_report(__file__, logpath=True,logfile="F:\\")

def testPhotoKg(name = "坎公挑战卷不足"):
    try:
        auto_setup(__file__, devices=["Android://127.0.0.1:5037/emulator-5566"])
        temp = Template(path + name + ".png",threshold=0.7,rgb=False)
        pos = exists(temp)
        touch(pos)
        print("{}找到了,坐标为：{}".format(name,pos))
    except Exception as e:
        return 0



if __name__ == "__main__":
    testPhotoFgo()