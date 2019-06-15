from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, \
    QPushButton

from dp.jiraDP import JiraDP


class PlanView(QWidget):
    navigation = ''
    jql = None

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
        userNameLable = QLabel("JQL查询语句")
        userNameEdit = QLineEdit()
        userNameEdit.textChanged.connect(self.changeJql)

        parentGroup.addWidget(userNameLable, 0, 0)
        parentGroup.addWidget(userNameEdit, 0, 1)
        loginBtn = QPushButton('确定', self)
        loginBtn.clicked.connect(lambda: self.show())
        parentGroup.addWidget(loginBtn, 2, 0, 1, 2, Qt.AlignTop | Qt.AlignCenter)
        contentGroup.addLayout(parentGroup)
        self.setLayout(contentGroup)

    def show(self):
        if self.jql is None:
            pass
        else:
            JiraDP().sprintSummary(self.jql)

    def changeJql(self, text):
        self.jql = text
