import copy
import logging
from typing import Dict

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QPushButton, \
    QGridLayout

from client.network.monitor import Monitor
from client.ui.widget.sensor import SensorFieldWidget

logger = logging.getLogger(__name__)


class SensorViewWidget(QGroupBox):
    fetch = Signal()

    def __init__(self, monitor: Monitor):
        super().__init__()
        self.monitor: Monitor = monitor
        self.indexes: Dict[str, SensorFieldWidget] = {}

        title = monitor.sensor.name
        self.setTitle(title)
        logger.info(f'创建传感器视图: {title}')

        self.context = QVBoxLayout()
        self.setLayout(self.context)
        self.context.setObjectName('context')
        self.context.setSpacing(10)
        self.context.setContentsMargins(10, 10, 10, 10)

        self.header = QHBoxLayout()
        self.context.addLayout(self.header)
        self.header.setObjectName('header')
        self.header.setSpacing(10)
        self.header.setContentsMargins(0, 0, 0, 0)

        self.online = QLabel('在线' if monitor.is_online else '离线')
        self.header.addWidget(self.online)
        self.online.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        self.header_space = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.header.addItem(self.header_space)

        self.refresh = QPushButton('刷新')
        self.header.addWidget(self.refresh)
        self.refresh.setFlat(True)

        self.label = QLabel()
        self.context.addWidget(self.label)
        self.label.setFixedHeight(40)
        self.label.setObjectName('label')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.hide()

        self.grid: QGridLayout | None = None

        # self.refresh.clicked.connect(self.pull)
        self.fetch.connect(self.pull)

        if not self.monitor.is_online:
            self.message('无法连接至传感器')
        else:
            self.message('正在等待传感器')

    def message(self, message: str):
        self.label.show()
        self.label.setText(message)

    def pull(self):
        # TODO btn
        self.label.hide()
        values = copy.deepcopy(self.monitor.last_values)
        trends = copy.deepcopy(self.monitor.history)
        indexes: Dict[str, SensorFieldWidget] = {}
        for key, value in values.items():
            widget = self.indexes.get(key, None)
            if widget is None:
                field = self.monitor.structure.fields[key]
                widget = SensorFieldWidget(field.name, field.unit)
            widget.set_value(str(round(value, 2)))
            widget.set_trend(trends.get(key, {}))
            indexes[key] = widget
        self.arrange(indexes)

    def arrange(self, widgets: Dict[str, SensorFieldWidget]):
        if set(widgets.keys()) == set(self.indexes.keys()):
            return
        logger.info('重新排列传感器视图')
        values = widgets.values()
        if self.grid is not None:
            for index in range(self.context.count()):
                item = self.context.itemAt(index)
                if item.layout() == self.grid:
                    self.context.removeItem(item)
        self.grid = QGridLayout()
        self.context.addLayout(self.grid)
        x, y = 0, 0
        for widget in values:
            self.grid.addWidget(widget, x, y, 1, 1)
            y += 1
            if y > 1:
                x += 1
                y = 0
        self.indexes = widgets
