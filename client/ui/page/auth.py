from asyncio import Future
from typing import Optional

from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QWidget
from requests import Response

from client.network.backend import Backend
from client.ui.src.impl.centralize import Ui_Centralize
from client.ui.widget.auth import LoginWidget, RegisterWidget
from client.ui.widget.common import StatusWidget
from client.ui.window import MainWindow


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

        self.widget.login.clicked.connect(self.__to_login)
        self.widget.reg.clicked.connect(self.__register)
        self.navigate.connect(self.__navigate_to_login)

    def __to_login(self):
        self.__navigate_to_login()

    def __navigate_to_login(self, username: Optional[str] = None):
        from client.ui.page.auth import LoginPage
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


class LoginPage(QWidget, Ui_Centralize):
    navigate = Signal()

    def __init__(self, window: MainWindow, username: Optional[str] = None):
        super(LoginPage, self).__init__()
        self.window: MainWindow = window
        self.widget: LoginWidget = LoginWidget()
        self.status: StatusWidget = StatusWidget(True)
        self.setupUi(self)

        self.context.addWidget(self.widget)
        self.context.addWidget(self.status)

        if username is not None:
            self.widget.username.setText(username)

        self.widget.reg.clicked.connect(self.__to_register)
        self.widget.login.clicked.connect(self.__login)
        self.navigate.connect(self.__to_token)

    def __to_register(self):
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
        from client.ui.page.registration import TokenSelectPage
        self.window.context.emit(TokenSelectPage(self.window))

    def __login_callback(self, future: Future[Response]):
        response = future.result()
        self.__status_reset()
        if response.status_code != 200:
            self.status.emit_message('用户名或密码错误')
            return
        self.navigate.emit()
