from typing import List

from client.network import Client
from client.network.packet import PondCreation, RequestNodeList
from client.ui import MainWindow
from client.ui.page.abstract import AbstractNamespacePage
from client.ui.widget import PondWidget


class PondPage(AbstractNamespacePage):
    def __init__(self, window: MainWindow, ponds: List[str]):
        super().__init__('鱼塘', window, PondWidget(), {x: None for x in ponds})

    def _create(self, name: str):
        Client().connection.send(PondCreation(name))

    def _select(self, name: str):
        Client().connection.send(RequestNodeList())

    def _show_selected(self, name: str) -> str:
        return f'已选择:\n{name}'
