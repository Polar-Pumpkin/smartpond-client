import machineid

from client.network.packet.base import serializable, IncomingPacket, OutgoingPacket


@serializable()
class RequestNodeRegistration(IncomingPacket):
    async def execute(self):
        from client.network import Client
        Client().connection.send(NodeRegistration())


@serializable()
class NodeRegistration(OutgoingPacket):
    def __init__(self):
        self.signature = machineid.hashed_id('smartpond')
