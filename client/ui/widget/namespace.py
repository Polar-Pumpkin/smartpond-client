from typing import Optional, Sequence, Callable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from client.ui.src.impl import Ui_NamespaceCreate
from client.ui.src.impl import Ui_NamespaceSelect


class NamespaceCreateWidget(QWidget, Ui_NamespaceCreate):
    signal_lock = Signal()
    signal_unlock = Signal()

    def __init__(self, placeholder: str, confirm: str,
                 title: Optional[str] = None,
                 secondary: Optional[str] = None):
        super(NamespaceCreateWidget, self).__init__()
        self.setupUi(self)
        self.allocate(placeholder, confirm, secondary, title)

        self.cached_name: Optional[str] = None

        self.signal_lock.connect(self.lock)
        self.signal_unlock.connect(self.unlock)

    def allocate(self, placeholder: str, confirm: str,
                 secondary: Optional[str] = None,
                 title: Optional[str] = None):
        if title is not None:
            self.title.setText(title)
        else:
            self.title.hide()
        self.name.setPlaceholderText(placeholder)
        self.confirm.setText(confirm)
        if secondary is not None:
            self.secondary.setText(secondary)
        else:
            self.secondary.hide()

    def lock(self):
        self.name.setEnabled(False)
        self.confirm.setEnabled(False)
        self.secondary.setEnabled(False)
        self.cached_name = self.name.text()

    def unlock(self):
        self.name.setEnabled(True)
        self.confirm.setEnabled(True)
        self.secondary.setEnabled(True)
        self.cached_name = None


class NamespaceSelectWidget(QWidget, Ui_NamespaceSelect):
    def __init__(self, namespaces: Sequence[str], confirm: str,
                 select: Callable[[str], str],
                 header_preferred: Optional[str] = None,
                 header_secondary: Optional[str] = None):
        super(NamespaceSelectWidget, self).__init__()
        self.select = select
        self.setupUi(self)
        self.refresh(namespaces)

        self.cached_selected: Optional[str] = None

        self.selected.hide()
        self.confirm.setText(confirm)
        if header_preferred is not None:
            self.header_preferred.setText(header_preferred)
        else:
            self.header_preferred.hide()
        if header_secondary is not None:
            self.header_secondary.setText(header_secondary)
        else:
            self.header_secondary.hide()

        self.namespaces.itemClicked.connect(self.__on_selected)

    def refresh(self, namespaces: Sequence[str]):
        self.namespaces.clear()
        self.namespaces.addItems(namespaces)

    def __on_selected(self, item):
        if self.selected.isHidden():
            self.selected.show()
        self.selected.setText(self.select(item.text()))
        self.cached_selected = item.text()

    def lock(self):
        self.header_preferred.setEnabled(False)
        self.header_secondary.setEnabled(False)
        self.namespaces.setEnabled(False)
        self.confirm.setEnabled(False)

    def unlock(self):
        self.header_preferred.setEnabled(True)
        self.header_secondary.setEnabled(True)
        self.namespaces.setEnabled(False)
        self.confirm.setEnabled(True)