from jsonobject import ListProperty, StringProperty

from client.abstract.packet import IncomingPacket, OutgoingPacket
from client.abstract.serialize import serializable
from client.config.cached import Cached
from client.network.websocket import Connection, Client
from client.network.serializable import Pond
from client.ui.window import MainWindow


@serializable
class PondList(IncomingPacket):
    ponds = ListProperty(Pond)

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        from client.ui.page.registration import PondSelectPage
        window.builder.emit([PondSelectPage, window, self.ponds])


@serializable
class PondCreation(OutgoingPacket):
    name = StringProperty()

    def __init__(self, name: str):
        super().__init__(name=name)


@serializable
class PondCreationReceipt(IncomingPacket):
    pondId: StringProperty()

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        from client.network.serializable.packet import RequestNodeList
        Cached().pond_id = self.pondId
        connection.send(RequestNodeList(Cached().pond_id))
