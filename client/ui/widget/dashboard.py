from typing import List

from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QHBoxLayout
from pyqtgraph import PlotWidget

from client.network.monitor import Monitor
from client.network.serializable import Sensor, SensorStructure, SensorField


class SensorViewWidget(QWidget):
    def __init__(self, monitor: Monitor):
        super().__init__()
        self.monitor = monitor

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
        self.grid.addWidget(self.status, 0, 0, 1, 6)
        self.status.setFixedHeight(20)
        self.status.setObjectName('status')

        fields = list(filter(lambda x: x[1], self.sensor.fields.items()))
        match len(fields):
            case 0:
                self.none = QLabel('没有有效指标')
                self.grid.addWidget(self.none, 1, 0, 1, 6)
                self.none.setFixedHeight(20)
                self.none.setObjectName('none')
                self.none.setAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont()
                font.setPointSize(20)
                font.setBold(True)
                self.none.setFont(font)
            case 1:
                key, _ = fields[0]
                field: SensorField = self.structure.fields[key]
                self.grid.addWidget(SensorFieldViewWidget(field.name, field.unit), 1, 0, 1, 2)
                self.grid.addWidget(SensorFieldTrendWidget(), 1, 2, 1, 4)
            case _:
                count = 1
                for key, value in fields:
                    pass

    @property
    def sensor(self) -> Sensor:
        return self.monitor.sensor

    @property
    def structure(self) -> SensorStructure:
        return self.monitor.structure


class SensorFieldViewWidget(QWidget):
    def __init__(self, name: str, unit: str):
        super().__init__()
        self.name = name
        self.unit = unit

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
