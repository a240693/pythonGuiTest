import time

from dao import dao, multiphotos
from dao import changeVar as cv

cv._init()
cv.set_value("path",cv.path)
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

#2022年7月16日11:37:36 逻辑重构。
def RDdaily():
    flag = True
    photoMap = multiphotos.Photo()
    photoMaps = [
        '粥点击收获',
        '粥每日线索',
        "粥停工",
        '粥会客室改',
        '粥基建总览',
        '粥基建',
    ]
    moveMaps = [
        (775, 0),  # 会客室（线索 0
        (47, 360),  # 左下角收取 1
        (2, -80),  # 粥会客室 2
        (-139, 361),  # 每日线索获取 3
        (-706, -44),  # 每日线索后退 4
        (809, -89),  # 粥休息室待办 5
        (8, 39),  # 停工复位
    ]
    while flag:
        photoMap.loopSearch(photoMaps)
        name = photoMap.name
        x = photoMap.x
        y = photoMap.y
        if "粥基建总览".__eq__(name):
            dao.moveToMRFZ(x + moveMaps[5][0], y + moveMaps[5][1], 1)
            continue

        if "粥会客室改".__eq__(name):
            dao.moveTo(x, y)
            meetingRoom()
            break

        if "停工" in name :
            dao.moveToMRFZ(x + moveMaps[6][0], y + moveMaps[6][1], 1)
            continue

        dao.moveTo(x,y)


# 2022年5月11日11:48:44
# 2022年7月16日11:15:36，逻辑重构。
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
    while True:
        photoMap = photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        dao.moveTo(x, y)
        if "领取" in name:
            buyTrust()
            break
        elif "收取" in name:
            dao.tapSpace(2)


# 2022年5月11日12:11:04
# 2022年7月16日11:15:46 逻辑重构
def buyTrust():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "粥信用不足",
        "粥招聘许可",
        "粥招聘许可",
        "粥75",
        "粥50",
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
        elif "不足" in name:
            photoMaps.remove("粥招聘许可")
            photoMaps.remove("粥50")
            photoMaps.remove("粥75")
            photoMaps.remove("粥购买物品")



# 2022年5月11日13:51:02
# 2022年7月16日11:15:54 逻辑重构
# 每日招聘。
def employDaily():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "粥招聘",
        "粥跳过",
        "粥公开招募",
    ]
    # onlyOneMaps = [
    #     "粥公开招募",
    # ]
    moveMaps = [
        (-717, -348),  # 左上角退出 0
    ]
    while True:
        photoMap = photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        dao.moveToMRFZ(x, y, 1)
        if "粥跳过" in name:
            dao.tapSpace(5)
        if "后退" in name:
            break
        if "粥招聘" in name:
            photoMaps.append("粥休息室后退")


# 2022年5月11日12:52:12
def allDaily():
    trustDaily()
    employDaily()
    RDdaily()
    dealRoom()

# 2022年7月16日11:55:48
# 会客室收取与退出。
def meetingRoom():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "粥线索已领取",
        "粥新线索",
        "粥线索领取",
        "粥线索交流结束",
        "粥线索详情",
        "粥每日线索",
    ]
    photoMapsNext = [
        "粥基建总览",
        "粥基建",
        "粥休息室后退",
    ]
    moveMaps = [
        (-58, -56),  # 左上角退出 0
    ]
    while True:
        photoMap = photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        if "线索交流" in name:
            dao.moveToMRFZ(x + moveMaps[0][0], y + moveMaps[0][1], 1)
            photoMaps.remove("粥线索交流结束")
        elif "已领取" in name:
            # 结束标识，删掉多余不用的同页面元素。
            photoMaps = photoMapsNext
            print(photoMaps)
        elif "总览" in name:
            break
        elif "粥基建".__eq__(name):
            dao.moveToMRFZ(x,y,1)
            break
        else:
            dao.moveToMRFZ(x,y,1)

# 交易站耗费无人机
def dealRoom():
    photoMap = multiphotos.Photo()
    photoMaps = [
        "粥订单完成",
        "粥贸易站结束标识",
        "粥贸易标识一",
        "粥无人机最多",
        "粥无人机协助",
        "粥贸易站",
        "粥线索详情",
        "粥贸易站确定",
    ]
    moveMaps = [
        (-58, -56),  # 左上角退出 0
    ]
    count = 0
    while 1:
        photoMap = photoMap.loopSearch(photoMaps)
        x = photoMap.x
        y = photoMap.y
        name = photoMap.name
        if "贸易标识" in name :
            photoMaps.remove("粥无人机最多")
            photoMaps.insert(0,"粥贸易站确定")
        elif "协助" in name:
            photoMaps.remove("粥贸易站确定")
            photoMaps.insert(2,"粥无人机最多")
            count = 0
        elif "最多" in name:
            count += 1
        elif "结束" in name:
            break

        dao.moveToMRFZ(x,y,1)

        if count >= 3 :
            photoMaps.remove("粥无人机最多")
            photoMaps.insert(0,"粥贸易站确定")
            count = 0




if __name__ == "__main__":
    # allDaily()
    # RDdaily()
    # employDaily()
    RDdaily()
    dealRoom()
    # restPeople()