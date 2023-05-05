import logging
from asyncio import Future
from datetime import datetime
from typing import Dict

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from requests import Response

from client.network import Backend
from client.network.old_websocket import Websocket
from client.ui import MainWindow
from client.ui.src.impl import Ui_Centralize
from client.ui.widget import StatusWidget, TokenWidget, NamespaceCreateWidget, NamespaceSelectWidget

logger = logging.getLogger(__name__)


class TokenPage(QWidget, Ui_Centralize):
    signal_creation = Signal()
    signal_selection = Signal()
    critical = Signal(str)

    def __init__(self, window: MainWindow):
        super(TokenPage, self).__init__()
        self.window: MainWindow = window
        self.widget: TokenWidget = TokenWidget()
        self.status: StatusWidget = StatusWidget()
        self.tokens: Dict[str, datetime] = {}
        self.setupUi(self)
        self.refresh()

        self.context.addWidget(self.widget)
        self.context.addWidget(self.status)

        self.status.action.clicked.launch(self.refresh)
        self.signal_creation.connect(self.__to_creation)
        self.signal_selection.connect(self.__to_selection)
        self.critical.connect(self.__critical)

    def refresh(self):
        self.widget.clean()
        self.status.show_message('正在列出登录凭证', True)
        Backend().list_token().add_done_callback(self.__list_callback)

    def __critical(self, message: str):
        self.status.show_message(message, False, '重试')

    def __to_creation(self):
        widget = NamespaceCreateWidget('登录凭据名称', '创建登录凭据',
                                       '没有可用的登录凭据' if len(self.tokens) <= 0 else None,
                                       '选择已有登录凭据' if len(self.tokens) > 0 else None)
        widget.confirm.clicked.launch(self.__create)
        widget.secondary.clicked.launch(self.refresh)
        self.widget.display.emit(widget)

    def __create(self):
        creation = self.widget.widget
        if not isinstance(creation, NamespaceCreateWidget):
            self.__critical('异常状态')
            return
        self.status.hide_message()
        self.status.show_bar()
        creation.lock()
        if not len(creation.cached_name) > 0:
            self.status.show_message('请输入登录凭据名称')
            creation.unlock()
            return
        Backend().is_token_available(creation.cached_name).add_done_callback(self.__available_callback)

    def __to_selection(self):
        if len(self.tokens) <= 0:
            self.signal_creation.emit()
            return
        widget = NamespaceSelectWidget(list(self.tokens.keys()), '使用该登录凭证',
                                       self.__on_select, '创建新登录凭证', '刷新')
        widget.confirm.clicked.launch(self.__select)
        widget.header_preferred.clicked.launch(self.__to_creation)
        widget.header_secondary.clicked.launch(self.refresh)
        self.widget.display.emit(widget)

    def __select(self):
        selection = self.widget.widget
        if not isinstance(selection, NamespaceSelectWidget):
            self.__critical('异常状态')
            return
        self.status.hide_message()
        self.status.show_bar()
        selection.lock()
        Backend().generate_token(selection.cached_selected).add_done_callback(self.__generate_callback)

    def __list_callback(self, future: Future[Response]):
        response = future.result()
        self.status.hide_all()
        self.tokens.clear()
        if response.status_code != 200:
            self.critical.emit('获取登录凭据失败')
            return
        for token in response.json()['tokens']:
            self.tokens[token['name']] = datetime.fromtimestamp(token['timestamp'] / 1000)
        self.signal_selection.emit()

    def __available_callback(self, future: Future[Response]):
        creation = self.widget.widget
        if not isinstance(creation, NamespaceCreateWidget):
            self.critical.emit('异常状态')
            return
        response = future.result()
        availability = response.json()
        try:
            assert response.status_code == 200, '检查登录凭证名称失败, 请稍后再试'
            assert availability['isAvailable'], '登录凭证名称已被占用'
        except AssertionError as ex:
            self.status.emit_message(str(ex))
            creation.signal_unlock.emit()
            return
        Backend().create_token(creation.cached_name).add_done_callback(self.__create_callback)

    def __create_callback(self, future: Future[Response]):
        creation = self.widget.widget
        if not isinstance(creation, NamespaceCreateWidget):
            self.critical.emit('异常状态')
            return
        response = future.result()
        if response.status_code != 201:
            self.status.emit_message(response.text)
            creation.signal_unlock.emit()
            return
        Backend().generate_token(creation.cached_name).add_done_callback(self.__generate_callback)

    def __generate_callback(self, future: Future[Response]):
        response = future.result()
        if response.status_code != 201:
            self.critical.emit('生成登录凭证失败')
            return
        token = response.json()['token']
        Backend().auth(token)
        Websocket().launch(token)

    def __on_select(self, name: str) -> str:
        timestamp = self.tokens[name]
        return f'已选择: {name}\n创建于 {timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
