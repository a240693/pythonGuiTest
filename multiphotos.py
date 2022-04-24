import pyautogui
import daoImpl
import time
# from . import test
path = 'F:\\pyTest\\'
class Photo:
    def __init__(self):
        self.name = "默认"
        self.x = 0
        self.y = 0

    def writeSelf(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y

    def onlySearchOnce(self,name,mode,times):
        try:
            x, y, w, h = pyautogui.locateOnScreen(path + name + '.png', grayscale=True)
            x, y = pyautogui.center((x, y, w, h))
            self.writeSelf(name,x,y)
            print("{}.png在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(name, x, y, w, h))
            return 1
        except:
            return 0

    # 随便你传几张照片进来，找到哪张就返回哪张照片的坐标和名字。
    def loopSearch(self,gamePagesMap):
        count = 0
        while True:
            for i in gamePagesMap :
                #print("开始查找{}".format(i))
                if 0 != self.onlySearchOnce(i,3,3):
                    return self
            count += 1
            if count == 5:
                print("找不到5次，休息0.3秒")
                time.sleep(0.3)
                count = 0

    # 进入游戏用，找不到会自动点击左键一次。
    def firstClickSearch(self,gamePagesMap):
        count = 0
        while True:
            for i in gamePagesMap :
                if 0 != self.onlySearchOnce(i,3,3):
                    return self
                else:
                    pyautogui.click(button="left")
                    time.sleep(5)
            count += 1
            if count == 5:
                print("找不到5次，休息0.3秒")
                time.sleep(0.3)
                count = 0


    def __str__(self):
        return print(self.name,self.x,self.y)