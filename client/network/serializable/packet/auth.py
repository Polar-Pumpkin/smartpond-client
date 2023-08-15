import asyncio
import logging
from concurrent.futures import Future

from jsonobject import StringProperty, ObjectProperty, ListProperty, DictProperty

from client.abstract.packet import IncomingPacket, OutgoingPacket
from client.abstract.serialize import serializable
from client.config.cached import Cached
from client.config.secrets import Secrets
from client.network.serializable import Pond, Node, Sensor, SensorStructure
from client.network.websocket import Connection, Client
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)


@serializable
class RequestNodeRegistration(IncomingPacket):
    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        client.send(NodeRegistration(Secrets().signature))


@serializable
class NodeRegistration(OutgoingPacket):
    signature = StringProperty()

    def __init__(self, signature: str):
        super().__init__(signature=signature)


@serializable
class RequestProfile(OutgoingPacket):
    nodeId = StringProperty()
    signature = StringProperty()

    def __init__(self, node_id: str, signature: str):
        super().__init__(nodeId=node_id, signature=signature)


@serializable
class Profile(IncomingPacket):
    username = StringProperty()
    pond = ObjectProperty(Pond)
    node = ObjectProperty(Node)
    sensors = ListProperty(Sensor)
    structures = DictProperty(SensorStructure)

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        def to_dashboard(task: Future[None] | None):
            if task is not None:
                pass
            from client.ui.page.dashboard import DashboardPage
            window.builder.emit([DashboardPage, window])

        Cached().profile = self
        from client.network.monitors import Monitors
        monitors = Monitors()
        monitors.window = window
        monitors.launch()

        loop = monitors.thread.loop
        futures = []
        for sensor in self.sensors:
            structure = self.structures.get(sensor.type, None)
            if structure is None:
                logger.warning(f'未找到适用于传感器 {sensor.type} 的结构数据')
                continue
            future = monitors.thread.monitor(sensor, structure)
            futures.append(asyncio.wrap_future(future, loop=loop))
        asyncio.gather(*futures).add_done_callback(to_dashboard)
        # to_dashboard(None)
