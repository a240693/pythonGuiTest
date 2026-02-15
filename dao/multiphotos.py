import pyautogui
import time
# from . import test
from . import dao
from . import changeVar as cv

path = cv.path
# path = 'D:\\pyTest\\'

class Photo:
    def __init__(self):
        self.name = "默认"
        self.x = 0
        self.y = 0
        global path
        path = cv.get_value("path")

    def writeSelf(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def onlySearchOnce(self, name, mode, times):
        try:
            filepath = path + name + '.png'
            img = dao.my_cv_imread(filepath)  # 获取读取的图像
            x, y, w, h = pyautogui.locateOnScreen(img, grayscale=False, confidence=0.7)
            x, y = pyautogui.center((x, y, w, h))
            self.writeSelf(name, x, y)
            print("{}.png在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(name, x, y, w, h))
            return 1
        except Exception as e:
            # print(e)
            return 0

    # 随便你传几张照片进来，找到哪张就返回哪张照片的坐标和名字。
    def loopSearch(self, gamePagesMap):
        count = 0
        while True:
            for i in gamePagesMap:
                print("————————开始查找：{}".format(i))
                time.sleep(0.2)
                if 0 != self.onlySearchOnce(i, 3, 3):
                    return self
            count += 1
            if count == 5:
                # print("找不到5次，休息0.3秒")
                time.sleep(0.1)
                count = 0

    # 进入游戏用，找不到会自动点击左键一次。
    def firstClickSearch(self, gamePagesMap):
        count = 0
        while True:
            for i in gamePagesMap:
                if 0 != self.onlySearchOnce(i, 3, 3):
                    return self
                else:
                    pyautogui.click(button="left")
                    time.sleep(5)
            count += 1
            if count == 5:
                print("找不到5次，休息0.3秒")
                time.sleep(0.3)
                count = 0

    def searchPhoto(self, name):
        count = 0
        found = False
        while not found:
            try:
                filepath = path + name + '.png'
                img = dao.my_cv_imread(filepath)  # 获取读取的图像
                x, y, w, h = pyautogui.locateOnScreen(img, grayscale=True, confidence=0.9)
                x, y = pyautogui.center((x, y, w, h))
                print("{}.png在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(name, x, y, w, h))
                found = True
                self.writeSelf(name, x, y)
                return self
            except:
                count = count + 1
                print('{}.png没找到，第{}次,3秒后重试'.format(name, count))
                time.sleep(3)
                if count > 20:
                    print("超过{}次没找到，判断为卡住，请人工协助。".format(count))
                    exit()

    def __str__(self):
        return print(self.name, self.x, self.y)
