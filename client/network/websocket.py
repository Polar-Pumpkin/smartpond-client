import asyncio
import logging
import time
from asyncio import Task, AbstractEventLoop
from concurrent.futures import Future
from threading import Thread

from websockets.client import connect, WebSocketClientProtocol
from websockets.exceptions import InvalidStatusCode

from client.abstract.meta import Singleton
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)


class Connection(Thread):
    def __init__(self, window: MainWindow | None, token: str, connected: Future[None]):
        super().__init__()
        self.__localhost: bool = False
        self.__window: MainWindow | None = window
        self.__token: str = token
        self.__connected: Future[None] = connected

        self.__loop: AbstractEventLoop = asyncio.new_event_loop()
        self.__task: Task[None] | None = None
        self.__client: WebSocketClientProtocol | None = None

    @property
    def window(self) -> MainWindow | None:
        return self.__window

    @property
    def token(self) -> str:
        return self.__token

    @property
    def loop(self) -> AbstractEventLoop:
        return self.__loop

    @property
    def task(self) -> Task[None] | None:
        return self.__task

    @property
    def client(self) -> WebSocketClientProtocol | None:
        return self.__client

    def run(self):
        logger.info('线程已启动')
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.__online())
        logger.info('线程准备结束')

    def stop(self, code: int = 1000, reason: str = 'Client offline') -> Future[None]:
        if not self.is_alive():
            logger.info('线程已经结束, 代表客户端已离线')
            future = Future()
            future.set_result(None)
            return future
        # self.loop.create_task(self.__offline(code, reason))
        return asyncio.run_coroutine_threadsafe(self.__offline(code, reason), self.loop)

    def send(self, packet) -> Future[None]:
        name = type(packet).__name__
        from client.abstract.packet import OutgoingPacket
        assert isinstance(packet, OutgoingPacket), '无效的 packet 对象'
        if not self.is_alive():
            logger.info('线程已经结束, 无法发送数据')
            future = Future()
            future.set_result(None)
            return future
        # self.loop.create_task(self.__send(message))
        from client.abstract.serialize import serialize
        return asyncio.run_coroutine_threadsafe(self.__send(serialize(packet), name), self.loop)

    async def __online(self):
        if self.client is not None:
            logger.warning('客户端已初始化')
            return
        logger.info('客户端准备上线')
        timestamp = time.time()
        try:
            base_url = 'ws://0.0.0.0:8080' if self.__localhost else 'wss://api.entityparrot.cc/smartpond'
            self.__client = await connect(f'{base_url}/client',
                                          extra_headers={'Authorization': f'Bearer {self.token}'})
        except Exception as ex:
            if isinstance(ex, InvalidStatusCode) and ex.status_code == 401:
                logger.info('登录凭证已失效')
                if self.window is not None:
                    from client.ui.page.auth import LoginPage
                    self.window.builder.emit([LoginPage, self.window])
                return
            logger.critical(f'上线时遇到错误: {ex}', exc_info=ex)
            # TODO show critical window then exit
            return
        elapsed = int((time.time() - timestamp) * 1000)
        logger.info(f'客户端已上线({elapsed}ms)')
        self.__connected.set_result(None)
        await self.__listen()

    async def __listen(self):
        from client.abstract.serialize import deserialize
        from client.abstract.packet import IncomingPacket
        async for payload in self.__client:
            if not isinstance(payload, str):
                logger.warning(f'<!- {payload.hex()}')
                continue
            packet = deserialize(payload)
            name = type(packet).__name__
            if not isinstance(packet, IncomingPacket):
                logger.warning(f'<!- ({name}) {payload}')
                continue
            logger.info(f'<-- ({name}) {payload}')
            logger.info(str(packet.to_json()))
            try:
                await packet.execute(self, Client(), self.window)
            except Exception as ex:
                logger.error(f'执行数据包时遇到错误: {ex}', exc_info=ex)
                # TODO maybe message box
        logger.info('客户端已停止数据接收')

    async def __offline(self, code: int, reason: str):
        if self.client is None:
            logger.warning('客户端未初始化')
            return
        if self.client.closed:
            logger.warning('客户端已离线')
            return
        logger.info('客户端准备离线')
        timestamp = time.time()
        await self.__client.close(code, reason)
        elapsed = int((time.time() - timestamp) * 1000)
        logger.info(f'客户端已离线({elapsed}ms)')

    async def __send(self, message: str, name: str = 'PlainText'):
        if self.client is None or not self.client.open:
            logger.warning('客户端未在线, 无法发送数据')
            return
        logger.info(f'--> ({name}) {message}')
        await self.client.send(message)


class Client(metaclass=Singleton):
    def __init__(self):
        self.__window: MainWindow | None = None
        self.__connection: Connection | None = None

    @property
    def window(self) -> MainWindow | None:
        return self.__window

    @property
    def connection(self) -> Connection | None:
        return self.__connection

    def bind(self, window: MainWindow):
        self.__window = window

    def launch(self, token: str) -> Future[None]:
        logger.info('尝试与后端建立 Websocket 连接')
        future = Future()
        old_connection = self.__connection

        self.__connection = Connection(self.__window, token, future)
        logger.info('已创建新连接对象')
        if old_connection is not None:
            logger.info('非首次连接, 将在停止先前连接后运行新的连接')
            old_connection.stop(reason='Reconnect').add_done_callback(self.__connect)
        else:
            logger.info('运行新的连接')
            self.__connect()
        return future

    def stop(self, code: int = 1000, reason: str = 'Client offline') -> Future[None]:
        if self.__connection is None:
            future = Future()
            future.set_result(None)
            return future
        return self.__connection.stop(code, reason)

    def send(self, packet) -> Future[None]:
        completed = Future()
        if self.__connection is None:
            logger.warning('客户端连接未初始化, 无法发送数据')
            completed.set_result(None)
            return completed
        if not self.__connection.is_alive() or not self.__connection.client.open:
            logger.warning('线程已经结束或客户端离线, 尝试重新连接到服务器')
            launched = self.launch(self.__connection.token)
            launched.add_done_callback(
                lambda: self.__connection.send(packet).add_done_callback(lambda: completed.set_result(None))
            )
            return completed
        return self.__connection.send(packet)

    def __connect(self):
        self.__connection.start()
