from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from client.network.serializable.packet.sensor import RequestSensorTypeList
from client.network.websocket import Client
from client.ui.src.impl.centralize import Ui_Centralize
from client.ui.widget.common import StatusWidget
from client.ui.widget.sensor import SensorCreateWidget
from client.ui.window import MainWindow
from client.util import serial_ports


class SensorCreatePage(QWidget, Ui_Centralize):
    models = Signal(list)
    ready = Signal()

    def __init__(self, window: MainWindow):
        super().__init__()
        self.window: MainWindow = window
        self.widget: SensorCreateWidget = SensorCreateWidget()
        self.status: StatusWidget = StatusWidget()
        self.setupUi(self)
        self.refresh()

        self.context.addWidget(self.widget)
        self.context.addWidget(self.status)

        self.widget.confirm.clicked.connect(self.__confirm)
        self.widget.cancel.clicked.connect(self.__cancel)
        self.models.connect(self.__set_models)
        self.ready.connect(self.__ready)

    def refresh(self):
        self.widget.hide()
        self.status.show_message('连接至服务器', True)

        self.widget.name.clear()
        self.widget.port.clear()
        self.widget.port.addItems(serial_ports())
        Client().connection.send(RequestSensorTypeList())

    def __confirm(self):
        pass

    def __cancel(self):
        from client.ui.page.dashboard import DashboardPage
        self.window.builder.emit([DashboardPage, self.window])

    def __set_models(self, models: List[str]):
        self.widget.model.clear()
        self.widget.model.addItems(models)

    def __ready(self):
        self.widget.show()
        self.status.hide()
