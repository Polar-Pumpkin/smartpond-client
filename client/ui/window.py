from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QWidget

from client.config import Secrets


class MainWindow(QMainWindow):
    context = Signal(QWidget)

    def __init__(self):
        super(MainWindow, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('智慧鱼塘')

        # self.stacks = QStackedWidget(self)
        # self.stacks.addWidget(LoginWidget())
        self.context.connect(self.setCentralWidget)

        secrets = Secrets()
        secrets.load()
        if secrets.token is None:
            from client.ui.page import LoginPage
            self.setCentralWidget(LoginPage(self))
        else:
            from client.network.websocket import Websocket
            socket = Websocket()
            socket.bind(self)
            socket.launch(secrets.token)
