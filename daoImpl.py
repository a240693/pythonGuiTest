import pyautogui
import time

# from . import test
path = 'F:\\pyTest\\'

def moveTo2(x, y):
    x1, y1 = pyautogui.position()
    pyautogui.moveTo(x, y)
    pyautogui.doubleClick(button="left")
    if x1 != x1 & y1 != y1:
        pyautogui.moveTo(x1, y1)
        time.sleep(1)
        # pyautogui.click(button="left")


def moveTo(x, y):
    x1, y1 = pyautogui.position()
    pyautogui.moveTo(x, y)
    pyautogui.click(button="left")
    if x1 != x1 & y1 != y1:
        pyautogui.moveTo(x1, y1)
        time.sleep(1)
        # pyautogui.click(button="left")


def moveToFive(x, y):
    x1, y1 = pyautogui.position()
    pyautogui.moveTo(x, y)
    count = 0
    while count < 5:
        pyautogui.click(button="left")
        count = count + 1
        time.sleep(0.2)
    if x1 != x1 & y1 != y1:
        pyautogui.moveTo(x1, y1)
        # time.sleep(1)
        # pyautogui.click(button="left")


def moveToNotRemember(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(button="left")


# 同一个位置隔一秒点击一次。
def moveToPcr(x, y, times):
    x1, y1 = pyautogui.position()
    pyautogui.moveTo(x, y)
    count = 0
    while count < times:
        pyautogui.click(button="left")
        count = count + 1
        if times > 10 :
            time.sleep(0.5)
        else:
            time.sleep(1)
    if x1 != x1 & y1 != y1:
        pyautogui.moveTo(x1, y1)
        time.sleep(1)
        # pyautogui.click(button="left")


def moveToKgAuto(x, y, times):
    # time.sleep(1)
    x1, y1 = pyautogui.position()
    pyautogui.moveTo(x, y)
    count = 0
    while count < times:
        pyautogui.click(button="left")
        count = count + 1
        time.sleep(0.1)
    if x1 != x1 & y1 != y1:
        pyautogui.moveTo(x1, y1)
        # pyautogui.click(button="left")


def searchPhoto(name, mode):
    count = 0
    found = False
    while not found:
        try:
            x, y, w, h = pyautogui.locateOnScreen(path + name + '.png', grayscale=True)
            x, y = pyautogui.center((x, y, w, h))
            print("{}.png在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(name, x, y, w, h))
            if mode == 1:
                moveTo(x, y)
            elif mode == 5:
                moveToNotRemember(x, y)
            else:
                moveTo2(x, y)
            found = True
        except:
            count = count + 1
            print('{}.png没找到，第{}次,3秒后重试'.format(name, count))
            time.sleep(3)


def enterGame():
    found = False
    while not found:
        try:
            x, y, w, h = pyautogui.locateOnScreen(path + '开始.png')
            found = True
        except:
            pyautogui.click(button="left")
            time.sleep(5)


def enterGamePcr(name,x1,y1):
    found = False
    while not found:
        try:
            x, y = pyautogui.locateCenterOnScreen(path + name +'.png')
            moveTo(x + x1, y + y1)
            found = True
        except:
            pyautogui.click(button="left")
            time.sleep(5)


def searchPhotoOpen(name):
    count = 0
    found = False
    while not found:
        try:
            x, y, w, h = pyautogui.locateOnScreen(path + name + '.png')
            x, y = pyautogui.center((x, y, w, h))
            print("该图标在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(x, y, w, h))
            moveTo(x + 318, y)
            found = True
        except:
            count = count + 1
            print('{}.png没找到，第{}次,3秒后重试'.format(name, count))
            time.sleep(3)


def searchPhotoOnce(name, mode):
    try:
        x, y, w, h = pyautogui.locateOnScreen(path + name + '.png', grayscale=True)
        x, y = pyautogui.center((x, y, w, h))
        # print("{}.png在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(name,x, y, w, h))
        if mode == 1:
            moveTo(x, y)
        elif mode == 3:
            moveToPcr(x, y, 3)
        elif mode == 4:
            moveToKgAuto(x, y, 3)
        else:
            moveTo2(x, y)
        return 1
    except:
        return 0

# 只找counts次，不管结果。
def searchPhotoCountsPcr(name, mode,x1,y1,counts):
    try:
        i = 0
        while i < counts :
            i += 1
            x, y, w, h = pyautogui.locateOnScreen(path + name + '.png', grayscale=True)
            x, y = pyautogui.center((x, y, w, h))
            break
        # print("{}.png在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(name,x, y, w, h))
        if mode == 1:
            moveTo(x + x1, y + y1)
        elif mode == 3:
            moveToPcr(x + x1, y + y1, 3)
        elif mode == 5:
            moveTo(x + x1, y + y1)
        else:
            moveTo2(x, y)
        return 1
    except:
        return 0


# 1 点一次 2 点两次 3 点一次，有偏移量 4 隔点时间点两次，有偏移量
def searchPhotoPcr(name, mode, c, d):
    count = 0
    found = False
    while not found:
        try:
            x, y, w, h = pyautogui.locateOnScreen(path + name + '.png', grayscale=True)
            x, y = pyautogui.center((x, y, w, h))
            print("{}.png在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(name, x, y, w, h))
            if mode == 1:
                moveTo(x, y)
            elif mode == 3:
                moveTo(x + c, y + d)
            elif mode == 4:
                moveToPcr(x + c, y + d, 3)
            elif mode == 5:
                moveToFive(x + c, y + d)
            else:
                moveTo2(x, y)
            found = True
            return x, y
        except:
            count = count + 1
            print('{}.png没找到，第{}次,3秒后重试'.format(name, count))
            time.sleep(3)


def onlySearchPcr(name):
    count = 0
    found = False
    while not found:
        try:
            x, y, w, h = pyautogui.locateOnScreen(path + name + '.png', grayscale=True)
            x, y = pyautogui.center((x, y, w, h))
            print("{}.png在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(name, x, y, w, h))
            found = True
            return x, y
        except:
            count = count + 1
            print('{}.png没找到，第{}次,3秒后重试'.format(name, count))
            time.sleep(3)




def setFlag():
    count = 10
    while count != 0:
        count -= 1
        print("还剩下{}秒".format(count))
        time.sleep(1)
    global flag
    flag = False


# 1 点一次 2 点两次  3 隔点时间点两次，有偏移量
def searchPhotoKg(name, mode, c, d):
    count = 0
    found = False
    while not found:
        try:
            x, y, w, h = pyautogui.locateOnScreen(path + name + '.png', grayscale=True)
            x, y = pyautogui.center((x, y, w, h))
            print("{}.png在屏幕中的位置是：X={},Y={}，宽{}像素,高{}像素".format(name, x, y, w, h))
            if mode == 1:
                moveTo(x + c, y + d)
            elif mode == 3:
                moveToPcr(x + c, y + d, 2)
            else:
                moveTo2(x + c, y + d)
            found = True
            return x, y
        except:
            count = count + 1
            print('{}.png没找到，第{}次,3秒后重试'.format(name, count))
            time.sleep(3)

def dualListPhotoKg(photoMap):
    t1 = time.localtime()
    for photo in photoMap:
        searchPhotoKg(photo[0],photo[1],photo[2],photo[3])
        if "进化石扫荡".__eq__(photo[0]) & 0 == photo[3]:
            time.sleep(5)
    return 1

def dualListPhotoPcr(photoMap):
    for photo in photoMap:
        # 自动点击页面直到再次找到主页。
        # v1.2 点尼玛直接loopSearch ↑ 一开始的思路真的是！@#！@#！@#才写出来的。
        # 5 的话 ，默认传一组图片名字进来，直接调用loopSearch，找到就走。
        # 但剩余一个问题： 如果有的图片是一次性的，只会在第一次进入展示。
        # 判断页面的方法看起来还是有必要的，判断后再决定走什么方法（？）
        if 5 == photo[1] :
            while True:
                result = searchPhotoCountsPcr(photo[0],photo[1],photo[2],photo[3],1)
                if 1 == result :
                    break
                else:
                    # 缺个坐标应该放在哪儿的思路，个人现在是恒定放在左边，算是个手操要素，但老实说，不太稳。
                    pyautogui.click(button="left")
        else:
            searchPhotoPcr(photo[0],photo[1],photo[2],photo[3])
        if "主页".__eq__(photo[0]) & 0 == photo[3]:
            time.sleep(1)
        elif "冒险".__eq__(photo[0]) & 0 == photo[3]:
            time.sleep(1)
        elif "战斗开始推图".__eq__(photo[0]) & 62 == photo[3]:
            time.sleep(15)
    return 1
# 开QQ
# moveTo(121, 255);

# 开雷电多开器
# searchPhoto('1',2)
# searchPhotoOpen('明日方舟')
# 开坎公
# searchPhoto('kg',1)
# time.sleep(10)
# enterGame()
# searchPhoto('kgx',1)
# searchPhoto('领取奖励.png',1)
# searchPhoto('确认.png',1)
# 开操作录制
# searchPhoto('button.png',1)
# 按操作录制X
# searchPhoto('x.png',1)

# 开脚本第三个
# searchPhoto('kg3.png',1)
# pcr测试