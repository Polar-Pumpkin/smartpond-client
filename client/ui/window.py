import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QWidget

from client.config.secrets import Secrets

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    context = Signal(QWidget)
    builder = Signal(list)

    def __init__(self):
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle('智慧鱼塘')

        # self.stacks = QStackedWidget(self)
        # self.stacks.addWidget(LoginWidget())
        self.context.connect(self.setCentralWidget)
        self.builder.connect(self.build)

        from client.network.websocket import Client
        client = Client()
        client.bind(self)

        secrets = Secrets()
        secrets.load()
        if secrets.token is None:
            from client.ui.page.auth import LoginPage
            self.setCentralWidget(LoginPage(self))
        else:
            from client.ui.widget.common import StatusWidget
            status = StatusWidget()
            self.setCentralWidget(status)
            status.show_message('正在连接至服务器', True)
            client.launch(secrets.token)

    def build(self, args: list):
        clazz = args.pop(0)
        self.context.emit(clazz(*args))
