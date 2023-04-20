from asyncio import Future
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from requests import Response

from client.network import Backend
from client.ui import MainWindow
from client.ui.src.impl import Ui_Centralize
from client.ui.widget import LoginWidget
from client.ui.widget import StatusWidget


class LoginPage(QWidget, Ui_Centralize):
    navigate = Signal()

    def __init__(self, window: MainWindow, username: Optional[str] = None):
        super(LoginPage, self).__init__()
        self.window: MainWindow = window
        self.widget: LoginWidget = LoginWidget()
        self.status: StatusWidget = StatusWidget(400, True)
        self.setupUi(self)

        self.context.addWidget(self.widget)
        self.context.addWidget(self.status)

        if username is not None:
            self.widget.username.setText(username)

        self.widget.reg.clicked.connect(self.__to_register)
        self.widget.login.clicked.connect(self.__login)
        self.navigate.connect(self.__to_token)

    def __to_register(self):
        from client.ui.page.register import RegisterPage
        self.window.context.emit(RegisterPage(self.window))

    def __login(self):
        username, password = self.widget.capture()
        if not self.status.validate_credential(username, password):
            return
        self.__status_logging()
        Backend().login(username, password).add_done_callback(self.__login_callback)

    def __status_logging(self):
        self.status.hide_message()
        self.status.show_bar()
        self.widget.status_logging()

    def __status_reset(self):
        self.status.hide_all()
        self.widget.status_reset()

    def __to_token(self):
        from client.ui.page import TokenPage
        self.window.context.emit(TokenPage(self.window))

    def __login_callback(self, future: Future[Response]):
        response = future.result()
        self.__status_reset()
        if response.status_code != 200:
            self.status.emit_message('用户名或密码错误')
            return
        self.navigate.emit()
