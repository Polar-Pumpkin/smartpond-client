from requests import Session


class LiveServerSession(Session):
    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        joined_url = '/'.join([self.base_url.rstrip('/'), url.lstrip('/')])
        return super().request(method, joined_url, *args, **kwargs)
