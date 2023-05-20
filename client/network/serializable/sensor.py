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
