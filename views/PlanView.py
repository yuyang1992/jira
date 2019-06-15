from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, \
    QPushButton

from dp.jiraDP import JiraDP


class PlanView(QWidget):
    navigation = ''
    jql = None
    subTaskJql = None

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
        userNameLable = QLabel("用户故事JQL查询语句")
        userNameEdit = QLineEdit()
        userNameEdit.textChanged.connect(self.changeJql)
        parentGroup.addWidget(userNameLable, 0, 0)
        parentGroup.addWidget(userNameEdit, 0, 1)

        subTaskLable = QLabel("子任务JQL查询语句")
        subTaskEdit = QLineEdit()
        subTaskEdit.textChanged.connect(self.changeSubTaskJql)

        parentGroup.addWidget(subTaskLable, 1, 0)
        parentGroup.addWidget(subTaskEdit, 1, 1)
        loginBtn = QPushButton('导出', self)
        loginBtn.clicked.connect(lambda: self.show())
        parentGroup.addWidget(loginBtn, 2, 0, 1, 2, Qt.AlignTop | Qt.AlignCenter)
        contentGroup.addLayout(parentGroup)
        self.setLayout(contentGroup)

    def show(self):
        JiraDP().spirntPlan(storyJql=self.jql, subTaskJql=self.subTaskJql)

    def changeJql(self, text):
        self.jql = text

    def changeSubTaskJql(self, text):
        self.subTaskJql = text
