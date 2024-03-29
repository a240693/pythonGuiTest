import numpy as np
import pyautogui;
import time;
import subprocess;
import _thread
import time
import platform
import cv2

# path = 'F:\\pyTest\\'
# path = "F:\\pyTest\\honkai\\"
path = "F:\\pyTest\\honkaiTrain\\"

# 获取颜色
def getcolour(x, y):
    img = pyautogui.screenshot()
    img.save
    co = img.getpixel((x, y))
    return co;


# 计时器
def countDown(m, s):
    timeLeft = 60 * m + s
    while (timeLeft > 0):
        print("还剩下：", timeLeft)
        time.sleep(1)
        timeLeft = timeLeft - 1


def fprocess():
    returnWord = subprocess.run(["D:", "dir"], shell=True, check=True)
    print(returnWord)


def showDetail():
    r = platform.architecture()
    print(r)


def my_cv_imread(filepath):
    # 使用imdecode函数进行读取 cv2.IMREAD_COLOR
    img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # cv2.imshow('img', img)  # 显示图像
    # cv2.waitKey(0)
    return img


def cvTest():
    filepath = path + 'chrome' + '.png'
    img = my_cv_imread(filepath)  # 获取读取的图像
    pyautogui.locateOnScreen(img)
    cv2.imshow('img', img)  # 显示图像
    cv2.waitKey(0)


def placeTest():
    countDown(0, 3)
    confidenPoint = 0.9
    x1, y1 = pyautogui.position();
    # name = 'star\\换人页标识升序'
    name = '星铁挑战'
    filepath = path + name + '.png'
    img = my_cv_imread(filepath)
    x, y, w, h = pyautogui.locateOnScreen(img, grayscale=True, confidence=confidenPoint)
    print(x,y)
    x, y = pyautogui.center((x, y, w, h))

    print("{} 颜色为：{},该坐标为{}".format(name, (getcolour(x, y)), (x, y)));
    print("鼠标坐标为{}".format((x1, y1)));
    print("差值为 ({}, {})".format((x1 - x), (y1 - y)));
    pyautogui.moveTo(x, y)


def scrollTest():
    countDown(0, 3)
    pyautogui.scroll(100, x=100, y=100)

def keyTest():
    time.sleep(3)
    pyautogui.keyDown('altleft')
    time.sleep(10)
    pyautogui.keyUp('altleft')

if __name__ == '__main__':
    # scrollTest()
    # keyTest()
    placeTest()
    # fprocess()
