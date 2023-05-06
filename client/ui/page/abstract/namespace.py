import logging
from abc import abstractmethod
from asyncio import Future
from typing import Dict, Any

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from requests import Response

from client.ui import MainWindow
from client.ui.abstract import QABCMeta
from client.ui.src.impl import Ui_Centralize
from client.ui.widget import StatusWidget, NamespaceCreateWidget, NamespaceSelectWidget
from client.ui.widget.abstract import Displayable

logger = logging.getLogger(__name__)


class NamespacePage(QWidget, Ui_Centralize, metaclass=QABCMeta):
    signal_creation = Signal()
    signal_selection = Signal()
    critical = Signal(str)

    def __init__(self, name: str, window: MainWindow, widget: Displayable):
        super(NamespacePage, self).__init__()
        self.name = name
        self.window: MainWindow = window
        self.displayable: Displayable = widget
        self.status: StatusWidget = StatusWidget()
        self.namespaces: Dict[str, Any] = {}
        self.setupUi(self)
        self.refresh()

        self.context.addWidget(self.displayable)
        self.context.addWidget(self.status)

        self.status.action.clicked.connect(self.refresh)
        self.signal_creation.connect(self.__to_creation)
        self.signal_selection.connect(self.__to_selection)
        self.critical.connect(self.__critical)

    def refresh(self):
        self.displayable.clean()
        self.status.show_message(f'正在列出{self.name}', True)
        self._list().add_done_callback(self.__list_callback)

    @abstractmethod
    def _list(self) -> Future[Response]:
        raise NotImplementedError

    def __critical(self, message: str):
        self.status.show_message(message, False, '重试')

    def __to_creation(self):
        widget = NamespaceCreateWidget(f'{self.name}名称', f'创建{self.name}',
                                       f'没有可用的{self.name}' if len(self.namespaces) <= 0 else None,
                                       f'选择已有{self.name}' if len(self.namespaces) > 0 else None)
        widget.confirm.clicked.connect(self.__create)
        widget.secondary.clicked.connect(self.refresh)
        self.displayable.display.emit(widget)

    def __create(self):
        creation = self.displayable.widget
        if not isinstance(creation, NamespaceCreateWidget):
            self.__critical('异常状态')
            return
        self.status.hide_message()
        self.status.show_bar()
        creation.lock()
        if not len(creation.cached_name) > 0:
            self.status.show_message(f'请输入{self.name}名称')
            creation.unlock()
            return
        self._is_namespace_available(creation.cached_name).add_done_callback(self.__available_callback)

    @abstractmethod
    def _is_namespace_available(self, name: str) -> Future[Response]:
        raise NotImplementedError

    def __to_selection(self):
        if len(self.namespaces) <= 0:
            self.signal_creation.emit()
            return
        widget = NamespaceSelectWidget(list(self.namespaces.keys()), f'使用该{self.name}',
                                       self._show_selected, f'创建新{self.name}', '刷新')
        widget.confirm.clicked.connect(self.__select)
        widget.header_preferred.clicked.connect(self.__to_creation)
        widget.header_secondary.clicked.connect(self.refresh)
        self.displayable.display.emit(widget)

    def __select(self):
        selection = self.displayable.widget
        if not isinstance(selection, NamespaceSelectWidget):
            self.__critical('异常状态')
            return
        self.status.hide_message()
        self.status.show_bar()
        selection.lock()
        self._on_select(selection.cached_selected).add_done_callback(self._select_callback)

    @abstractmethod
    def _on_select(self, name: str) -> Future[Response]:
        raise NotImplementedError

    def __list_callback(self, future: Future[Response]):
        response = future.result()
        self.status.hide_all()
        self.namespaces.clear()
        if response.status_code != 200:
            self.critical.emit(f'获取{self.name}失败')
            return
        self._extract(response)
        self.signal_selection.emit()

    @abstractmethod
    def _extract(self, response: Response):
        raise NotImplementedError

    def __available_callback(self, future: Future[Response]):
        creation = self.displayable.widget
        if not isinstance(creation, NamespaceCreateWidget):
            self.critical.emit('异常状态')
            return
        response = future.result()
        availability = response.json()
        try:
            assert response.status_code == 200, f'检查{self.name}名称失败, 请稍后再试'
            assert availability['isAvailable'], f'{self.name}名称已被占用'
        except AssertionError as ex:
            self.status.emit_message(str(ex))
            creation.signal_unlock.emit()
            return
        self._on_create(creation.cached_name).add_done_callback(self.__create_callback)

    @abstractmethod
    def _on_create(self, name: str) -> Future[Response]:
        raise NotImplementedError

    def __create_callback(self, future: Future[Response]):
        creation = self.displayable.widget
        if not isinstance(creation, NamespaceCreateWidget):
            self.critical.emit('异常状态')
            return
        response = future.result()
        if response.status_code != 201:
            self.status.emit_message(response.text)
            creation.signal_unlock.emit()
            return
        self._after_create(creation.cached_name)

    @abstractmethod
    def _after_create(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def _select_callback(self, future: Future[Response]):
        raise NotImplementedError

    @abstractmethod
    def _show_selected(self, name: str) -> str:
        raise NotImplementedError
