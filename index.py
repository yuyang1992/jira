import sys

from PyQt5.QtWidgets import QApplication

from views.JiraKit import JiraKit

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = JiraKit()
    sys.exit(app.exec_())
