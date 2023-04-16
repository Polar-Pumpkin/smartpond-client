import logging
from asyncio import Future
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from requests import Response

from client.network import Backend
from client.ui.src.impl.login import Ui_Login
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)


class LoginWidget(QWidget, Ui_Login):
    __message = Signal(str)

    def __init__(self, parent: MainWindow, username: Optional[str] = None):
        super(LoginWidget, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.__status_reset()

        if username is not None:
            self.username.setText(username)

        self.reg.clicked.connect(self.switch_to_register)
        self.login.clicked.connect(self.do_login)
        self.__message.connect(self.__show_message)

    def switch_to_register(self):
        from client.ui.widget.register import RegisterWidget
        self.parent.setCentralWidget(RegisterWidget(self.parent))

    def do_login(self):
        if not self.message.isHidden():
            self.message.hide()

        username = self.username.text()
        if len(username) <= 0:
            self.__show_message('请输入用户名')
            return

        password = self.password.text()
        if len(password) <= 0:
            self.__show_message('请输入密码')
            return

        Backend().login(username, password).add_done_callback(self.__callback)
        self.__status_logging()

    def __status_logging(self):
        self.bar.show()
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        self.login.setEnabled(False)
        self.login.setText('登录中...')

    def __status_reset(self):
        self.message.hide()
        self.bar.hide()
        self.username.setEnabled(True)
        self.password.setEnabled(True)
        self.password.clear()
        self.login.setEnabled(True)
        self.login.setText('登录')

    def __show_message(self, message: str):
        self.message.show()
        self.message.setText(message)

    def __callback(self, future: Future[Response]):
        response = future.result()
        self.__status_reset()
        if response.status_code != 200:
            logger.warning('登录失败')
            self.__message.emit('用户名或密码错误')
            return
        logger.info('登录成功')
        # TODO Token selection
