import logging
from asyncio import Future
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from requests import Response

from client.network import Backend
from client.ui.src.impl.register import Ui_Register
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)


class RegisterWidget(QWidget, Ui_Register):
    __message = Signal(str)
    __navigate = Signal(str)

    def __init__(self, parent: MainWindow):
        super(RegisterWidget, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.__status_reset()

        self.__username = None
        self.__password = None

        self.login.clicked.connect(self.switch_to_login)
        self.reg.clicked.connect(self.do_register)
        self.__message.connect(self.__show_message)
        self.__navigate.connect(self.__navigate_to_login)

    def switch_to_login(self):
        self.__navigate_to_login()

    def do_register(self):
        if not self.message.isHidden():
            self.message.hide()

        username = self.username.text()
        if len(username) <= 0:
            self.__show_message('请输入用户名')
            return
        self.__username = username

        password = self.password.text()
        if len(password) <= 0:
            self.__show_message('请输入密码')
            return
        self.__password = password

        Backend().is_username_available(username).add_done_callback(self.__available_callback)
        self.__status_registering()

    def __status_registering(self):
        self.bar.show()
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        self.reg.setEnabled(False)
        self.reg.setText('注册中...')

    def __status_reset(self):
        self.message.hide()
        self.bar.hide()
        self.username.setEnabled(True)
        self.password.setEnabled(True)
        self.password.clear()
        self.reg.setEnabled(True)
        self.reg.setText('注册')

    def __show_message(self, message: str):
        self.message.show()
        self.message.setText(message)

    def __clean(self):
        self.__username = None
        self.__password = None

    def __navigate_to_login(self, username: Optional[str] = None):
        self.__clean()
        from client.ui.widget.login import LoginWidget
        self.parent.setCentralWidget(LoginWidget(self.parent, username))

    def __available_callback(self, future: Future[Response]):
        response = future.result()
        self.__status_reset()
        if response.status_code != 200:
            logger.warning('用户名检查失败')
            self.__message.emit('检查用户名失败, 请稍后重试')
            self.__clean()
            return
        if not response.json()['isAvailable']:
            logger.info('用户名不可用')
            self.__message.emit('用户名已被占用')
            self.__clean()
            return
        logger.info('用户名可用')
        Backend().reg(self.__username, self.__password).add_done_callback(self.__register_callback)

    def __register_callback(self, future: Future[Response]):
        response = future.result()
        self.__status_reset()
        if response.status_code != 201:
            message = response.text
            logger.warning('注册失败: ' + message)
            self.__message.emit(message)
            self.__clean()
            return
        self.__navigate.emit(self.__username)
