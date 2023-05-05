from client.network.packet.base import serializable, IncomingPacket


@serializable()
class RequestNodeRegistration(IncomingPacket):
    async def execute(self):
        pass
