from typing import List

from client.config.cached import Cached
from client.network.packet.node import RequestNodeList
from client.network.packet.pond import PondCreation
from client.network.websocket import Client
from client.serializable import Pond
from client.ui.page.template.namespace import AbstractNamespacePage
from client.ui.widget.pond import PondWidget
from client.ui.window import MainWindow


class PondPage(AbstractNamespacePage):
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
