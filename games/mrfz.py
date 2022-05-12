import time

from dao import dao, multiphotos


# 2022年4月26日11:54:49
# 2022年5月11日13:57:09 修改成半自动，暂时没想法怎么整成全自动。
def restPeople():
    photoMap = multiphotos.Photo()
    photoMaps = [
        # '注意力涣散',
        '粥休息室确认',
        # '粥宿舍',
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
        (870, -451),  # 清空宿舍 2
        (759, -351)  # 进入宿舍换人 3
    ]
    while True:
        photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        if "粥休息室确认".__eq__(photoMap.name):
            for i in peopleMaps:
                dao.moveToMRFZ(x + i[0], y + i[1], 1)
            dao.moveToMRFZ(x, y, 1)
            time.sleep(10)
        elif "粥宿舍".__eq__(photoMap.name):
            for i in moveMaps:
                dao.moveToMRFZ(x + i[0], y + i[1], 1)
        elif "二次确认" in photoMap.name:
            dao.moveToMRFZ(x, y, 1)
            break


def RDdaily():
    flag = True
    photoMap = multiphotos.Photo()
    photoMaps = [
        '粥会客室',
        '粥每日线索',
        '粥基建总览',
    ]
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
            dao.moveToMRFZ(x + moveMaps[1][0], y + moveMaps[1][1], 6)
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


# 2022年5月11日11:48:44
# 每日收取信用点。
def trustDaily():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "粥采购中心",
        "粥信用交易所",
        "粥收取信用",
        "粥已领取",
    ]
    moveMaps = []
    for i in photoMaps:
        photoMap = photoMap.searchPhoto(i)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        dao.moveTo(x, y)
        if "领取" in name:
            buyTrust()
        elif "收取" in name:
            dao.tapSpace(2)


# 2022年5月11日12:11:04
def buyTrust():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "粥招聘许可",
        "粥招聘许可",
        "粥购买物品",
        "粥已领取",
    ]
    moveMaps = [
        (-630, 175),  # 购买第一个 0
        (-472, 188),  # 购买第二个 1
        (-227, 195),  # 购买第三个 2
        (-721, 1),  # 左上角退出 3
    ]
    while True:
        photoMap = photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        dao.moveTo(x, y)
        if "购买" in name:
            dao.tapSpace(2)
        elif "领取" in name:
            # 暂时不买
            dao.moveToMRFZ(x + moveMaps[3][0], y + moveMaps[3][1], 1)
            break


# 2022年5月11日13:51:02
# 每日招聘。
def employDaily():
    flag = True
    count = 0
    photoMap = multiphotos.Photo()
    photoMaps = [
        "粥招聘",
        "粥跳过",
    ]
    onlyOneMaps = [
        "粥公开招募",
    ]
    moveMaps = [
        (-717, -348),  # 左上角退出 0
    ]
    photoMap = photoMap.searchPhoto(onlyOneMaps[0])
    ex = photoMap.x
    ey = photoMap.y
    dao.moveTo(ex, ey)
    while (flag) & (count < 4):
        for i in photoMaps:
            photoMap = photoMap.searchPhoto(i)
            x = photoMap.x
            y = photoMap.y
            name = photoMap.name
            dao.moveToMRFZ(x, y, 1)
            if "粥跳过" in name:
                dao.tapSpace(5)
        count += 1
    dao.moveToMRFZ(ex + moveMaps[0][0], ey + moveMaps[0][1], 1)


# 2022年5月11日12:52:12
def allDaily():
    trustDaily()
    employDaily()


if __name__ == "__main__":
    # allDaily()
    # RDdaily()
    restPeople()
