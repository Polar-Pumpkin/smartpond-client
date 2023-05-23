from concurrent.futures import Future
from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from client.network.monitor import Monitors
from client.network.serializable.packet.sensor import RequestSensorTypeList, SensorCreation
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

    def lock(self):
        self.widget.name.setEnabled(False)
        self.widget.port.setEnabled(False)
        self.widget.model.setEnabled(False)

    def unlock(self):
        self.widget.name.setEnabled(True)
        self.widget.port.setEnabled(True)
        self.widget.model.setEnabled(True)

    def __confirm(self):
        self.lock()
        self.status.hide_all()
        name = self.widget.name.text()
        if len(name) <= 0:
            self.unlock()
            self.status.show_message('请输入传感器名称')
            return
        port = self.widget.port.currentText()
        self.status.show_message('正在连接至传感器', True)
        Monitors().test(port).add_done_callback(self.__test_callback)

    def __test_callback(self, future: Future[bool]):
        available = future.result()
        if not available:
            self.unlock()
            return
        name = self.widget.name.text()
        port = self.widget.port.currentText()
        model = self.widget.model.currentText()
        self.status.show_message('正在连接至服务器', True)
        Client().connection.send(SensorCreation(name, port, model))

    def __cancel(self):
        from client.ui.page.dashboard import DashboardPage
        self.window.builder.emit([DashboardPage, self.window])

    def __set_models(self, models: List[str]):
        self.widget.model.clear()
        self.widget.model.addItems(models)

    def __ready(self):
        self.widget.show()
        self.status.hide_all()
