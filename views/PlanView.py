from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QGridLayout, QLineEdit, \
    QPushButton


class PlanView(QWidget):
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
        userNameLable = QLabel("账号")
        userNameEdit = QLineEdit()

        parentGroup.addWidget(userNameLable, 0, 0)
        parentGroup.addWidget(userNameEdit, 0, 1)
        # userNameEdit.textChanged.connect(self.changeName)

        userPWLable = QLabel("密码")

        userPWEdit = QLineEdit()
        parentGroup.addWidget(userPWLable, 1, 0)
        parentGroup.addWidget(userPWEdit, 1, 1)

        # userPWEdit.textChanged.connect(self.changePW)

        loginBtn = QPushButton('登录', self)
        # loginBtn.clicked.connect(lambda: self.onLogin(self.navigation))
        parentGroup.addWidget(loginBtn, 2, 0, 1, 2, Qt.AlignTop | Qt.AlignCenter)
        parentGroup = QHBoxLayout()
        self.setLayout(parentGroup)

    def show(self):
        self.show()
