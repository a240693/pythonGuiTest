import _thread
import time
import  datetime
import platform

# 为线程定义一个函数
flag = True


def print_time(threadName, delay):
    count = 0
    while flag:
        time.sleep(delay)
        count += 1
        print("%s: %s,%d" % (threadName, time.ctime(time.time()),0+flag))


def setFlag():
    count = 10
    while count != 0:
        count -= 1
        print("还剩下{}秒".format(count))
        time.sleep(1)
    global flag
    flag = False


if __name__ == "__main__":
    # 创建两个线程
    try:
        _thread.start_new_thread(print_time, ("Thread-1", 2,))
        _thread.start_new_thread(setFlag,())
    except:
        print("Error: 无法启动线程")

    while 1:
        pass
