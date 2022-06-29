import pyautogui
import time
# from . import test
from . import changeVar as cv
from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__, devices=[cv.device])

path = cv.FgoPath


# path = 'D:\\pyTest\\'

class Photo:
    def __init__(self):
        self.name = "默认"
        self.pos = (0, 0)

    def writeSelf(self, name, pos):
        self.name = name
        self.pos = pos

    # 循环 找到图片就返回坐标和名字回最顶层。
    def loopSearch(self, photoMaps):
        for photoMap in photoMaps:
            result = self.appearThenClick(photoMap)
            if 1 == result:
                return self
            elif 0 == result:
                continue

    # 查找图片，3秒内判断该图片有没有出现，没有则找下一张。
    # 有就返回1，无就返回0.
    def appearThenClick(self, photoMap):
        try:
            photo = Template(path + photoMap + ".png")
            pos = exists(photo)
            if pos:
                self.writeSelf(photoMap, pos)
                return 1
            else:
                return 0
        except:
            return 0
        finally:
            simple_report(__file__, logpath=True)

    def __str__(self):
        return print(self.name, self.pos)
