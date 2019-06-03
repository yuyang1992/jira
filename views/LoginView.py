from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit

from dp.jiraDP import JiraDP


class LoginView(QWidget):
    name = ''
    pw = ''

    def __init__(self, navigation):
        super().__init__()
        self.initView(navigation)

    def initView(self, navigation):
        contentGroup = QVBoxLayout()
        contentGroup.addStretch(1)
        parentGroup = QGridLayout()
        contentGroup.addLayout(parentGroup, 1)
        contentGroup.addStretch(1)
        userNameLable = QLabel("账号")
        userNameEdit = QLineEdit()

        parentGroup.addWidget(userNameLable, 0, 0)
        parentGroup.addWidget(userNameEdit, 0, 1)
        userNameEdit.textChanged.connect(self.changeName)

        userPWLable = QLabel("密码")

        userPWEdit = QLineEdit()
        parentGroup.addWidget(userPWLable, 1, 0)
        parentGroup.addWidget(userPWEdit, 1, 1)

        userPWEdit.textChanged.connect(self.changePW)

        loginBtn = QPushButton('登录', self)
        loginBtn.clicked.connect(lambda: self.onLogin(navigation))
        parentGroup.addWidget(loginBtn, 2, 0, 1, 2, Qt.AlignTop | Qt.AlignCenter)
        self.setLayout(contentGroup)
        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle("巧房jira自动化工具")
        self.show()

    def changeName(self, text):
        self.name = text
        print(text)

    def changePW(self, text):
        self.pw = text
        print(text)

    def onLogin(self, navigation):
        print("登录")
        JiraDP().login(self.name, self.pw)
        navigation.setCurrentIndex(1)
