from jsonobject import ListProperty, StringProperty

from client.abstract.packet import IncomingPacket, OutgoingPacket
from client.abstract.serialize import serializable
from client.config.secrets import Secrets
from client.network.websocket import Connection, Client
from client.serializable import Pond
from client.ui.window import MainWindow


@serializable
class PondList(IncomingPacket):
    ponds = ListProperty(Pond)

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        from client.ui.page.pond import PondPage
        window.builder.emit([PondPage, window, self.ponds])


@serializable
class PondCreation(OutgoingPacket):
    name = StringProperty()

    def __init__(self, name: str):
        super().__init__(name=name)


@serializable
class PondCreationReceipt(IncomingPacket):
    pondId: StringProperty()

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        from client.network.packet import RequestNodeList
        Secrets().set(pond_id=self.pondId)
        connection.send(RequestNodeList(Secrets().pond_id))
