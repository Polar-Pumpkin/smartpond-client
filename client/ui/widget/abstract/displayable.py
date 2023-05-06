from abc import abstractmethod

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from client.ui.abstract import QABCMeta


class Displayable(metaclass=QABCMeta):
    display = Signal(QWidget)
    widget: QWidget | None = None

    @abstractmethod
    def clean(self):
        raise NotImplementedError
