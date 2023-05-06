import logging

from PySide6.QtWidgets import QWidget

from client.ui.src.impl import Ui_Token
from client.ui.widget.abstract import Displayable

logger = logging.getLogger(__name__)


class TokenWidget(QWidget, Ui_Token, Displayable):
    def __init__(self):
        super(TokenWidget, self).__init__()
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
