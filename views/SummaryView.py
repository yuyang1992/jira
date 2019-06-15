from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, \
    QComboBox, QDateTimeEdit

from dp.jiraDP import JiraDP


class SummaryView(QWidget):
    navigation = ''

    def __init__(self, navigation):
        super().__init__()
        self.navigation = navigation
        self.initView()

    def initView(self):
        contentGroup = QVBoxLayout()
        parentGroup = QGridLayout()
        contentGroup.addLayout(parentGroup, 1)
        contentGroup.addStretch(1)

        # 小组类别
        groupLable = QLabel("小组")
        groupComBox = QComboBox()
        groupComBox.addItems(["房客", "交易", "公共组", "移动端"])
        parentGroup.addWidget(groupLable, 0, 0)
        parentGroup.addWidget(groupComBox, 0, 1)
        # userNameEdit.textChanged.connect(self.changeName)

        # 时间
        startEimeLable = QLabel("开始时间")
        startTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        startTimeEdit.setDisplayFormat('yyyy-MM-dd')
        startTimeEdit.setCalendarPopup(True)

        endTimeLable = QLabel("结束时间")
        endTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        endTimeEdit.setDisplayFormat('yyyy-MM-dd')
        endTimeEdit.setCalendarPopup(True)

        parentGroup.addWidget(startEimeLable, 1, 0)
        parentGroup.addWidget(startTimeEdit, 1, 1)
        parentGroup.addWidget(endTimeLable, 2, 0)
        parentGroup.addWidget(endTimeEdit, 2, 1)

        # 迭代版本
        spirntLable = QLabel("迭代")
        spirntEdit = QLineEdit()
        parentGroup.addWidget(spirntLable, 3, 0)
        parentGroup.addWidget(spirntEdit, 3, 1)

        # userPWEdit.textChanged.connect(self.changePW)

        loginBtn = QPushButton('导出', self)
        loginBtn.clicked.connect(lambda: self.exportExcel())
        parentGroup.addWidget(loginBtn, 4, 0, 1, 2, Qt.AlignTop | Qt.AlignCenter)
        self.setLayout(contentGroup)

    def exportExcel(self):
        print(JiraDP().exportSummrayExcel("sprint总结"))
