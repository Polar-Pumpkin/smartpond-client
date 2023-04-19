import logging
from asyncio import Future
from datetime import datetime
from typing import Optional, Dict

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from requests import Response

from client.network import Backend
from client.ui import MainWindow
from client.ui.src.impl.token import Ui_Token
from client.ui.widget.common import StatusWidget
from client.ui.widget.namespace import NamespaceCreateWidget, NamespaceSelectWidget

logger = logging.getLogger(__name__)


class TokenWidget(QWidget, Ui_Token):
    creation_signal = Signal(bool, str)
    selection_signal = Signal()

    def __init__(self, parent: MainWindow):
        super(TokenWidget, self).__init__()
        self.parent = parent
        self.widget: Optional[QWidget] = None
        self.status: StatusWidget = StatusWidget()
        self.tokens: Dict[str, datetime] = {}
        self.setupUi(self)
        self.footer.addWidget(self.status)
        self.refresh()

        self.creation_signal.connect(self.creation)
        self.selection_signal.connect(self.selection)

    def refresh(self):
        if self.widget is not None:
            self.context.removeWidget(self.widget)
            self.widget = None
        Backend().list_token().add_done_callback(self.__selection)
        self.status.show_message('正在列出登录凭证', True)

    def set_context(self, widget: QWidget):
        if self.widget is not None:
            self.context.removeWidget(self.widget)
        self.widget = widget
        self.context.addWidget(widget)

    def creation(self, has_namespaces: bool, title: Optional[str] = None):
        widget = NamespaceCreateWidget('登录凭据名称', '创建登录凭据', title,
                                       '选择已有登录凭据' if has_namespaces else None)
        self.set_context(widget)
        widget.confirm.clicked.connect(self.__create)
        widget.secondary.clicked.connect(self.refresh)

    def __creation(self):
        self.creation(len(self.tokens) > 0)

    def selection(self):
        widget = NamespaceSelectWidget(list(self.tokens.keys()), '使用该登录凭证',
                                       self.__on_select,
                                       '创建新登录凭证', '刷新')
        self.set_context(widget)
        widget.confirm.clicked.connect(self.__select)
        widget.header_preferred.clicked.connect(self.__creation)
        widget.header_secondary.clicked.connect(self.refresh)

    def __selection(self, future: Future[Response]):
        response = future.result()
        self.status.hide_all()
        self.tokens.clear()
        for token in response.json()['tokens']:
            self.tokens[token['name']] = token['timestamp']
        if len(self.tokens) <= 0:
            self.creation_signal.emit(False, '没有可用的登录凭据')
        else:
            self.selection_signal.emit()

    def __on_select(self, name: str) -> str:
        timestamp = self.tokens[name]
        return f'已选择: ${name}\n创建于 ${timestamp.strftime("%Y-%m-%d %H:%M:%S")}'

    def __create(self, name: str):
        pass

    def __select(self):
        pass
