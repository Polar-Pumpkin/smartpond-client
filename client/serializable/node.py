from jsonobject import JsonObject, StringProperty, BooleanProperty, DateTimeProperty


class Node(JsonObject):
    id = StringProperty(name='_id')
    pondId = StringProperty()
    name = StringProperty()
    # FIXME Sensitive data
    signature = StringProperty()
    activated = BooleanProperty()
    created = DateTimeProperty(exact=True)
