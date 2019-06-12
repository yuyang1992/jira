import sys

from PyQt5.QtWidgets import QApplication

from dp.jiraDP import JiraDP
from views.JiraKit import JiraKit

if __name__ == '__main__':
    # JiraDP().login("1", "2")
    app = QApplication(sys.argv)
    login = JiraKit()
    sys.exit(app.exec_())
