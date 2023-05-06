import copy
import json
import logging
from abc import ABCMeta, abstractmethod
from json import JSONEncoder, JSONDecoder
from types import GenericAlias
from typing import TypeVar, Any

logger = logging.getLogger(__name__)
registered: dict[str, type] = {}
T = TypeVar('T')


def serializable(name: str | None = None):
    def _define(cls: type[T]) -> type[T]:
        if name is not None:
            _name = name
        else:
            match cls:
                case cls if issubclass(cls, Packet):
                    _name = 'cn.edu.bistu.smartpond.packet.Packet'
                    match cls:
                        case cls if issubclass(cls, IncomingPacket):
                            _name += 'Out'
                        case cls if issubclass(cls, OutgoingPacket):
                            _name += 'In'
                        case _:
                            raise TypeError(f'Cannot determine packet direction for {cls}')
                    _name += cls.__name__
                case _:
                    raise ValueError(f'Cannot generate serializable name for {cls}')
        if _name is None:
            raise ValueError('Serializable name cannot be None')
        setattr(cls, 'type', _name)
        registered[_name] = cls
        logger.info('注册可序列化对象: ' + _name)
        return cls

    return _define


class Packet:
    def __str__(self) -> str:
        return serialize(self)

    @property
    def context(self) -> dict[str, Any]:
        return self.__dict__


class IncomingPacket(Packet, metaclass=ABCMeta):
    def __init__(self, **kwargs):
        if hasattr(self, '__annotations__'):
            for key, clazz in self.__annotations__.items():
                value = kwargs.pop(key, None)
                if value is None:
                    raise ValueError(f'{key} is required')
                origin = clazz
                if isinstance(clazz, GenericAlias):
                    origin = clazz.__origin__
                if not isinstance(value, origin):
                    raise ValueError(f'{key} is expected to be {origin.__name__}, but actual is {type(value).__name__}')
                setattr(self, key, value)
        if len(kwargs) > 0:
            raise NameError(f'Unknown names: {", ".join(kwargs.keys())}')

    @abstractmethod
    async def execute(self):
        raise NotImplementedError


class OutgoingPacket(Packet):
    pass


class PacketEncoder(JSONEncoder):

    def default(self, o: Any) -> Any:
        if not (isinstance(o, Packet) and hasattr(o, 'type')):
            return JSONEncoder.default(self, o)
        values = copy.deepcopy(o.__dict__)
        values['=='] = getattr(o, 'type')
        return values


class PacketDecoder(JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=PacketDecoder.from_dict)

    @staticmethod
    def from_dict(values: dict[str, Any]):
        name = values.pop('==', None)
        if name is None or name not in registered:
            return None
        return registered[name](**values)


def serialize(packet: Packet) -> str:
    return json.dumps(packet, cls=PacketEncoder)


def deserialize(content: str) -> Any | None:
    return json.loads(content, cls=PacketDecoder)
