import json
import logging
from json import JSONEncoder
from typing import TypeVar, Any

from jsonobject import JsonObject

from client.abstract.packet import Packet, IncomingPacket, OutgoingPacket

logger = logging.getLogger(__name__)
registered: dict[str, type] = {}
T = TypeVar('T')

field = '__serial_name__'


def serializable(clazz: type[T]) -> type[T]:
    defined = hasattr(clazz, field)
    if defined:
        name = clazz.__serial_name__
    else:
        match clazz:
            case clazz if issubclass(clazz, Packet):
                name = 'cn.edu.bistu.smartpond.packet.Packet'
                match clazz:
                    case clazz if issubclass(clazz, IncomingPacket):
                        name += 'Out'
                    case clazz if issubclass(clazz, OutgoingPacket):
                        name += 'In'
                    case _:
                        raise TypeError(f'无法辨别包 {clazz} 的通信方向')
                name += clazz.__name__
            case _:
                raise ValueError(f'无法生成包 {clazz} 的完整名称')
    if name is None:
        raise ValueError('序列化类型名称不可为 None')
    if not defined:
        setattr(clazz, field, name)
    registered[name] = clazz
    logger.info('注册可序列化对象: ' + name)
    return clazz


class PacketEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if not (isinstance(o, Packet) and hasattr(o, field)):
            if isinstance(o, JsonObject):
                return o.to_json()
            return JSONEncoder.default(self, o)
        values = o.to_json()
        values['=='] = getattr(o, field)
        return values


def serialize(packet: Packet) -> str:
    return json.dumps(packet, cls=PacketEncoder)


def deserialize_from_dict(values: dict[str, Any]) -> Any:
    name = values.pop('==', None)
    if name is None or name not in registered:
        return values
    target = registered[name]
    if issubclass(target, JsonObject):
        return target(values)
    else:
        return target(**values)


def deserialize(content: str, clazz: type[T] | None = None) -> T | Any | None:
    if clazz is None:
        return json.loads(content, object_hook=deserialize_from_dict)
    elif issubclass(clazz, JsonObject):
        return clazz(json.loads(content))
    else:
        return None
