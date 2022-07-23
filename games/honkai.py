import _thread
import time

from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from dao import airMultiPhotos as air
from dao import changeVar as cv
import logging

# 日志只输出INFO等级，debugger等级不输出。
# logger = logging.getLogger("airtest")
# logger.setLevel(logging.INFO)

cv._init()
cv.set_value("path", cv.kgAirPath)
cv.set_value("device", cv.kgDevice)

if __name__ == "__main__":
    auto_setup(__file__, devices=["Windows:///?title_re=崩坏3"])