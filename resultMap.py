class resultMap:
    def __init__(self):
        self.resultCode = 0  # 0失败 1成功
        self.resultMessage = "有错误"

    def writeResult(self,resultCode,resultMessage):
        self.resultCode = resultCode
        self.resultMessage = resultMessage



