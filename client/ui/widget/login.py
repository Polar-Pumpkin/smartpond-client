import logging
from typing import Tuple

from PySide6.QtWidgets import QWidget

from client.ui.src.impl import Ui_Login

logger = logging.getLogger(__name__)


class LoginWidget(QWidget, Ui_Login):
    def __init__(self):
        super(LoginWidget, self).__init__()
        self.setupUi(self)

    def capture(self) -> Tuple[str, str]:
        return self.username.text(), self.password.text()

    def status_logging(self):
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        self.login.setEnabled(False)
        self.login.setText('登录中')

    def status_reset(self):
        self.username.setEnabled(True)
        self.password.setEnabled(True)
        self.password.clear()
        self.login.setEnabled(True)
        self.login.setText('登录')
