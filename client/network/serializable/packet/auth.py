from jsonobject import StringProperty, ObjectProperty, ListProperty, SetProperty

from client.abstract.packet import IncomingPacket, OutgoingPacket
from client.abstract.serialize import serializable
from client.config.cached import Cached
from client.config.secrets import Secrets
from client.network.serializable import Pond, Node, Sensor, SensorStructure
from client.network.websocket import Connection, Client
from client.ui.window import MainWindow


@serializable
class RequestNodeRegistration(IncomingPacket):
    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        connection.send(NodeRegistration(Secrets().signature))


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
    structures = SetProperty(SensorStructure)

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        Cached().profile = self
        from client.network.monitor import Monitors
        monitors = Monitors()
        monitors.launch()
        for sensor in self.sensors:
            monitors.monitor(sensor)

        from client.ui.page.dashboard import DashboardPage
        window.builder.emit([DashboardPage])
