from jsonobject import StringProperty, ListProperty

from client.abstract.packet import IncomingPacket, OutgoingPacket
from client.abstract.serialize import serializable
from client.network.serializable import Node
from client.network.websocket import Connection, Client
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
        from client.ui.page.registration import NodeSelectPage
        window.builder.emit([NodeSelectPage, window, self.nodes])


@serializable
class NodeCreation(OutgoingPacket):
    pondId = StringProperty()
    name = StringProperty()
    signature = StringProperty()

    def __init__(self, pond_id: str, name: str, signature: str):
        super().__init__(pondId=pond_id, name=name, signature=signature)
