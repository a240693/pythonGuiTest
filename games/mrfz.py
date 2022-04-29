import time

from dao import dao, multiphotos


# 2022年4月26日11:54:49
def restPeople():
    photoMap = multiphotos.Photo()
    photoMaps = [
        #'注意力涣散',
        '粥休息室确认',
        '粥宿舍',
        '粥宿舍二次确认'
    ]
    peopleMaps = [  # 第1-5个人
        (-531, -346),
        (-532, -140),
        (-417, -335),
        (-406, -156),
        (-301, -340)
    ]
    moveMaps = [
        (450, -223),  # 宿舍内无影响的地方 0
        (25, -259),  # 进驻信息 1
        (870, -451),    # 清空宿舍 2
        (759, -351)   # 进入宿舍换人 3
    ]
    while True:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        if "粥休息室确认".__eq__(photoMap.name):
            for i in peopleMaps:
                dao.moveToMRFZ(x + i[0], y + i[1], 1)
            dao.moveToMRFZ(x, y, 1)
        elif "粥宿舍".__eq__(photoMap.name):
            for i in moveMaps:
                dao.moveToMRFZ(x + i[0], y + i[1], 1)
        elif "二次确认" in photoMap.name:
            dao.moveToMRFZ(x, y, 1)
            break


def RDdaily():
    flag = True
    photoMap = multiphotos.Photo()
    photoMaps = ['粥会客室', '粥每日线索', '粥基建总览']
    moveMaps = [
        (775, 0),  # 会客室（线索 0
        (47, 360),  # 左下角收取 1
        (2, -80),  # 粥会客室 2
        (-139, 361),  # 每日线索获取 3
        (-706, -44),  # 每日线索后退 4
        (809, -89)  # 粥休息室待办 5
    ]
    while flag:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        if "粥基建总览".__eq__(photoMap.name):
            dao.moveToMRFZ(x + moveMaps[5][0], y + moveMaps[5][1], 1)
            dao.moveToMRFZ(x + moveMaps[1][0], y + moveMaps[1][1], 5)
            time.sleep(1)
            dao.moveTo(x, y)
            dao.moveToMRFZ(x + moveMaps[0][0], y + moveMaps[0][1], 1)
            time.sleep(1)
            dao.moveToMRFZ(x + moveMaps[1][0], y + moveMaps[1][1], 1)
        elif "粥每日线索".__eq__(photoMap.name):
            dao.moveTo(x + moveMaps[3][0], y + moveMaps[3][1])
            dao.moveTo(x, y)
            dao.moveToMRFZ(x + moveMaps[4][0], y + moveMaps[4][1], 3)
            flag = False
        elif "粥会客室".__eq__(photoMap.name):
            # 还没做收取线索
            dao.moveTo(x + moveMaps[2][0], y + moveMaps[2][1])


if __name__ == "__main__":
    # RDdaily()
    restPeople()
