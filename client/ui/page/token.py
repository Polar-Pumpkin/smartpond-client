from asyncio import Future
from datetime import datetime

from requests import Response

from client.network import Backend, Client
from client.ui import MainWindow
from client.ui.page.abstract import NamespacePage
from client.ui.widget import TokenWidget


class TokenPage(NamespacePage):
    def __init__(self, window: MainWindow):
        super(TokenPage, self).__init__('登录凭证', window, TokenWidget())
        self.refresh()

    def _list(self) -> Future[Response]:
        return Backend().list_token()

    def _is_namespace_available(self, name: str) -> Future[Response]:
        return Backend().is_token_available(name)

    def _on_select(self, name: str) -> Future[Response]:
        return Backend().generate_token(name)

    def _extract(self, response: Response):
        for token in response.json()['tokens']:
            self.namespaces[token['name']] = datetime.fromtimestamp(token['timestamp'] / 1000)

    def _on_create(self, name: str) -> Future[Response]:
        return Backend().create_token(name)

    def _after_create(self, name: str):
        Backend().generate_token(name).add_done_callback(self.__generate_callback)

    def _select_callback(self, future: Future[Response]):
        self.__generate_callback(future)

    def _show_selected(self, name: str) -> str:
        timestamp = self.namespaces[name]
        return f'已选择: {name}\n创建于 {timestamp.strftime("%Y-%m-%d %H:%M:%S")}'

    def __generate_callback(self, future: Future[Response]):
        response = future.result()
        if response.status_code != 201:
            self.critical.emit('生成登录凭证失败')
            return
        token = response.json()['token']
        Backend().auth(token)
        # TODO waiting
        Client().launch(token)
