import logging
from enum import Enum

from jsonobject import IntegerProperty, DictProperty

from client.abstract.packet import IncomingPacket
from client.abstract.serialize import serializable, deserialize_from_dict
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
    INVALID_SENSOR_ID = 7
    INVALID_SENSOR_NAME = 8


@serializable
class Failure(IncomingPacket):
    code = IntegerProperty()

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        logger.warning(f'收到失败通知: {FailureReason(self.code)}')
        widget = window.centralWidget()
        match self.code:
            case 8:
                from client.ui.page.sensor import SensorCreatePage
                if not isinstance(widget, SensorCreatePage):
                    return
                widget.unlock()
                widget.status.emit_message('该传感器名称已被占用')
            case _:
                pass


@serializable
class Operation(IncomingPacket):
    __serial_name__ = 'cn.edu.bistu.smartpond.packet.Operation'
    operationId = IntegerProperty()
    packet = DictProperty()

    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        packet = deserialize_from_dict(self.packet)
        if not isinstance(packet, IncomingPacket):
            logger.warning(f'收到无法解析的 Operation: {packet}')
            return
        await packet.execute(connection, client, window)
