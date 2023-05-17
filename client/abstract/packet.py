from abc import abstractmethod
from typing import Any

from jsonobject import JsonObject

from client.abstract.meta import JsonABCMeta
from client.network.websocket import Connection, Client
from client.ui.window import MainWindow


class Packet(JsonObject):
    def __str__(self) -> str:
        from client.abstract.serialize import serialize
        return serialize(self)

    @property
    def context(self) -> dict[str, Any]:
        return self.to_json()


class IncomingPacket(Packet, metaclass=JsonABCMeta):
    # def __init__(self, *args, **kwargs):
    #     if hasattr(self, '__annotations__'):
    #         for key, clazz in self.__annotations__.items():
    #             value = kwargs.pop(key, None)
    #             if value is None:
    #                 raise ValueError(f'{key} is required')
    #             origin = clazz
    #             if isinstance(clazz, GenericAlias):
    #                 origin = clazz.__origin__
    #             if not isinstance(value, origin):
    #                 raise ValueError(f'期望 {key} 为 {origin.__name__}, 实际为 {type(value).__name__}')
    #             setattr(self, key, value)
    #     if len(kwargs) > 0:
    #         raise NameError(f'未知名称: {", ".join(kwargs.keys())}')

    @abstractmethod
    async def execute(self, connection: Connection, client: Client, window: MainWindow):
        raise NotImplementedError


class OutgoingPacket(Packet):
    pass
