import logging
from asyncio import Future
from typing import TypeVar

from requests import Response, Session
from requests.auth import AuthBase
from requests_futures.sessions import FuturesSession

from client.abstract.meta import Singleton
from client.config.secrets import Secrets

logger = logging.getLogger(__name__)
T = TypeVar('T')


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

    @staticmethod
    def __watch(func):
        def on_exception(value: Future):
            ex = value.exception()
            if ex is not None:
                logger.critical(f'处理 Future 时遇到错误: {ex}', exc_info=ex)
            else:
                logger.info('Future 正常结束')

        def watched(*args, **kwargs):
            future = func(*args, **kwargs)
            future.add_done_callback(on_exception)
            return future

        return watched

    @__watch
    def is_username_available(self, name: str) -> Future[Response]:
        return self.client.get('/user/available', data=name)

    @__watch
    def reg(self, username: str, password: str) -> Future[Response]:
        return self.client.post('/user/reg', json={'username': username, 'password': password})

    @__watch
    def login(self, username: str, password: str) -> Future[Response]:
        future = self.client.post('/user/auth', json={'username': username, 'password': password})
        future.add_done_callback(self.__auth)
        return future

    def auth(self, token: str, save: bool = False):
        self.session.auth = TokenAuth(token)
        logger.info('Session 已注册')
        if save:
            Secrets().set(token=token)

    def __auth(self, future: Future[Response]):
        response = future.result()
        if response.status_code != 200:
            return
        self.auth(response.json()['token'])

    @__watch
    def list_token(self) -> Future[Response]:
        return self.client.get('/token/list')

    @__watch
    def is_token_available(self, name: str) -> Future[Response]:
        return self.client.get('/token/available', data=name)

    @__watch
    def create_token(self, name: str) -> Future[Response]:
        return self.client.post('/token/create', data=name)

    @__watch
    def generate_token(self, name: str) -> Future[Response]:
        return self.client.get('/token/generate/constant', data=name)
