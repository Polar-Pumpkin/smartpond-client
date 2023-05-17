from typing import List

from client.config.secrets import Secrets
from client.network.packet import NodeCreation, RequestProfile
from client.network.websocket import Client
from client.serializable import Node
from client.ui.page.template.namespace import AbstractNamespacePage
from client.ui.widget.node import NodeWidget
from client.ui.window import MainWindow


class NodePage(AbstractNamespacePage):
    def __init__(self, window: MainWindow, nodes: List[Node]):
        super().__init__('节点', window, NodeWidget(), {x.name: x for x in nodes})

    def _create(self, name: str):
        self.status.show_message(f'正在创建节点', True)
        Client().connection.send(NodeCreation(Secrets().pond_id, name, Secrets().signature))

    def _select(self, name: str):
        self.status.show_message(f'正在与服务器通信', True)
        Client().connection.send(RequestProfile(self.namespaces[name].id, Secrets().signature))

    def _show_selected(self, name: str) -> str:
        timestamp = self.namespaces[name].created.strftime("%Y-%m-%d %H:%M:%S")
        return f'已选择: {name}\n创建于 {timestamp}'
