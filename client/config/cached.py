from client.abstract.meta import Singleton


class Cached(metaclass=Singleton):
    def __init__(self):
        from client.network.packet import Profile
        self.pond_id: str | None = None
        self.profile: Profile | None = None
