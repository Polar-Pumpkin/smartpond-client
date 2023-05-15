from client.config import Secrets
from client.network.packet import IncomingPacket, serializable, OutgoingPacket


@serializable()
class RequestNodeList(OutgoingPacket):
    def __init__(self, pond_id: str = Secrets().pond_id):
        self.pondId = pond_id


@serializable()
class NodeList(IncomingPacket):
    nodes: list[str]

    async def execute(self):
        # TODO go to node page
        pass


@serializable()
class NodeCreation(OutgoingPacket):
    def __init__(self, name: str, pond_id: str = Secrets().pond_id, signature: str = Secrets().signature):
        self.pondId = pond_id
        self.name = name
        self.signature = signature


@serializable()
class NodeProfile(IncomingPacket):
    async def execute(self):
        pass
