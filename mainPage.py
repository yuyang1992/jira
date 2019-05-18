import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp


class PyUIWidget(QMainWindow):

    def __init__(self):
        super().__init__()

    def initStatus(self):
        self.statusBar().showMessage("准备就绪...")
        self.setGeometry(300, 300, 250, 250)
        self.setWindowTitle("状态栏")
        self.show()

    def initMenu(self):
        exitAct = QAction(QIcon('exit.png'), "&Exit", self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        # exitAct.triggered.connect(qApp.quit())
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("简单的菜单")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyUIWidget()
    # ex.initStatus()
    ex.initMenu()
    sys.exit(app.exec_())
