from jsonobject import StringProperty, ListProperty

from client.abstract import IncomingPacket, serializable, OutgoingPacket
from client.config import Secrets


@serializable
class RequestNodeList(OutgoingPacket):
    pondId = StringProperty()

    def __init__(self, pond_id: str = Secrets().pond_id):
        super().__init__(pondId=pond_id)


@serializable
class NodeList(IncomingPacket):
    nodes: ListProperty(str)

    async def execute(self):
        # TODO go to node page
        pass


@serializable
class NodeCreation(OutgoingPacket):
    pondId = StringProperty()
    name = StringProperty()
    signature = StringProperty()

    def __init__(self, name: str, pond_id: str = Secrets().pond_id, signature: str = Secrets().signature):
        super().__init__(pondId=pond_id, name=name, signature=signature)


@serializable
class NodeProfile(IncomingPacket):
    async def execute(self):
        pass
