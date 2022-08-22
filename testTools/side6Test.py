import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

import sys
import requests
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt)
from PySide6.QtWidgets import (QComboBox, QGroupBox, QLabel,
                               QMenuBar, QPushButton, QStatusBar, QTextEdit, QWidget)

class Ui_QtWeather(object):
    def setupUi(self, QtWeather):
        if not QtWeather.objectName():
            QtWeather.setObjectName(u"QtWeather")
        QtWeather.setWindowModality(Qt.ApplicationModal)
        QtWeather.resize(360, 398)
        self.centralwidget = QWidget(QtWeather)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 20, 321, 301))
        self.cityLabel = QLabel(self.groupBox)
        self.cityLabel.setObjectName(u"cityLabel")
        self.cityLabel.setGeometry(QRect(20, 30, 31, 16))
        self.selectBox = QComboBox(self.groupBox)
        self.selectBox.setObjectName(u"selectBox")
        self.selectBox.setGeometry(QRect(60, 30, 231, 22))
        self.selectBox.setEditable(True)
        self.textEdit = QTextEdit(self.groupBox)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(20, 70, 271, 211))
        self.clearBtn = QPushButton(self.centralwidget)
        self.clearBtn.setObjectName(u"clearBtn")
        self.clearBtn.setGeometry(QRect(30, 330, 75, 24))
        self.seachBtn = QPushButton(self.centralwidget)
        self.seachBtn.setObjectName(u"seachBtn")
        self.seachBtn.setGeometry(QRect(270, 330, 75, 24))
        QtWeather.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(QtWeather)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 360, 22))
        QtWeather.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(QtWeather)
        self.statusbar.setObjectName(u"statusbar")
        QtWeather.setStatusBar(self.statusbar)

        self.retranslateUi(QtWeather)

        self.seachBtn.clicked.connect(QtWeather.queryWeather)
        self.clearBtn.clicked.connect(QtWeather.clearText)

        QMetaObject.connectSlotsByName(QtWeather)

    # setupUi

    def retranslateUi(self, QtWeather):
        _translate = QCoreApplication.translate
        QtWeather.setWindowTitle(_translate("QtWeather", u"MainWindow", None))
        self.groupBox.setTitle(_translate("QtWeather", u"城市天气预报", None))
        self.cityLabel.setText(_translate("QtWeather", u"城市", None))
        self.clearBtn.setText(_translate("QtWeather", u"清空", None))
        self.seachBtn.setText(_translate("QtWeather", u"查询", None))

        self.selectBox.addItem("广州")
        self.selectBox.addItem("韶关")
        self.selectBox.addItem("深圳")
        self.selectBox.addItem("珠海")
        self.selectBox.addItem("汕头")
        self.selectBox.addItem("佛山")
        self.selectBox.addItem("江门")
        self.selectBox.addItem("湛江")
        self.selectBox.addItem("茂名")
        self.selectBox.addItem("肇庆")
        self.selectBox.addItem("惠州")
        self.selectBox.addItem("梅州")
        self.selectBox.addItem("汕尾")
        self.selectBox.addItem("河源")
        self.selectBox.addItem("阳江")
        self.selectBox.addItem("清远")
        self.selectBox.addItem("东莞")
        self.selectBox.addItem("中山")
        self.selectBox.addItem("潮州")
        self.selectBox.addItem("揭阳")
        self.selectBox.addItem("云浮")

        # 设置默认值
        self.selectBox.setCurrentIndex(3)
        self.selectBox.currentText()
    # retranslateUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QtWeather()
        self.ui.setupUi(self)
        self.cityDict = {
            "广州": "440100",
            "韶关": "440200",
            "深圳": "440300",
            "珠海": "440400",
            "汕头": "440500",
            "佛山": "440600",
            "江门": "440700",
            "湛江": "440800",
            "茂名": "440900",
            "肇庆": "441200",
            "惠州": "441300",
            "梅州": "441400",
            "汕尾": "441500",
            "河源": "441600",
            "阳江": "441700",
            "清远": "441800",
            "东莞": "441900",
            "中山": "442000",
            "潮州": "445100",
            "揭阳": "445200",
            "云浮": "445300"
        }

    def queryWeather(self):
        cityName = self.ui.selectBox.currentText()
        cityCode = self.getCode(cityName)

        r = requests.get(
            "https://restapi.amap.com/v3/weather/weatherInfo?key=f4fd5b287b6d7d51a3c60fee24e42002&city={}".format(cityCode))

        if r.status_code == 200:
            data = r.json()['lives'][0]
            weatherMsg = '城市：{}\n天气：{}\n温度：{}\n风向：{}\n风力：{}\n湿度：{}\n发布时间：{}\n'.format(
                data['city'],
                data['weather'],
                data['temperature'],
                data['winddirection'],
                data['windpower'],
                data['humidity'],
                data['reporttime'],
            )
        else:
            weatherMsg = '天气查询失败，请稍后再试！'
        self.ui.textEdit.setText(weatherMsg)

    def getCode(self, cityName):
        return self.cityDict.get(cityName, '广州')

    def clearText(self):
        self.ui.textEdit.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setGeometry(150, 150, 360, 398*2)
    window.setWindowTitle("QT 简单示例教程")
    window.show()

    sys.exit(app.exec())