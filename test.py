import pyautogui;
import time;
import subprocess;
import _thread
import time
import platform
path = 'F:\\pyTest\\'
# 获取颜色
def getcolour(x,y):
    img = pyautogui.screenshot()
    img.save
    co = img.getpixel((x,y))
    return co;

# 计时器
def countDown(m,s):
    timeLeft = 60*m + s
    while(timeLeft > 0):
        print("还剩下：",timeLeft)
        time.sleep(1)
        timeLeft = timeLeft - 1

def fprocess():
    returnWord = subprocess.run(["D:","dir"],shell=True,check=True)
    print(returnWord)

def showDetail():
    r = platform.architecture()
    print(r)

if __name__ == '__main__':
    countDown(0,3)
    x1,y1 = pyautogui.position();
    name = '坎公进入商店'
    x, y, w, h = pyautogui.locateOnScreen(path + name + '.png')
    x, y = pyautogui.center((x, y, w, h))

    print("{}颜色为：{},该坐标为{}".format(name,(getcolour(x,y)),(x,y)));
    print("鼠标坐标为{}".format((x1,y1)));
    print("差值为 {}, {}".format((x1-x),(y1-y)));
    pyautogui.moveTo(x, y)
    #fprocess()