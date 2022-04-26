import daoImpl


# 坎公用 1 点一次 2 点两次  3 隔点时间点两次，有偏移量
def searchPhotoKg(name, mode, c, d):
    return daoImpl.searchPhotoKg(name, mode, c, d)


# pcr用 1 点一次 2 点两次 3 点一次，有偏移量 4 隔点时间点两次，有偏移量
def searchPhotoPcr(name, mode, c, d):
    return daoImpl.searchPhotoPcr(name, mode, c, d)


# pcr用，只找一次，1 点一次 2 点两次 3 隔点时间点两次，固定了偏移量。
def searchPhotoOncePcr(name, mode):
    return daoImpl.searchPhotoOncePcr(name, mode)


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
