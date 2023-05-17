from PySide6.QtWidgets import QWidget

from client.ui.src.impl.token import Ui_Token
from client.ui.widget.template.displayable import Displayable


class TokenWidget(Displayable, Ui_Token):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def _set_context(self, widget: QWidget):
        self.context.addWidget(widget)

    def clean(self):
        if self.widget is not None:
            self.context.removeWidget(self.widget)
            self.widget.deleteLater()
        self.widget = None
