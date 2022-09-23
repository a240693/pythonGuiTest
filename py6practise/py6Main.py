import time
from threading import Thread

from PySide6.QtWidgets import QApplication,QMainWindow

from untitled import Ui_MainWindow
from template import  add

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow() # UI类的实例化
        self.ui.setupUi(self)
        self.bind()

    def bind(self):
        self.ui.pushButton.clicked.connect(self.handle_click)

    def handle_click(self):
        def innerFunction():
            a = self.ui.inputA.value()
            b = self.ui.inputB.value()

            time_cost = self.ui.timeCost.value()
            for index,n in enumerate(range(time_cost)):
                progress = index* 100 // time_cost
                self.ui.progressBar.setValue(progress)
                time.sleep(1)
            self.ui.progressBar.setValue(100)
            result = str(add(a,b))
            self.ui.result.setText(result)
        task = Thread(target=innerFunction)
        task.start()

if __name__ == "__main__":
    app = QApplication([]) # 启动一个应用
    window = MainWindow() # 实例化主窗口
    window.show() # 主窗口展示
    app.exec() # 等待