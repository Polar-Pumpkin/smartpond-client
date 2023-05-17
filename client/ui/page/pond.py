from typing import List

from client.network.packet.node import RequestNodeList
from client.network.packet.pond import PondCreation
from client.network.websocket import Client
from client.ui.page.template.namespace import AbstractNamespacePage
from client.ui.widget.pond import PondWidget
from client.ui.window import MainWindow


class PondPage(AbstractNamespacePage):
    def __init__(self, window: MainWindow, ponds: List[str]):
        super().__init__('鱼塘', window, PondWidget(), {x: None for x in ponds})

    def _create(self, name: str):
        Client().connection.send(PondCreation(name))

    def _select(self, name: str):
        Client().connection.send(RequestNodeList())

    def _show_selected(self, name: str) -> str:
        return f'已选择:\n{name}'
