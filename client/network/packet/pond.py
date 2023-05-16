from jsonobject import ListProperty, StringProperty

from client.abstract import IncomingPacket, serializable, OutgoingPacket
from client.config import Secrets
from client.network import Client
from client.network.packet.node import RequestNodeList
from client.ui.page import PondPage


@serializable
class PondList(IncomingPacket):
    ponds = ListProperty(str)

    async def execute(self):
        client = Client()
        window = client.window
        window.builder.emit([PondPage, window, self.ponds])


@serializable
class PondCreation(OutgoingPacket):
    name = StringProperty()

    def __init__(self, name: str):
        super().__init__(name=name)


@serializable
class PondCreationReceipt(IncomingPacket):
    pondId: StringProperty()

    async def execute(self):
        Secrets().set(pond_id=self.pondId)
        Client().connection.send(RequestNodeList())
