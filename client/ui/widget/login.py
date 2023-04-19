import logging
from asyncio import Future
from typing import Optional

from PySide6.QtWidgets import QWidget
from requests import Response

from client.network import Backend
from client.ui.src.impl.login import Ui_Login
from client.ui.widget.common import StatusWidget
from client.ui.widget.token import TokenWidget
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)


class LoginWidget(QWidget, Ui_Login):
    def __init__(self, window: MainWindow, username: Optional[str] = None):
        super(LoginWidget, self).__init__()
        self.window: MainWindow = window
        self.status: StatusWidget = StatusWidget(True)
        self.setupUi(self)
        self.central.addWidget(self.status)
        self.__status_reset()

        if username is not None:
            self.username.setText(username)

        self.reg.clicked.connect(self.switch_to_register)
        self.login.clicked.connect(self.do_login)

    def switch_to_register(self):
        from client.ui.widget.register import RegisterWidget
        self.window.context.emit(RegisterWidget(self.window))

    def do_login(self):
        self.status.hide_message()
        username = self.username.text()
        password = self.password.text()
        if not self.status.validate_credential(username, password):
            return
        Backend().login(username, password).add_done_callback(self.__callback)
        self.__status_logging()

    def __status_logging(self):
        self.status.show_bar()
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        self.login.setEnabled(False)
        self.login.setText('登录中...')

    def __status_reset(self):
        self.status.hide_all()
        self.username.setEnabled(True)
        self.password.setEnabled(True)
        self.password.clear()
        self.login.setEnabled(True)
        self.login.setText('登录')

    def __callback(self, future: Future[Response]):
        response = future.result()
        self.__status_reset()
        if response.status_code != 200:
            logger.warning('登录失败')
            self.status.emit_message('用户名或密码错误')
            return
        logger.info('登录成功')
        self.window.context.emit(TokenWidget(self.window))
