import copy
import logging
from concurrent.futures import Future
from typing import List, Dict, Tuple, Set

from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QHBoxLayout, \
    QPushButton
from pyqtgraph import PlotWidget

from client.network.monitor import Monitor, Monitors
from client.network.serializable import Sensor, SensorStructure

logger = logging.getLogger(__name__)


class SensorViewWidget(QWidget):
    values = Signal(dict)

    def __init__(self, monitor: Monitor):
        super().__init__()
        self.monitor: Monitor = monitor
        self.indexes: Dict[str, Tuple[SensorFieldViewWidget, SensorFieldTrendWidget]] = {}
        self.keys: Set[str] | None = None
        logger.info(f'创建传感器 {self.monitor.sensor.name} 的视图控件')

        self.context = QVBoxLayout()
        self.setLayout(self.context)
        self.context.setSpacing(10)
        self.context.setObjectName('context')
        self.context.setContentsMargins(10, 10, 10, 10)

        self.group = QGroupBox(self.sensor.name)
        self.context.addWidget(self.group)
        self.group.setObjectName('group')
        self.group.setContentsMargins(0, 0, 0, 0)

        self.grid = QGridLayout()
        self.group.setLayout(self.grid)
        self.grid.setSpacing(10)
        self.grid.setObjectName('grid')
        self.grid.setContentsMargins(10, 10, 10, 10)

        self.status = QLabel('在线' if self.monitor.is_online else '离线')
        self.grid.addWidget(self.status, 0, 0, 1, 5)
        self.status.setFixedHeight(40)
        self.status.setObjectName('status')

        self.button = QPushButton('刷新')
        self.grid.addWidget(self.button, 0, 5, 1, 1)
        self.button.setFixedHeight(40)
        self.button.setObjectName('pull')
        self.button.setFlat(True)

        self.label = QLabel()
        self.grid.addWidget(self.label, 1, 0, 1, 6)
        self.label.setFixedHeight(40)
        self.label.setObjectName('none')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.hide()

        self.button.clicked.connect(self.pull)
        self.values.connect(self.refresh)

        if not self.monitor.is_online:
            self.message('无法连接至传感器')
            return

        fields = copy.deepcopy(self.sensor.fields)
        if len(fields) <= 0:
            fields.update({x: True for x in self.structure.fields.keys()})
        fields = list(map(lambda x: x[0], filter(lambda x: x[1], fields.items())))
        logger.info(f'有效指标: ({len(fields)}) {", ".join(fields)}')
        if len(fields) > 0:
            for key in fields:
                field = self.structure.fields[key]
                view = SensorFieldViewWidget(field.name, field.unit)
                trend = SensorFieldTrendWidget()
                self.indexes[key] = (view, trend)
            self.arrange()
        else:
            self.message('没有有效指标')

    @property
    def sensor(self) -> Sensor:
        return self.monitor.sensor

    @property
    def structure(self) -> SensorStructure:
        return self.monitor.structure

    def message(self, message: str):
        self.label.show()
        self.label.setText(message)

    def pull(self):
        Monitors().thread.pull(self.monitor).add_done_callback(self.__pull_callback)

    def __pull_callback(self, future: Future[List[float | None]]):
        result = future.result()
        if result is None:
            return
        self.values.emit(self.monitor.match(result))

    def refresh(self, values: Dict[str, float]):
        for key, value in values.items():
            content = str(round(value, 2))
            if key not in self.indexes:
                field = self.structure.fields[key]
                view = SensorFieldViewWidget(field.name, field.unit)
                view.set_value(content)
                trend = SensorFieldTrendWidget()
                self.indexes[key] = (view, trend)
            else:
                view, trend = self.indexes[key]
                view.set_value(content)
        for key in list(filter(lambda x: x[0] not in values, self.indexes)):
            self.indexes.pop(key)
        self.arrange()

    def arrange(self):
        keys = set(self.indexes.keys())
        if self.keys is not None and self.keys == keys:
            return
        index = self.grid.count() - 1
        while index > 1:
            self.grid.takeAt(index)
            index = index - 1
        x = 1
        y = 0
        for key, widgets in self.indexes.items():
            view, trend = widgets
            self.grid.addWidget(view, x, y, 1, 1)
            self.grid.addWidget(trend, x, y + 1, 1, 2)
            y = y + 3
            if y > 3:
                x = x + 1
                y = 0
        self.keys = keys


class SensorFieldViewWidget(QWidget):
    def __init__(self, name: str, unit: str):
        super().__init__()
        self.name = name
        self.unit = unit
        # self.setStyleSheet('background-color: gray;')

        self.setFixedHeight(120)

        self.context = QVBoxLayout()
        self.setLayout(self.context)
        self.context.setSpacing(10)
        self.context.setObjectName('context')
        self.context.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel(self.name)
        self.context.addWidget(self.label)
        self.label.setObjectName('label')
        self.label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.view = QVBoxLayout()
        self.context.addLayout(self.view)
        self.view.setSpacing(0)
        self.view.setObjectName('view')
        self.view.setContentsMargins(0, 0, 0, 0)

        self.value = QLabel('--')
        self.view.addWidget(self.value)
        self.value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        font = QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.value.setFont(font)

        self.footer = QLabel(self.unit)
        self.view.addWidget(self.footer)
        self.label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.footer.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

    def set_value(self, value: str):
        self.value.setText(value)


class SensorFieldTrendWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.setStyleSheet('background-color: gray;')

        self.setFixedHeight(120)

        self.context = QVBoxLayout()
        self.setLayout(self.context)
        self.context.setSpacing(10)
        self.context.setObjectName('context')
        self.context.setContentsMargins(10, 10, 10, 10)

        self.header = QHBoxLayout()
        self.context.addLayout(self.header)
        self.header.setSpacing(0)
        self.header.setObjectName('header')
        self.header.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel('变化趋势')
        self.header.addWidget(self.label)
        self.label.setObjectName('label')
        self.label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.interval = QLabel('一小时内')
        self.header.addWidget(self.interval)
        self.interval.setObjectName('interval')
        self.interval.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.interval.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        self.none = QLabel('暂无数据')
        self.context.addWidget(self.none)
        self.none.setObjectName('none')
        self.none.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.none.setFont(font)

        self.canvas = PlotWidget()
        self.context.addWidget(self.canvas)
        self.canvas.hide()

    def none(self):
        self.none.show()
        self.canvas.hide()

    def set_value(self, values: List[float]):
        self.none.hide()
        self.canvas.show()
        # TODO 绘图
