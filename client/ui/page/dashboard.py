from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QGridLayout, \
    QPushButton

from client.config.cached import Cached


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

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

        self.grid =  QVBoxLayout()
        self.context.addLayout(self.grid)
        self.grid.setSpacing(10)
        self.grid.setObjectName('grid')
        self.grid.setContentsMargins(10, 10, 10, 10)

        # TODO 添加传感器 Widget
        profile = Cached().profile
        if profile is not None:
            profile.sensors

        self.create = QPushButton('添加新传感器')
        self.grid.addWidget(self.create, 0, 0, 1, 4)
        self.create.setFixedHeight(40)
        self.create.setObjectName('create')
        self.create.setFlat(True)
