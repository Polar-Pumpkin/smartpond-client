import logging
from asyncio import Future
from datetime import datetime
from typing import Dict

from PySide6.QtWidgets import QWidget
from requests import Response

from client.network import Backend
from client.ui import MainWindow
from client.ui.src.impl import Ui_Centralize
from client.ui.widget import StatusWidget, TokenWidget, NamespaceCreateWidget, NamespaceSelectWidget

logger = logging.getLogger(__name__)


class TokenPage(QWidget, Ui_Centralize):
    def __init__(self, window: MainWindow):
        super(TokenPage, self).__init__()
        self.window: MainWindow = window
        self.widget: TokenWidget = TokenWidget()
        self.status: StatusWidget = StatusWidget(400)
        self.tokens: Dict[str, datetime] = {}
        self.setupUi(self)
        self.refresh()

        self.context.addWidget(self.widget)
        self.context.addWidget(self.status)

    def refresh(self):
        self.widget.clean()
        self.status.show_message('正在列出登录凭证', True)
        Backend().list_token().add_done_callback(self.__list_callback)

    def __to_creation(self):
        widget = NamespaceCreateWidget('登录凭据名称', '创建登录凭据',
                                       '没有可用的登录凭据' if len(self.tokens) <= 0 else None,
                                       '选择已有登录凭据' if len(self.tokens) > 0 else None)
        widget.confirm.clicked.connect(self.__create)
        widget.secondary.clicked.connect(self.refresh)
        self.widget.display.emit(widget)

    def __create(self):
        pass

    def __to_selection(self):
        if len(self.tokens) <= 0:
            self.__to_creation()
            return
        widget = NamespaceSelectWidget(list(self.tokens.keys()), '使用该登录凭证',
                                       self.__on_select, '创建新登录凭证', '刷新')
        widget.confirm.clicked.connect(self.__select)
        widget.header_preferred.connect(self.__to_creation)
        widget.header_secondary.connect(self.refresh)
        self.widget.display.emit(widget)

    def __select(self):
        pass

    def __list_callback(self, future: Future[Response]):
        response = future.result()
        logger.info(response.text)
        self.status.hide_all()
        self.tokens.clear()
        for token in response.json()['tokens']:
            self.tokens[token['name']] = token['timestamp']
        self.__to_selection()

    def __on_select(self, name: str) -> str:
        timestamp = self.tokens[name]
        return f'已选择: ${name}\n创建于 ${timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
