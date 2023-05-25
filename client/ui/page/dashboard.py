from typing import Dict

from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton

from client.config.cached import Cached
from client.network.monitor import Monitors
from client.ui.widget.dashboard import SensorViewWidget
from client.ui.window import MainWindow


class DashboardPage(QWidget):
    def __init__(self, window: MainWindow):
        super().__init__()
        self.window: MainWindow = window
        self.indexes: Dict[str, SensorViewWidget] = {}

        self.context = QVBoxLayout()
        self.setLayout(self.context)
        self.context.setSpacing(10)
        self.context.setObjectName('context')
        self.context.setContentsMargins(0, 0, 0, 0)
        self.context.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.header = QWidget()
        self.context.addWidget(self.header)
        self.header.setFixedHeight(60)
        self.header.setObjectName('header')
        # self.header.setStyleSheet('background-color: #000000;')

        self.header_layout = QHBoxLayout()
        self.header.setLayout(self.header_layout)
        self.header_layout.setSpacing(10)
        self.header_layout.setObjectName('header_layout')
        self.header_layout.setContentsMargins(10, 10, 10, 10)

        self.profile = QVBoxLayout()
        self.header_layout.addLayout(self.profile)
        self.profile.setSpacing(0)
        self.profile.setObjectName('profile')
        self.profile.setContentsMargins(0, 0, 0, 0)

        self.name = QLabel(Cached().profile.node.name)
        self.profile.addWidget(self.name)
        self.name.setObjectName('name')
        name_font = QFont()
        name_font.setPointSize(20)
        name_font.setBold(True)
        self.name.setFont(name_font)

        self.pond = QLabel(Cached().profile.pond.name)
        self.profile.addWidget(self.pond)
        self.pond.setObjectName('pond')

        self.header_space = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.header_layout.addItem(self.header_space)

        self.user = QVBoxLayout()
        self.header_layout.addLayout(self.user)
        self.user.setSpacing(0)
        self.user.setObjectName('user')
        self.user.setContentsMargins(0, 0, 0, 0)

        self.logged = QLabel('已登录为')
        self.user.addWidget(self.logged)
        self.logged.setObjectName('logged')
        self.logged.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.username = QLabel(Cached().profile.username)
        self.user.addWidget(self.username)
        self.username.setObjectName('username')
        username_font = QFont()
        username_font.setPointSize(20)
        username_font.setBold(True)
        self.username.setFont(username_font)
        self.username.setAlignment(Qt.AlignmentFlag.AlignRight)

        # self.grid = QGridLayout()
        # self.context.addLayout(self.grid)
        # self.grid.setSpacing(10)
        # self.grid.setObjectName('grid')
        # self.grid.setContentsMargins(10, 10, 10, 10)

        # self.scroll = QScrollArea()
        # self.context.addWidget(self.scroll)
        # self.scroll.setObjectName('scroll')
        # self.scroll.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # self.scroll.setStyleSheet('background-color: green;')

        # self.area = QWidget()
        # self.area.setObjectName('area')
        # self.area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # self.area.setStyleSheet('background-color: black;')

        self.grid = QVBoxLayout()
        self.context.addLayout(self.grid)
        # self.area.setLayout(self.grid)
        self.grid.setSpacing(10)
        self.grid.setObjectName('grid')
        self.grid.setContentsMargins(10, 10, 10, 10)

        for monitor in Monitors().monitors.values():
            widget = SensorViewWidget(monitor)
            self.indexes[monitor.sensor.name] = widget
            self.grid.addWidget(widget)

        self.create = QPushButton('添加新传感器')
        # self.grid.addWidget(self.create, 0, 0, 1, 4)
        self.grid.addWidget(self.create)
        self.create.setFixedHeight(40)
        self.create.setObjectName('create')
        self.create.setFlat(True)
        self.create.clicked.connect(self.__to_sensor_creation)

        # self.scroll.setWidget(self.area)

    def __to_sensor_creation(self):
        from client.ui.page.sensor import SensorCreatePage
        self.window.builder.emit([SensorCreatePage, self.window])
