from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QStackedLayout

from views.CustomerCountView import CustomerCountView
from views.DingDingDayCountView import DingDingDayCountView
from views.DingDingTestView import DingDingTestView
from views.PlanView import PlanView
from views.SummaryView import SummaryView


class MainView(QWidget):
    navigation = ''

    def __init__(self):
        super().__init__()
        # self.navigation = navigation
        self.initView()

    def initView(self):
        parentGroup = QHBoxLayout()
        leftGroup = QVBoxLayout()
        rightGroup = QHBoxLayout()
        leftList = QListWidget()

        leftList.addItems(["迭代总结统计", "迭代计划统计", "人均Bug统计", "钉钉每日统计", "钉钉测试"])
        leftGroup.addWidget(leftList)
        qStackedLayout = QStackedLayout()
        qStackedLayout.addWidget(SummaryView(qStackedLayout))
        qStackedLayout.addWidget(PlanView(qStackedLayout))
        qStackedLayout.addWidget(CustomerCountView(qStackedLayout))
        qStackedLayout.addWidget(DingDingDayCountView(qStackedLayout))
        qStackedLayout.addWidget(DingDingTestView(qStackedLayout))

        rightGroup.addLayout(qStackedLayout)
        parentGroup.addLayout(leftGroup, 1)
        parentGroup.addLayout(rightGroup, 3)
        leftList.setDragEnabled(True)
        leftList.itemSelectionChanged.connect(
            lambda: qStackedLayout.setCurrentIndex(leftList.currentRow()))
        self.setLayout(parentGroup)

    def show(self):
        self.show()
