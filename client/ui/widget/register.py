import logging
from typing import Optional, Tuple

from PySide6.QtWidgets import QWidget

from client.ui.src.impl import Ui_Register

logger = logging.getLogger(__name__)


class RegisterWidget(QWidget, Ui_Register):
    def __init__(self):
        super(RegisterWidget, self).__init__()
        self.setupUi(self)

        self.cached_username: Optional[str] = None
        self.cached_password: Optional[str] = None

    def capture(self) -> Tuple[str, str]:
        self.cached_username = self.username.text()
        self.cached_password = self.password.text()
        return self.cached_username, self.cached_password

    def clean(self):
        self.cached_username = None
        self.cached_password = None

    def status_registering(self):
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        self.reg.setEnabled(False)
        self.reg.setText('注册中')

    def status_reset(self):
        self.username.setEnabled(True)
        self.password.setEnabled(True)
        self.password.clear()
        self.reg.setEnabled(True)
        self.reg.setText('注册')
