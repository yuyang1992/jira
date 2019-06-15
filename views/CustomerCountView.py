from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QPushButton

from dp.jiraDP import JiraDP


class CustomerCountView(QWidget):
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
        userNameLable = QLabel("BugJQL查询语句")
        userNameEdit = QLineEdit()
        userNameEdit.textChanged.connect(self.changeJql)
        parentGroup.addWidget(userNameLable, 0, 0)
        parentGroup.addWidget(userNameEdit, 0, 1)

        loginBtn = QPushButton('导出', self)
        loginBtn.clicked.connect(lambda: self.show())
        parentGroup.addWidget(loginBtn, 2, 0, 1, 2, Qt.AlignTop | Qt.AlignCenter)
        contentGroup.addLayout(parentGroup)
        self.setLayout(contentGroup)

    def show(self):
        JiraDP().sprintBugCountInUser(jql=self.jql)

    def changeJql(self, text):
        self.jql = text
