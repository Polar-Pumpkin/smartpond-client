import logging
from asyncio import Future
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from requests import Response

from client.network import Backend
from client.ui.src.impl.register import Ui_Register
from client.ui.widget.common import StatusWidget
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)


class RegisterWidget(QWidget, Ui_Register):
    navigate = Signal(str)

    def __init__(self, window: MainWindow):
        super(RegisterWidget, self).__init__()
        self.window: MainWindow = window
        self.status: StatusWidget = StatusWidget(True)
        self.setupUi(self)
        self.central.addWidget(self.status)
        self.__status_reset()

        self.__username: Optional[str] = None
        self.__password: Optional[str] = None

        self.login.clicked.connect(self.switch_to_login)
        self.reg.clicked.connect(self.do_register)
        self.navigate.connect(self.__switch_to_login)

    def __clean(self):
        self.__username = None
        self.__password = None

    def switch_to_login(self):
        self.__switch_to_login()

    def __switch_to_login(self, username: Optional[str] = None):
        self.__clean()
        from client.ui.widget.login import LoginWidget
        self.window.context.emit(LoginWidget(self.window, username))

    def do_register(self):
        self.status.hide_message()
        username = self.username.text()
        password = self.password.text()
        if not self.status.validate_credential(username, password):
            return
        self.__username = username
        self.__password = password
        Backend().is_username_available(username).add_done_callback(self.__available_callback)
        self.__status_registering()

    def __status_registering(self):
        self.status.show_bar()
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        self.reg.setEnabled(False)
        self.reg.setText('注册中...')

    def __status_reset(self):
        self.status.hide_all()
        self.username.setEnabled(True)
        self.password.setEnabled(True)
        self.password.clear()
        self.reg.setEnabled(True)
        self.reg.setText('注册')

    def __available_callback(self, future: Future[Response]):
        response = future.result()
        self.__status_reset()
        try:
            assert response.status_code == 200, '用户名检查失败, 请稍后再试'
            assert not response.json()['isAvailable'], '用户名已被占用'
        except AssertionError as ex:
            logger.warning(str(ex))
            self.status.emit_message(str(ex))
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
            self.status.emit_message(message)
            self.__clean()
            return
        self.navigate.emit(self.__username)
