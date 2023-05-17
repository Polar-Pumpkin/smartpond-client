import logging
from abc import abstractmethod
from asyncio import Future
from typing import Dict, Any

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from requests import Response

from client.abstract.meta import QABCMeta
from client.ui.src.impl.centralize import Ui_Centralize
from client.ui.widget.common import StatusWidget
from client.ui.widget.namespace import NamespaceCreateWidget, NamespaceSelectWidget
from client.ui.widget.template.displayable import Displayable
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)


class AbstractNamespacePage(QWidget, Ui_Centralize, metaclass=QABCMeta):
    signal_creation = Signal()
    signal_selection = Signal()
    critical = Signal(str)

    def __init__(self, name: str, window: MainWindow, widget: Displayable, namespaces: Dict[str, Any] | None = None,
                 creation_placeholder: str = '{name}名称', creation_confirm: str = '创建{name}',
                 creation_title: str = '没有可用的{name}', creation_secondary: str = '选择已有{name}',
                 selection_confirm: str = '使用该{name}', selection_preferred: str = '创建新{name}',
                 selection_secondary: str = '刷新'):
        super().__init__()
        self.name: str = name
        self.window: MainWindow = window
        self.displayable: Displayable = widget
        self.status: StatusWidget = StatusWidget()
        self.namespaces: Dict[str, Any] = namespaces if namespaces is not None else {}

        self.creation_placeholder = creation_placeholder
        self.creation_confirm = creation_confirm
        self.creation_title = creation_title
        self.creation_secondary = creation_secondary

        self.selection_confirm = selection_confirm
        self.selection_preferred = selection_preferred
        self.selection_secondary = selection_secondary

        self.setupUi(self)
        self._retry()

        self.context.addWidget(self.displayable)
        self.context.addWidget(self.status)

        self.status.action.clicked.connect(self._retry)
        self.signal_creation.connect(self.__to_creation)
        self.signal_selection.connect(self.__to_selection)
        self.critical.connect(self._critical)

    @property
    def length(self) -> int:
        return len(self.namespaces)

    def _retry(self):
        if len(self.namespaces) <= 0:
            self.__to_creation()
        else:
            self.__to_selection()

    def _critical(self, message: str):
        logger.warning(message)
        self.status.show_message(message, False, '重试')

    def __to_creation(self):
        logger.info('切换至命名空间创建页面')
        widget = NamespaceCreateWidget(self.creation_placeholder.format(name=self.name),
                                       self.creation_confirm.format(name=self.name),
                                       self.creation_title.format(name=self.name) if self.length <= 0 else None,
                                       self.creation_secondary.format(name=self.name) if self.length > 0 else None)
        widget.confirm.clicked.connect(self.__create)
        widget.secondary.clicked.connect(self._retry)
        self.displayable.display.emit(widget)

    def __create(self):
        logger.info('执行命名空间创建')
        creation = self.displayable.widget
        if not isinstance(creation, NamespaceCreateWidget):
            self._critical('异常状态')
            return
        self.status.hide_message()
        self.status.show_bar()
        creation.lock()
        if not len(creation.cached_name) > 0:
            self.status.show_message('请输入' + self.creation_placeholder.format(name=self.name))
            creation.unlock()
            return
        logger.info(f'准备创建命名空间: {creation.cached_name}')
        self._create(creation.cached_name)

    @abstractmethod
    def _create(self, name: str):
        raise NotImplementedError

    def __to_selection(self):
        logger.info('切换至命名空间选择页面')
        if len(self.namespaces) <= 0:
            self.signal_creation.emit()
            return
        widget = NamespaceSelectWidget(list(self.namespaces.keys()),
                                       self.selection_confirm.format(name=self.name),
                                       self._show_selected,
                                       self.selection_preferred.format(name=self.name),
                                       self.selection_secondary.format(name=self.name))
        widget.confirm.clicked.connect(self._select)
        widget.header_preferred.clicked.connect(self.__to_creation)
        widget.header_secondary.clicked.connect(self._retry)
        self.displayable.display.emit(widget)

    @abstractmethod
    def _show_selected(self, name: str) -> str:
        raise NotImplementedError

    def __select(self):
        logger.info('执行命名空间选择')
        selection = self.displayable.widget
        if not isinstance(selection, NamespaceSelectWidget):
            self._critical('异常状态')
            return
        self.status.hide_message()
        self.status.show_bar()
        selection.lock()
        logger.info(f'准备选择命名空间: {selection.cached_selected}')
        self._select(selection.cached_selected)

    @abstractmethod
    def _select(self, name: str):
        raise NotImplementedError


class HttpNamespacePage(AbstractNamespacePage):
    def _retry(self):
        self.displayable.clean()
        self.status.show_message(f'正在列出{self.name}', True)
        self._list().add_done_callback(self.__list_callback)

    @abstractmethod
    def _list(self) -> Future[Response]:
        raise NotImplementedError

    def __list_callback(self, future: Future[Response]):
        logger.info('已通过 HTTP 获取命名空间列表')
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

    def _create(self, name: str):
        logger.info('通过 HTTP 创建命名空间')
        self._is_namespace_available(name).add_done_callback(self.__available_callback)

    @abstractmethod
    def _is_namespace_available(self, name: str) -> Future[Response]:
        raise NotImplementedError

    def __available_callback(self, future: Future[Response]):
        logger.info('已通过 HTTP 确认命名空间名称可用性')
        response = future.result()
        payload = response.json()
        name = payload['name']
        is_available = payload['isAvailable']
        try:
            assert response.status_code == 200, f'检查{self.name}名称失败, 请稍后再试'
            assert is_available, f'{self.name}名称已被占用'
        except AssertionError as ex:
            self.status.emit_message(str(ex))
            widget = self.displayable.widget
            if isinstance(widget, NamespaceCreateWidget):
                widget.signal_unlock.emit()
            return
        self._on_create(name).add_done_callback(self.__create_callback)

    @abstractmethod
    def _on_create(self, name: str) -> Future[Response]:
        raise NotImplementedError

    def __create_callback(self, future: Future[Response]):
        logger.info('已通过 HTTP 创建命名空间')
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

    def _select(self, name: str):
        logger.info('通过 HTTP 选择命名空间')
        self._on_select(name).add_done_callback(self._after_select)

    @abstractmethod
    def _on_select(self, name: str) -> Future[Response]:
        raise NotImplementedError

    @abstractmethod
    def _after_select(self, future: Future[Response]):
        raise NotImplementedError
