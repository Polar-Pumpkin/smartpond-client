import logging
from abc import abstractmethod

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from client.ui.abstract import QABCMeta

logger = logging.getLogger(__name__)


class Displayable(QWidget, metaclass=QABCMeta):
    display = Signal(QWidget)
    widget: QWidget | None = None

    def __init__(self):
        super().__init__()
        self.display.connect(self.set_context)

    def set_context(self, widget: QWidget):
        logger.info(f'设置显示内容: {type(widget).__name__}')
        self.clean()
        self._set_context(widget)
        self.widget = widget

    @abstractmethod
    def _set_context(self, widget: QWidget):
        raise NotImplementedError

    @abstractmethod
    def clean(self):
        raise NotImplementedError
