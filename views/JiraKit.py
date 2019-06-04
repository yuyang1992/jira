from PyQt5.QtWidgets import QMainWindow, QStackedLayout, QVBoxLayout

from views.LoginView import LoginView
from views.MainView import MainView


class JiraKit(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initStatus()

    def initStatus(self):
        qStackedLayout = QStackedLayout()
        qStackedLayout.addWidget(
            LoginView(qStackedLayout))
        qStackedLayout.addWidget(MainView())
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(qStackedLayout)
        self.setLayout(mainLayout)
        self.setGeometry(600, 600, 400, 200)
        self.move(self.window().height() / 2, self.window().width() / 2)
