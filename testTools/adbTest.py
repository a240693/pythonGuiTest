#emulator-5566
from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__,devices=["Android://127.0.0.1:5037/emulator-5566"])

path = 'F:\\pyTest\\'

if __name__ == "__main__":
    try:
        print(poco.adb_client.get_device_info())  # 获取设备信息
        temp = Template(path +"mrfz.png", record_pos=(0.779, 0.382), resolution=(720, 1280))
        print(temp)
        touch(temp)
    finally:
        # generate html report
        simple_report(__file__, logpath=True)