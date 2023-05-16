from jsonobject import StringProperty

from client.abstract import IncomingPacket, OutgoingPacket, serializable
from client.config import Secrets
from client.network import Client


@serializable
class RequestNodeRegistration(IncomingPacket):
    async def execute(self):
        Client().connection.send(NodeRegistration())


@serializable
class NodeRegistration(OutgoingPacket):
    signature = StringProperty()

    def __init__(self, signature: str = Secrets().signature):
        super().__init__(signature=signature)
