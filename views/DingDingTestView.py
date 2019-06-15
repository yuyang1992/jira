from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QDateTimeEdit)

from config.jiraCfg import dingdingTest
from dp.jiraDP import JiraDP


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
        timingBtn.clicked.connect(lambda: self.onTiming())
        parentGroup.addWidget(loginBtn, 1, 0)
        parentGroup.addWidget(timingBtn, 1, 1)
        contentGroup.addLayout(parentGroup)
        self.setLayout(contentGroup)

    def show(self):
        JiraDP().searchCustomerNeed(dingdingTest)
        JiraDP().searchDayBug(dingdingTest)

    def onTiming(self):
        JiraDP().setSchedulerTask(17, 30, self.show)
        # SchedulerThread().start()
