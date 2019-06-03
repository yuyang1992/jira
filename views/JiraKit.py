from PyQt5.QtWidgets import QWidget, QStackedLayout, QVBoxLayout

from views.LoginView import LoginView
from views.MainView import MainView


class JiraKit(QWidget):

    def __init__(self):
        super().__init__()
        self.initStatus()

    def initStatus(self):
        self.setGeometry(600, 600, 600, 600)
        qStackedLayout = QStackedLayout()
        # qStackedLayout.addWidget(
        #     LoginView(qStackedLayout))
        qStackedLayout.addWidget(MainView())
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(qStackedLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("巧房jira自动化工具")
        self.show()
