from jsonobject import JsonObject, StringProperty, ListProperty, BooleanProperty, DateTimeProperty


class Pond(JsonObject):
    _id: StringProperty()
    name: StringProperty()
    owner: StringProperty()
    collaborators: ListProperty(str)
    activated: BooleanProperty()
    created: DateTimeProperty(exact=True)
