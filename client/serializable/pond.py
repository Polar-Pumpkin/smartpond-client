from jsonobject import JsonObject, StringProperty, ListProperty, BooleanProperty, DateTimeProperty


class Pond(JsonObject):
    id = StringProperty(name='_id')
    name = StringProperty()
    owner = StringProperty()
    collaborators = ListProperty(str)
    activated = BooleanProperty()
    created = DateTimeProperty(exact=True)
