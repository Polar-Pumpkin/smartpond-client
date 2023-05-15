from client.config import Secrets
from client.network import Client
from client.network.packet import IncomingPacket, serializable, OutgoingPacket, RequestNodeList
from client.ui.page import PondPage


@serializable()
class PondList(IncomingPacket):
    ponds: list[str]

    async def execute(self):
        Client().window.context.emit(PondPage(Client().window, self.ponds))


@serializable()
class PondCreation(OutgoingPacket):
    def __init__(self, name: str):
        self.name = name


@serializable()
class PondCreationReceipt(IncomingPacket):
    pondId: str

    async def execute(self):
        Secrets().set(pond_id=self.pondId)
        Client().connection.send(RequestNodeList())
