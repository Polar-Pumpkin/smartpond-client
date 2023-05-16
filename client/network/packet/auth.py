from jsonobject import StringProperty

from client.config import Secrets
from client.network.packet.base import serializable, IncomingPacket, OutgoingPacket


@serializable
class RequestNodeRegistration(IncomingPacket):
    async def execute(self):
        from client.network import Client
        Client().connection.send(NodeRegistration())


@serializable
class NodeRegistration(OutgoingPacket):
    signature = StringProperty()

    def __init__(self, signature: str = Secrets().signature):
        super().__init__(signature=signature)
