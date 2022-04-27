import easygui as gui
from easygui.boxes.choice_box import ChoiceBox
from games import kg, pcr, other


# 好像没有办法做到修改父类所在的文件的方法这种事情。
class alter(ChoiceBox):

    def stop(self):
        global flag
        flag = False
        self.ui.stop()
# 2022年4月23日01:02:30 增加全打地下城按钮 dailyMission(1)。
choices = ("明日方舟",
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
           "=坎公===================",
           "开游戏每日",
           "卡马逊半自动",
            "卡马逊全自动",
           "PVP",
           "买金币和锤子",
           "坎公日常一",
           "坎公日常二",
           "坎公日常三",
           "=杂项===================",
           "QQ",
           "=关闭===================",
           "关闭")

def main():
    return gui.choicebox("脚本选择", "瞎写的随便", choices=choices)


def test(name):
    gui.msgbox(name)

if __name__ == "__main__":
    flag = True
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
            pcr.fullAuto(pcr.saveXY(1))
        elif choice == "任务礼物":
            pcr.missionAndGift()
        elif choice == "日常全地下城":
            pcr.dailyMission(1)

