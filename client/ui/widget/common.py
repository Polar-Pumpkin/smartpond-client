from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget

from client.ui.src.impl import Ui_Status


class StatusWidget(QWidget, Ui_Status):
    status = Signal(str, bool)

    def __init__(self, width: int, center: bool = False):
        super(StatusWidget, self).__init__()
        self.setupUi(self)
        self.setFixedWidth(width)
        self.hide_all()

        self.status.connect(self.show_message)
        if center:
            self.message.setAlignment(Qt.AlignCenter)

    def show_bar(self):
        self.bar.show()

    def hide_bar(self):
        self.bar.hide()

    def emit_message(self, message: str, show_bar: bool = False):
        self.status.emit(message, show_bar)

    def show_message(self, message: str, show_bar: bool = False):
        self.__show_message(message)
        self.bar.setHidden(not show_bar)

    def __show_message(self, message: str):
        self.message.show()
        self.message.setText(message)

    def hide_message(self):
        self.message.hide()

    def hide_all(self):
        self.hide_bar()
        self.hide_message()

    def validate_credential(self, username: str, password: str) -> bool:
        try:
            assert len(username) > 0, '请输入用户名'
            assert len(password) > 0, '请输入密码'
        except AssertionError as ex:
            self.show_message(str(ex))
            return False
        return True
