import time


class kgPhoto:
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0

    def writeSelf(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def justPrint(self, name):
        print(self.name)

    def addPrint(self, x):
        if x == 1:
            self.x = 1
        elif x == 2:
            self.x = 2
        elif x == 3:
            self.writeSelf("图片3", 3, 3)
    # ?
    def names(self):
        names = []
        names.append(self)

    # 传三张照片进来，找到哪张就返回哪张照片的名字。
    # 有尼玛卵用啊透，回传坐标才有用。
    def enterTest(self, photoOne, photoTwo, photoThree):
        print(self.name)

    def __str__(self):
        return print(self.name,self.x,self.y)

def selfAdd(kg1):
    kg1.x = 10

def selfTest(i):
    print(i)

    # 嵌套循环测试
def loopTest():
    kg = kgPhoto
    photoMap = ["图片1", "图片2"]
    photoMap.append(("图片3","图片3.5"))
    photoMap2 = [photoMap, "图片4"]
    photoMaps = [photoMap, photoMap2]
    # 嵌套循环。
    print(photoMap[2][0],photoMap[2][1])
    for i in photoMaps:
        print(i)
        for i in i:
            print(i)

def mathTest():
    # 方法外改数组内的值，会不会同步变更的实验。
    photoMap = ["图片1", "图片2"]
    print(photoMap)
    for i in photoMap:
        kg1 = kgPhoto(i)
        kg1.__str__()
        kg1.y = 4
        kg1.addPrint(3)
        selfAdd(kg1)
        kg1.__str__()
# 字典测试
def dictTest():
    photoMapsTest = []
    photoMapsTest.append(dict(zip(['one', 'two', 'three'], [1, 2, 3])))
    photoMapsTest.append(dict(zip(['one', 'two', 'three'], [4, 5, 6])))
    for i in photoMapsTest :
        selfTest(i.get('one'))

    # print("图片3" == kg1.name)
    # print("图片3".__eq__(kg1.name))
# 下标测试
def downNumber():
    kgMaps = []
    kgMessages = []
    kg = kgPhoto("测试1")
    kgMessages.append(("1",1,1))
    kgMessages.append(("2", 2, 2))
    for i in kgMessages:
        t1 = time.clock()
        time.sleep(1)
        print(t1)
        kg.writeSelf(i[0],i[1],i[2])
        t2 = time.clock()
        print(t2 - t1)
    #kgMaps.append(kg)
    kg.__str__()

def addTest():
    onlyOneMap = [
        "star\\jjc刷新",  # 0
    ]
    onlyOneMap.append("star\\jjc战斗开始")
    onlyOneMap.append("star\\jjc碎钻确认")
    print(onlyOneMap)

def removeTest():
    test1 = [
        "图片1",
        "图片2",
    ]
    test1.remove("图片2")
    print(test1)

if __name__ == "__main__":
    removeTest()




