from asyncio import Future
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from requests import Response

from client.network import Backend
from client.ui import MainWindow
from client.ui.src.impl import Ui_Centralize
from client.ui.widget import StatusWidget
from client.ui.widget import RegisterWidget


class RegisterPage(QWidget, Ui_Centralize):
    navigate = Signal(str)

    def __init__(self, window: MainWindow):
        super(RegisterPage, self).__init__()
        self.window: MainWindow = window
        self.widget: RegisterWidget = RegisterWidget()
        self.status: StatusWidget = StatusWidget(True)
        self.setupUi(self)

        self.context.addWidget(self.widget)
        self.context.addWidget(self.status)

        self.widget.login.clicked.launch(self.__to_login)
        self.widget.reg.clicked.launch(self.__register)
        self.navigate.connect(self.__navigate_to_login)

    def __to_login(self):
        self.__navigate_to_login()

    def __navigate_to_login(self, username: Optional[str] = None):
        from client.ui.page.login import LoginPage
        self.window.context.emit(LoginPage(self.window, username))

    def __register(self):
        username, password = self.widget.capture()
        if not self.status.validate_credential(username, password):
            return
        self.__status_registering()
        Backend().is_username_available(username).add_done_callback(self.__available_callback)

    def __status_registering(self):
        self.status.hide_message()
        self.status.show_bar()
        self.widget.status_registering()

    def __available_callback(self, future: Future[Response]):
        response = future.result()
        try:
            assert response.status_code == 200, '检查用户名失败, 请稍后再试'
            assert response.json()['isAvailable'], '用户名已被占用'
        except AssertionError as ex:
            self.status.emit_message(str(ex))
            self.widget.status_reset()
            self.widget.clean()
            return
        Backend().reg(self.widget.cached_username, self.widget.cached_password) \
            .add_done_callback(self.__register_callback)

    def __register_callback(self, future: Future[Response]):
        response = future.result()
        if response.status_code != 201:
            self.status.emit_message(response.text)
            self.widget.status_reset()
            self.widget.clean()
            return
        self.navigate.emit(self.widget.cached_username)
