from datetime import datetime, timedelta
from typing import Dict

from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QWidget
from pyqtgraph import PlotWidget, AxisItem, mkPen

from client.ui.src.impl.sensor_create import Ui_SensorCreate
from client.ui.src.impl.sensor_field import Ui_SensorField


class SensorCreateWidget(QWidget, Ui_SensorCreate):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class SensorFieldWidget(QWidget, Ui_SensorField):
    field = Signal(str)
    history = Signal(dict)

    def __init__(self, name: str, unit: str):
        super().__init__()
        self.setupUi(self)
        self.name.setText(name)
        self.value.setText('--')
        self.unit.setText(unit)

        self.status.hide()
        self.canvas = PlotWidget()
        self.trend.addWidget(self.canvas)
        self.message('暂无数据')

        self.field.connect(self.set_value)
        self.history.connect(self.set_trend)

    def message(self, message: str):
        self.status.show()
        self.canvas.hide()
        self.status.setText(message)

    def set_value(self, value: str):
        self.value.setText(value)

    def set_trend(self, values: Dict[datetime, float]):
        if len(values) <= 0:
            self.message('暂无数据')
            return
        self.status.hide()
        self.canvas.show()
        expanded: Dict[str, float] = {}
        start = datetime.now()
        end = start - timedelta(hours=1)
        cursor = start
        while cursor > end:
            key = cursor.strftime('%H:%M')
            found: datetime | None = None
            for timestamp, value in values.items():
                if timestamp.hour == cursor.hour and timestamp.minute == cursor.minute:
                    expanded[key] = value
                    found = timestamp
            if found is None:
                expanded[key] = 0.0
            else:
                values.pop(found)
            cursor -= timedelta(minutes=1)

        self.canvas.clear()
        x = {}
        y = list(expanded.values())
        keys = list(expanded.keys())
        for index in range(len(keys)):
            num = index + 1
            if num == 1 or num % 10 == 0:
                x[index] = keys[index]
            else:
                x[index] = ''
        # x = dict(enumerate(expanded.keys()))
        xAxis = self.canvas.getAxis('bottom')
        # xAxis = AxisItem(orientation='bottom')
        xAxis.setTicks([x.items()])
        pen = mkPen(color=(77, 81, 87), width=2)
        self.canvas.plot(list(x.keys()), y, pen=pen, axisItems={'bottom': xAxis})
