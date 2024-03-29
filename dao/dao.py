from . import daoImpl


# 坎公用 1 点一次 2 点两次  3 隔点时间点两次，有偏移量
def searchPhotoKg(name, mode, c, d):
    return daoImpl.searchPhotoKg(name, mode, c, d)


# pcr用 1 点一次 2 点两次 3 点一次，有偏移量 4 隔点时间点两次，有偏移量
def searchPhotoPcr(name, mode, c, d):
    return daoImpl.searchPhotoPcr(name, mode, c, d)


# pcr用，只找一次，1 点一次 2 点两次 3 隔点时间点两次，固定了偏移量。
def searchPhotoOnce(name, mode):
    return daoImpl.searchPhotoOnce(name, mode)


# 1 点一次 2 点两次  3 隔点时间点两次，有偏移量，比较万用的坎公用的方法。
def searchPhotoKg(name, mode, c, d):
    return daoImpl.searchPhotoKg(name, mode, c, d)


# 传坐标进去批量处理,KG特化。
# 1 点一次 2 点两次  3 隔点时间点两次，有偏移量
def dualListPhotoKg(photoMap):
    return daoImpl.dualListPhotoKg(photoMap)


# 传坐标进去批量处理,pcr特化。
def dualListPhotoPcr(photoMap):
    return daoImpl.dualListPhotoPcr(photoMap)


# 专门给PCR用的点击，本身有偏移量，TIMES为重复点击次数
# 10次以上速度加快为0.3
def moveToPcr(x, y, times):
    return daoImpl.moveToPcr(x, y, times)


# 最原始的moveTo,只有单击，没有任何双击。
def moveTo(x, y):
    return daoImpl.moveTo(x, y)


# 坎公自动点击，times是重复点击次数，1的话就和moveTo一样
def moveToKgAuto(x, y, times):
    return daoImpl.moveToKgAuto(x, y, times)


# 明日方舟自动点击，times是重复点击次数，1的话就和moveTo一样
# 基底是坎公
def moveToMRFZ(x, y, times):
    return daoImpl.moveToMRFZ(x, y, times)

# opencv引入后，要把路径的中文进行转换用的东西。
def my_cv_imread(filepath):
    return daoImpl.my_cv_imread(filepath)

def scrollKg(x,y):
    return daoImpl.scrollKg(x,y)

# 2022年5月11日11:58:23
def tapSpace(times):
    return daoImpl.tapSpace(times)

# 2023年5月3日18:20:04
# 最原始的moveTo2,只有双击，没有任何单击。
def moveTo2(x, y):
    return daoImpl.moveTo2(x, y)

#2023年5月4日20:58:57
# 星铁用的，点击带按键。
def moveToWithKey(x, y,key):
    return daoImpl.moveToWithKey(x, y,key)

# 2023年5月5日16:53:11
# 星铁用的，单按键。
def pressKey(key):
    return daoImpl.pressKey(key)