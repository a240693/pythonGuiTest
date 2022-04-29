import numpy as np
import pyautogui;
import time;
import subprocess;
import _thread
import time
import platform
import cv2

path = 'F:\\pyTest\\'


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
    name = '坎公44段位更新'
    filepath = path + name + '.png'
    img = my_cv_imread(filepath)
    x, y, w, h = pyautogui.locateOnScreen(img, grayscale=True, confidence=confidenPoint)
    x, y = pyautogui.center((x, y, w, h))

    print("{}颜色为：{},该坐标为{}".format(name, (getcolour(x, y)), (x, y)));
    print("鼠标坐标为{}".format((x1, y1)));
    print("差值为 ({}, {})".format((x1 - x), (y1 - y)));
    pyautogui.moveTo(x, y)


if __name__ == '__main__':
    placeTest()
    # fprocess()
