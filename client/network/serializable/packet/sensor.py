import logging

from jsonobject import StringProperty, ObjectProperty, SetProperty, IntegerProperty, DefaultProperty

import client.service.mariadb as mariadb
from client.abstract.packet import IncomingPacket, OutgoingPacket
from client.abstract.serialize import serializable
from client.config.cached import Cached
from client.network.serializable import Sensor, SensorStructure, SensorReport
from client.network.websocket import Connection, Client
from client.ui.window import MainWindow

_logger = logging.getLogger(__name__)


@serializable
class RequestSensorTypeList(OutgoingPacket):
    pass


@serializable
class SensorTypeList(IncomingPacket):
    types = SetProperty(str)

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        from client.ui.page.sensor import SensorCreatePage
        widget = window.centralWidget()
        if not isinstance(widget, SensorCreatePage):
            _logger.warning('在主页面非 SensorCreatePage 的情况下收到 SensorTypeList')
            return
        widget.models.emit(list(self.types))
        widget.ready.emit()


@serializable
class SensorCreation(OutgoingPacket):
    name = StringProperty()
    port = StringProperty()
    type = StringProperty()

    def __init__(self, name: str, port: str, model: str):
        super().__init__(name=name, port=port, type=model)


@serializable
class SensorCreationReceipt(IncomingPacket):
    sensor = ObjectProperty(Sensor)
    structure = ObjectProperty(SensorStructure)

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        from client.ui.page.dashboard import DashboardPage
        profile = Cached().profile
        profile.sensors.append(self.sensor)
        if self.structure is not None:
            profile.structures[self.structure.type] = self.structure
        window.builder.emit([DashboardPage, window])


count = 0


def _report_index() -> int:
    global count
    count = count + 1
    return count


@serializable
class Report(OutgoingPacket):
    index = IntegerProperty()
    report = ObjectProperty(SensorReport)

    def __init__(self, report: SensorReport):
        idx = _report_index()
        super().__init__(index=idx, report=report)
        mariadb.save_report(idx, report, report.sensorId)


@serializable
class RawReport(OutgoingPacket):
    index = IntegerProperty()
    type = StringProperty()
    context = DefaultProperty()

    def __init__(self, sensor_type: str, context):
        super().__init__(index=_report_index(), type=sensor_type, context=context)


@serializable
class ReportReceipt(IncomingPacket):
    index = IntegerProperty()
    reportId = StringProperty()

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        mariadb.attach_report_id(self.index, self.reportId)


@serializable
class RequestWeather(OutgoingPacket):
    index = IntegerProperty()

    def __init__(self):
        super().__init__(index=_report_index())


@serializable
class Weather(IncomingPacket):
    index = IntegerProperty()
    context = DefaultProperty()
    reportId = StringProperty()

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        mariadb.save_report(self.index, self.context, report_id=self.reportId)
