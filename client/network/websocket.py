import logging
from typing import Optional

from websocket import WebSocketApp, WebSocketBadStatusException

from client.abstract import Singleton
from client.ui import MainWindow

logger = logging.getLogger(__name__)


class Websocket(metaclass=Singleton):

    def __init__(self):
        self.window: Optional[MainWindow] = None
        self.client: Optional[WebSocketApp] = None

    def bind(self, window: MainWindow):
        self.window = window

    def launch(self, token: str):
        if self.client is not None:
            self.client.close()
        self.client = WebSocketApp('wss://api.entityparrot.cc/smartpond/client',
                                   header={'Authorization': f'Bearer {token}'},
                                   on_open=self.on_open,
                                   on_message=self.on_message,
                                   on_error=self.on_error,
                                   on_close=self.on_close)
        self.client.run_forever()

    @staticmethod
    def on_open(client):
        logger.info('连接已建立')

    @staticmethod
    def on_message(client, message):
        logger.info('收到数据: ' + str(message))

    def on_error(self, client, error):
        if isinstance(error, WebSocketBadStatusException):
            if error.status_code == 401:
                from client.ui.page import LoginPage
                self.window.context.emit(LoginPage(self.window))
                return
        logger.critical(f'通信时遇到错误: {str(error)}', exc_info=error)
        # TODO Show critical window then exit

    @staticmethod
    def on_close(client, status_code, message):
        logger.info(f'连接已关闭: ({status_code}) {message}')
