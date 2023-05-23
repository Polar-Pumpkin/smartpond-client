import logging

from jsonobject import StringProperty, ObjectProperty, SetProperty

from client.abstract.packet import IncomingPacket, OutgoingPacket
from client.abstract.serialize import serializable
from client.config.cached import Cached
from client.network.serializable import Sensor, SensorStructure
from client.network.websocket import Connection, Client
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)


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
            logger.warning('在主页面非 SensorCreatePage 的情况下收到 SensorTypeList')
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
            profile.structures.append(self.structure)
        window.builder.emit([DashboardPage, window])
