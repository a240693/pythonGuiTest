import sys

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
    print(x, y)
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


a = [0]
def stdinTest():
    for line in sys.stdin:
        a = line.split(" ")
        a[a.__len__()-1] = a[a.__len__()-1].split("\n")[0];
        break
    # print(a)
    try:
        for i in range(a.__len__()):
            if (0 <= int(a[i])) or (9 >= int(a[i])):
                # print(int(a[i]))
                continue
    except:
        return []
    dual(a)


# 贪心算法先走一次试试？反正先把周围两个的大小比出来换位置再说。
def selectMax(i,a):
    if i > 0:
        if a[i] < a[i - 1]:
            exchange(i, i - 1,a)
    if i < a.__len__() - 1:
        if a[i] < a[i + 1]:
            exchange(i, i + 1,a)


def selectMin(i,a):
    if a[i] > a[i - 1]:
        exchange(i, i - 1,a)

    if i < a.__len__() - 1:
        if a[i] > a[i + 1]:
            exchange(i, i + 1,a)


def exchange(i, i2,a):
    temp = a[i]
    a[i] = a[i2]
    a[i2] = temp
    # print(a)


def dual(a):
    word = ""
    for i in range(a.__len__()):
        if i % 2 == 0:
            selectMax(i,a)
        if i % 2 == 1:
            selectMin(i,a)
    for i in range(a.__len__()):
        word += a[i]+" "
    print(word)


if __name__ == '__main__':
    # scrollTest()
    # keyTest()
    stdinTest()
    # fprocess()
    # exchange(0, 1)
    # dual()
