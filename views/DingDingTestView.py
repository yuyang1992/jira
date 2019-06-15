from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QGridLayout, QLineEdit, \
    QPushButton

from dp.jiraDP import JiraDP
from config.jiraCfg import host, userQuestionCount, onlineDingDing, dayBugDingDing, dayBugCount, dingdingTest, memberWorkTimes

class DingDingTestView(QWidget):
    navigation = ''

    def __init__(self, navigation):
        super().__init__()
        self.navigation = navigation
        self.initView()

    def initView(self):
        contentGroup = QVBoxLayout()
        contentGroup.addStretch(1)
        parentGroup = QGridLayout()
        contentGroup.addLayout(parentGroup, 1)
        contentGroup.addStretch(1)
        loginBtn = QPushButton('发送', self)
        loginBtn.clicked.connect(lambda: self.show())
        parentGroup.addWidget(loginBtn, 2, 0, 1, 2, Qt.AlignTop | Qt.AlignCenter)
        contentGroup.addLayout(parentGroup)
        self.setLayout(contentGroup)

    def show(self):
            JiraDP().searchCustomerNeed(dingdingTest)
            JiraDP().searchDayBug(dingdingTest)


