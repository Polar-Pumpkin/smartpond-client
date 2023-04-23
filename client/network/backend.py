import logging
from asyncio import Future

from requests import Response
from requests.auth import AuthBase
from requests_futures.sessions import FuturesSession

from client.abstract import Singleton
from client.network.session import LiveServerSession

logger = logging.getLogger(__name__)


class TokenAuth(AuthBase):
    def __init__(self, token: str):
        self.token: str = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.token
        return r


class Backend(metaclass=Singleton):
    __base_url = 'https://api.entityparrot.cc/smartpond/'
    __session = LiveServerSession(__base_url)
    __client = FuturesSession(session=__session)

    def is_username_available(self, name: str) -> Future[Response]:
        return self.__client.get('/user/available', data=name)

    def reg(self, username: str, password: str) -> Future[Response]:
        return self.__client.post('/user/reg', json={'username': username, 'password': password})

    def login(self, username: str, password: str) -> Future[Response]:
        future = self.__client.post('/user/auth', json={'username': username, 'password': password})
        future.add_done_callback(self.__auth)
        return future

    def __auth(self, future: Future[Response]):
        response = future.result()
        if response.status_code != 200:
            return
        self.__session.auth = TokenAuth(response.json()['token'])
        logger.info('Session 已注册')

    def list_token(self) -> Future[Response]:
        return self.__client.get('/token/list')

    def headers(self) -> Future[Response]:
        return self.__client.get('https://httpbin.org/headers', absolute=True)
