import logging
from enum import Enum

from jsonobject import IntegerProperty

from client.abstract.packet import IncomingPacket
from client.abstract.serialize import serializable
from client.network.websocket import Connection, Client
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)


class FailureReason(Enum):
    EXCEPTION = 0
    ALREADY_REGISTRATION = 1
    DUPLICATE_REGISTRATION = 2
    INVALID_POND_NAME = 3
    INVALID_POND_ID = 4
    INVALID_NODE_NAME = 5
    INVALID_NODE_ID = 6


@serializable
class Failure(IncomingPacket):
    code = IntegerProperty()

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        logger.warning(f'收到失败通知: {FailureReason(self.code)}')
