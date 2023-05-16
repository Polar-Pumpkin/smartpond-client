from asyncio import Future
from datetime import datetime

from requests import Response

from client.network import Backend, Client
from client.ui import MainWindow
from client.ui.page.template import HttpNamespacePage
from client.ui.widget import TokenWidget


class TokenPage(HttpNamespacePage):
    def __init__(self, window: MainWindow):
        super().__init__('登录凭证', window, TokenWidget())

    def _list(self) -> Future[Response]:
        return Backend().list_token()

    def _extract(self, response: Response):
        for token in response.json()['tokens']:
            self.namespaces[token['name']] = datetime.strptime(token['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')

    def _is_namespace_available(self, name: str) -> Future[Response]:
        return Backend().is_token_available(name)

    def _on_create(self, name: str) -> Future[Response]:
        return Backend().create_token(name)

    def _after_create(self, name: str):
        Backend().generate_token(name).add_done_callback(self.__auth)

    def _on_select(self, name: str) -> Future[Response]:
        return Backend().generate_token(name)

    def _after_select(self, future: Future[Response]):
        self.__auth(future)

    def _show_selected(self, name: str) -> str:
        timestamp = self.namespaces[name]
        return f'已选择: {name}\n创建于 {timestamp.strftime("%Y-%m-%d %H:%M:%S")}'

    def __auth(self, future: Future[Response]):
        response = future.result()
        if response.status_code != 201:
            self.critical.emit('生成登录凭证失败')
            return
        token = response.json()['token']
        Backend().auth(token)
        Client().launch(token)
        self.status.emit_message('正在连接服务器', True)
