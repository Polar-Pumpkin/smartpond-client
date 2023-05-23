from asyncio import Future
from datetime import datetime
from typing import List

from requests import Response

from client.config.cached import Cached
from client.config.secrets import Secrets
from client.network.backend import Backend
from client.network.serializable import Pond, Node
from client.network.serializable.packet import PondCreation, RequestNodeList, NodeCreation, RequestProfile
from client.network.websocket import Client
from client.ui.page.template.namespace import HttpNamespacePage, AbstractNamespacePage
from client.ui.widget.auth import TokenWidget, PondWidget, NodeWidget
from client.ui.window import MainWindow


class TokenSelectPage(HttpNamespacePage):
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
        Backend().auth(token, True)
        Client().launch(token)
        self.status.emit_message('正在连接服务器', True)


class PondSelectPage(AbstractNamespacePage):
    def __init__(self, window: MainWindow, ponds: List[Pond]):
        super().__init__('鱼塘', window, PondWidget(), {x.name: x for x in ponds})

    def _create(self, name: str):
        self.status.show_message(f'正在创建鱼塘', True)
        Client().connection.send(PondCreation(name))

    def _select(self, name: str):
        self.status.show_message(f'正在与服务器通信', True)
        Cached().pond_id = self.namespaces[name].id
        Client().connection.send(RequestNodeList(Cached().pond_id))

    def _show_selected(self, name: str) -> str:
        timestamp = self.namespaces[name].created.strftime("%Y-%m-%d %H:%M:%S")
        return f'已选择: {name}\n创建于 {timestamp}'


class NodeSelectPage(AbstractNamespacePage):
    def __init__(self, window: MainWindow, nodes: List[Node]):
        super().__init__('节点', window, NodeWidget(), {x.name: x for x in nodes})

    def _create(self, name: str):
        self.status.show_message(f'正在创建节点', True)
        Client().connection.send(NodeCreation(Cached().pond_id, name, Secrets().signature))

    def _select(self, name: str):
        self.status.show_message(f'正在与服务器通信', True)
        Client().connection.send(RequestProfile(self.namespaces[name].id, Secrets().signature))

    def _show_selected(self, name: str) -> str:
        timestamp = self.namespaces[name].created.strftime("%Y-%m-%d %H:%M:%S")
        return f'已选择: {name}\n创建于 {timestamp}'
