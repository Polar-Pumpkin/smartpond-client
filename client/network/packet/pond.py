from client.network.packet import IncomingPacket, serializable


@serializable()
class PondList(IncomingPacket):
    ponds: list[str]

    async def execute(self):
        pass
