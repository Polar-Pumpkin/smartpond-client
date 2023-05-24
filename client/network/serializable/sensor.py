from datetime import datetime
from typing import Dict

from jsonobject import JsonObject, StringProperty, DictProperty, BooleanProperty, DateTimeProperty


class Sensor(JsonObject):
    id = StringProperty(name='_id')
    nodeId = StringProperty()
    name = StringProperty()
    port = StringProperty()
    type = StringProperty()
    fields = DictProperty(bool)
    activated = BooleanProperty()
    modified = DateTimeProperty(exact=True)
    created = DateTimeProperty(exact=True)


class SensorField(JsonObject):
    key = StringProperty()
    name = StringProperty()
    unit = StringProperty()


class SensorStructure(JsonObject):
    type = StringProperty()
    fields = DictProperty(SensorField)


class SensorReport(JsonObject):
    nodeId = StringProperty()
    sensorId = StringProperty()
    type = StringProperty()
    fields = DictProperty(float)
    timestamp = DateTimeProperty(exact=True)

    def __init__(self, node_id: str, sensor_id: str, model: str, fields: Dict[str, float], timestamp: datetime):
        super().__init__(nodeId=node_id, sensorId=sensor_id, type=model, fields=fields, timestamp=timestamp)
