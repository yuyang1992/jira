from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QDateTimeEdit

from config.jiraCfg import onlineDingDing, dayBugDingDing
from dp.jiraDP import JiraDP


class DingDingDayCountView(QWidget):
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
        # 时间
        startTimeLable = QLabel("任务执行时间")
        startTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        startTimeEdit.setDisplayFormat('hh:ss')
        startTimeEdit.setCalendarPopup(True)
        parentGroup.addWidget(startTimeLable, 0, 0)
        parentGroup.addWidget(startTimeEdit, 0, 1)

        loginBtn = QPushButton('立即发送', self)
        timingBtn = QPushButton('定时发送', self)
        loginBtn.clicked.connect(lambda: self.show())
        timingBtn.clicked.connect(lambda: self.show())
        parentGroup.addWidget(loginBtn, 1, 0)
        parentGroup.addWidget(timingBtn, 1, 1)
        contentGroup.addLayout(parentGroup)
        self.setLayout(contentGroup)

    def show(self):
        # JiraDP().searchCustomerNeed(onlineDingDing)
        # JiraDP().searchDayBug(dayBugDingDing)
        pass

    def onTiming(self):
        JiraDP().setSchedulerTask(hour=15, minute=57, job=self.show())
