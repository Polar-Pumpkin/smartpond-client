import logging
from typing import Optional

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget

from client.ui.src.impl.status import Ui_Status

logger = logging.getLogger(__name__)


class StatusWidget(QWidget, Ui_Status):
    status = Signal(str, bool, str)

    def __init__(self, center: bool = False):
        super(StatusWidget, self).__init__()
        self.setupUi(self)
        self.hide_all()

        self.status.connect(self.show_message)
        if center:
            self.message.setAlignment(Qt.AlignCenter)

    def show_bar(self):
        self.bar.show()

    def hide_bar(self):
        self.bar.hide()

    def emit_message(self, message: str, show_bar: bool = False, action: Optional[str] = None):
        self.status.emit(message, show_bar, action)

    def show_message(self, message: str, show_bar: bool = False, action: Optional[str] = None):
        self.message.show()
        self.message.setText(message)
        if show_bar:
            logger.info(message)
        else:
            logger.warning(message)

        self.bar.setHidden(not show_bar)
        if action is not None and len(action) > 0:
            self.show_action(action)

    def hide_message(self):
        self.message.hide()

    def show_action(self, action: str):
        self.action.show()
        self.action.setText(action)

    def hide_action(self):
        self.action.hide()

    def hide_all(self):
        self.hide_bar()
        self.hide_message()
        self.hide_action()

    def validate_credential(self, username: str, password: str) -> bool:
        try:
            assert len(username) > 0, '请输入用户名'
            assert len(password) > 0, '请输入密码'
        except AssertionError as ex:
            self.show_message(str(ex))
            return False
        return True
