import logging
from asyncio import Future

from requests import Response, Session
from requests.auth import AuthBase
from requests_futures.sessions import FuturesSession

from client.abstract import Singleton
from client.config import Secrets

logger = logging.getLogger(__name__)


class LiveServerSession(Session):
    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        if not kwargs.pop('absolute', False):
            url = '/'.join([self.base_url.rstrip('/'), url.lstrip('/')])
        return super().request(method, url, *args, **kwargs)


class TokenAuth(AuthBase):
    def __init__(self, token: str):
        self.token: str = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.token
        return r


class Backend(metaclass=Singleton):
    def __init__(self):
        self.__base_url = 'https://api.entityparrot.cc/smartpond/'
        self.__session = LiveServerSession(self.__base_url)
        self.__client = FuturesSession(session=self.__session)

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def client(self) -> FuturesSession:
        return self.__client

    def stop(self):
        self.client.close()

    def is_username_available(self, name: str) -> Future[Response]:
        return self.client.get('/user/available', data=name)

    def reg(self, username: str, password: str) -> Future[Response]:
        return self.client.post('/user/reg', json={'username': username, 'password': password})

    def login(self, username: str, password: str) -> Future[Response]:
        future = self.client.post('/user/auth', json={'username': username, 'password': password})
        future.add_done_callback(self.__auth)
        return future

    def auth(self, token: str):
        self.session.auth = TokenAuth(token)
        logger.info('Session 已注册')
        Secrets().set_token(token)

    def __auth(self, future: Future[Response]):
        response = future.result()
        if response.status_code != 200:
            return
        self.auth(response.json()['token'])

    def list_token(self) -> Future[Response]:
        return self.client.get('/token/list')

    def is_token_available(self, name: str) -> Future[Response]:
        return self.client.get('/token/available', data=name)

    def create_token(self, name: str) -> Future[Response]:
        return self.client.post('/token/create', data=name)

    def generate_token(self, name: str) -> Future[Response]:
        return self.client.get('/token/generate/constant', data=name)
