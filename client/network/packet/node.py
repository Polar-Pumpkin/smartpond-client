from jsonobject import StringProperty, ListProperty, ObjectProperty, SetProperty

from client.abstract.packet import IncomingPacket, OutgoingPacket
from client.abstract.serialize import serializable
from client.network.websocket import Connection, Client
from client.serializable import Pond, Node, Sensor, SensorStructure
from client.ui.window import MainWindow


@serializable
class RequestNodeList(OutgoingPacket):
    pondId = StringProperty()

    def __init__(self, pond_id: str):
        super().__init__(pondId=pond_id)


@serializable
class NodeList(IncomingPacket):
    pondId = StringProperty()
    nodes = ListProperty(Node)

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        from client.ui.page.node import NodePage
        window.builder.emit([NodePage, window, self.nodes])


@serializable
class NodeCreation(OutgoingPacket):
    pondId = StringProperty()
    name = StringProperty()
    signature = StringProperty()

    def __init__(self, pond_id: str, name: str, signature: str):
        super().__init__(pondId=pond_id, name=name, signature=signature)


@serializable
class RequestProfile(OutgoingPacket):
    nodeId = StringProperty()
    signature = StringProperty()

    def __init__(self, node_id: str, signature: str):
        super().__init__(nodeId=node_id, signature=signature)


@serializable
class Profile(IncomingPacket):
    pond = ObjectProperty(Pond)
    node = ObjectProperty(Node)
    sensors = ListProperty(Sensor)
    structures = SetProperty(SensorStructure)

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        # TODO go to main page
        pass
