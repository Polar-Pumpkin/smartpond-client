from jsonobject import ListProperty, StringProperty

from client.config import Secrets
from client.network.packet import IncomingPacket, serializable, OutgoingPacket


@serializable
class PondList(IncomingPacket):
    ponds = ListProperty(str)

    async def execute(self):
        from client.network import Client
        from client.ui.page import PondPage
        Client().window.context.emit(PondPage(Client().window, self.ponds))


@serializable
class PondCreation(OutgoingPacket):
    name = StringProperty()

    def __init__(self, name: str):
        super().__init__(name=name)


@serializable
class PondCreationReceipt(IncomingPacket):
    pondId: StringProperty()

    async def execute(self):
        from client.network import Client
        from client.network.packet import RequestNodeList
        Secrets().set(pond_id=self.pondId)
        Client().connection.send(RequestNodeList())
