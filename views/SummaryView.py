from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QPushButton

from dp.jiraDP import JiraDP


class SummaryView(QWidget):
    navigation = ''
    reopenJql = ''
    storyJql = ''
    bugJql = ''

    def __init__(self, navigation):
        super().__init__()
        self.navigation = navigation
        self.initView()

    def initView(self):
        contentGroup = QVBoxLayout()
        parentGroup = QGridLayout()
        contentGroup.addLayout(parentGroup, 1)
        contentGroup.addStretch(1)

        # # 小组类别
        # groupLable = QLabel("小组")
        # groupComBox = QComboBox()
        # groupComBox.addItems(["房客", "交易", "公共组", "移动端"])
        # parentGroup.addWidget(groupLable, 0, 0)
        # parentGroup.addWidget(groupComBox, 0, 1)
        # # userNameEdit.textChanged.connect(self.changeName)
        #
        # # 时间
        # startEimeLable = QLabel("开始时间")
        # startTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        # startTimeEdit.setDisplayFormat('yyyy-MM-dd')
        # startTimeEdit.setCalendarPopup(True)
        #
        # endTimeLable = QLabel("结束时间")
        # endTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        # endTimeEdit.setDisplayFormat('yyyy-MM-dd')
        # endTimeEdit.setCalendarPopup(True)
        #
        # parentGroup.addWidget(startEimeLable, 1, 0)
        # parentGroup.addWidget(startTimeEdit, 1, 1)
        # parentGroup.addWidget(endTimeLable, 2, 0)
        # parentGroup.addWidget(endTimeEdit, 2, 1)

        # 用户故事查询语句
        stroyLable = QLabel("用户故事查询语句")
        stroyEdit = QLineEdit()
        parentGroup.addWidget(stroyLable, 1, 0)
        parentGroup.addWidget(stroyEdit, 1, 1)
        stroyEdit.textChanged.connect(self.changeStoryJql)

        # reopen查询语句
        reopenLable = QLabel("重开Bug查询语句")
        reopenEdit = QLineEdit()
        parentGroup.addWidget(reopenLable, 2, 0)
        parentGroup.addWidget(reopenEdit, 2, 1)
        reopenEdit.textChanged.connect(self.changeReopenJql)

        # Bug查询语句
        spirntLable = QLabel("Bug查询语句")
        spirntEdit = QLineEdit()
        parentGroup.addWidget(spirntLable, 3, 0)
        parentGroup.addWidget(spirntEdit, 3, 1)

        spirntEdit.textChanged.connect(self.changeBugJql)

        loginBtn = QPushButton('导出', self)
        loginBtn.clicked.connect(lambda: self.exportExcel())
        parentGroup.addWidget(loginBtn, 4, 0, 1, 2, Qt.AlignTop | Qt.AlignCenter)
        self.setLayout(contentGroup)

    def changeReopenJql(self, text):
        self.reopenJql = text

    def changeStoryJql(self, text):
        self.storyJql = text

    def changeBugJql(self, text):
        self.bugJql = text

    def exportExcel(self):
        #   reopenJql = "project = SAAS2 AND issuetype in (Bug, 故障) AND (assignee in membersOf(移动端) OR labels in (移动端, iOS, IOS, Android)) AND status in (open, Reopened, 'In Progress')"
        #   storyJql = "project = SAAS2 AND issuetype in (任务, 用户故事) AND Sprint = 232 AND assignee in (zhen.xu, huainan.qu, haitao.cao, li.zhang, nan.xia, jingyan.wan)"
        #   bugJql = "project = SAAS2 AND issuetype in (Bug, 故障) AND (assignee in membersOf(移动端) OR labels in (移动端, iOS, IOS, Android)) AND status in (open, Reopened, 'In Progress') "
        JiraDP().sprintSummary(self.storyJql)
        JiraDP().exportSummrayExcel(storyJql=self.storyJql, reopendJql=self.reopenJql,
                                    bugJql=self.bugJql)
