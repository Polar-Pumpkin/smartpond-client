from PySide6.QtWidgets import QWidget

from client.ui.src.impl.sensor_create import Ui_SensorCreate


class SensorCreateWidget(QWidget, Ui_SensorCreate):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
