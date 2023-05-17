from jsonobject import StringProperty

from client.abstract.packet import IncomingPacket, OutgoingPacket
from client.abstract.serialize import serializable
from client.config.secrets import Secrets
from client.network.websocket import Connection, Client
from client.ui.window import MainWindow


@serializable
class RequestNodeRegistration(IncomingPacket):
    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        connection.send(NodeRegistration(Secrets().signature))


@serializable
class NodeRegistration(OutgoingPacket):
    signature = StringProperty()

    def __init__(self, signature: str):
        super().__init__(signature=signature)
