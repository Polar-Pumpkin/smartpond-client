from typing import Optional, Tuple

from PySide6.QtWidgets import QWidget

from client.ui.src.impl.login import Ui_Login
from client.ui.src.impl.node import Ui_Node
from client.ui.src.impl.pond import Ui_Pond
from client.ui.src.impl.register import Ui_Register
from client.ui.src.impl.token import Ui_Token
from client.ui.widget.template.displayable import Displayable


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


class PondWidget(Displayable, Ui_Pond):
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


class NodeWidget(Displayable, Ui_Node):
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
