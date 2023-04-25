import logging
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from client.ui.src.impl import Ui_Token

logger = logging.getLogger(__name__)


class TokenWidget(QWidget, Ui_Token):
    display = Signal(QWidget)

    def __init__(self):
        super(TokenWidget, self).__init__()
        self.widget: Optional[QWidget] = None
        self.setupUi(self)

        self.display.connect(self.__set_context)

    def __set_context(self, widget: QWidget):
        self.clean()
        self.widget = widget
        self.context.addWidget(widget)

    def clean(self):
        if self.widget is not None:
            self.context.removeWidget(self.widget)
            self.widget.deleteLater()
        self.widget = None
