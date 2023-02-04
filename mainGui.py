import easygui as gui
from easygui.boxes.choice_box import ChoiceBox
from games import kg, pcr, other, mrfz


# 好像没有办法做到修改父类所在的文件的方法这种事情。
class alter(ChoiceBox):

    def stop(self):
        global flag
        flag = False
        self.ui.stop()


# 2022年4月23日01:02:30 增加全打地下城按钮 dailyMission(1)。
# 2022年5月12日11:18:47 新增方舟游戏功能测试。
choices = ("=明日方舟==============",
           "半自动换人休息",
           "公开招募与信用点",
           "基建页收取",
           "每日",
           "=pcr===================",
           "地下城Ex2",
           "地下城Ex3",
           "推图半自动",
           "240693",
           "183",
           "任务礼物",
           "日常",
           "日常全地下城",
           "小号日常",
           "全自动推图",
           "活动信赖",
           "自动剧情",
           "自动活动扭蛋",
           "每日串联",
           "=坎公===================",
           "开游戏每日",
           "卡马逊半自动",
           "卡马逊全自动",
           "PVP",
           "买金币和锤子",
           "坎公日常一",
           "坎公日常二",
           "坎公日常三",
           "半自动强化",
           "半自动强化改",
           "自动收取活动",
           "=杂项===================",
           "QQ",
           "=关闭===================",
           "关闭")


def main():
    return gui.choicebox("脚本选择", "瞎写的随便", choices=choices)


def test(name):
    gui.msgbox(name)


def inputBox():
    return gui.integerbox(msg='请输入章节下标', title='下标：', default=None, lowerbound=0, upperbound=9999, image=None,
                          root=None)

def printChoice():
    print(choices)

if __name__ == "__main__":
    flag = True
    # printChoice()
    while flag == True:
        choice = ''
        choice = main()
        if choice == "明日方舟":
            test(choice)
        elif choice == "开游戏每日":
            kg.open()
        elif choice == "卡马逊半自动":
            kg.kmxAuto()
        elif choice == "推图半自动":
            pcr.autoMapEnter()
        elif choice == "QQ":
            other.QQ()
        elif choice == "PVP":
            kg.pvp()
        elif choice == "买金币和锤子":
            kg.dailyBuy()
        elif choice == "地下城Ex2":
            pcr.pcrUnderEX2()
        elif choice == "240693":
            pcr.open(1)
        elif choice == "183":
            pcr.open(0)
        elif choice == "卡马逊全自动":
            kg.fullAutoKmx()
        elif choice == "关闭":
            break
        elif choice == "日常":
            pcr.dailyMission(0)
        elif choice == "小号日常":
            pcr.dailyMissionSmall()
        elif choice == "坎公日常一":
            kg.day2buy(1)
        elif choice == "坎公日常二":
            kg.day2buy(2)
        elif choice == "坎公日常三":
            kg.day2buy(3)
        elif choice == "地下城Ex3":
            pcr.underWorld(0)
        elif choice == "全自动推图":
            index = inputBox()
            pcr.fullAuto(pcr.saveXY(index))
        elif choice == "任务礼物":
            pcr.missionAndGift()
        elif choice == "日常全地下城":
            pcr.dailyMission(1)
        # 方舟。
        elif choice == "半自动换人休息":
            mrfz.restPeople()
        elif choice == "公开招募与信用点":
            mrfz.allDaily()
        elif choice == "基建页收取":
            mrfz.RDdaily()
        # 2022年5月14日18:39:17 新增 pcr “活动信赖” 和 “自动剧情”
        elif choice == "活动信赖":
            pcr.autoTrust()
        elif choice == "自动剧情":
            pcr.autoText()
        # 2022年5月25日19:03:04 新增自动活动扭蛋。
        elif choice == "自动活动扭蛋":
            pcr.autoEventEgg()
        # 2022年5月27日02:42:13 半自动强化
        elif choice == "半自动强化":
            kg.kgSwitch(kg.halfAutoStr)
        # 2022年6月15日12:22:56 自动检测装备图鉴是否完成。
        elif choice == "半自动强化改":
            kg.kgSwitch(kg.autoCheckDevice())
        # 2022年6月23日17:30:29 自动收取活动
        elif choice == "自动收取活动":
            kg.kgSwitch(kg.autoEventGet())
        # 2022年7月18日11:40:03 方舟每日。
        elif choice == "每日":
            mrfz.allDaily()
        elif choice == "每日串联":
            pcr.changePlayerOpen()




