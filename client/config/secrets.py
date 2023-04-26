import json
import logging
import os.path
from typing import Optional

from client.abstract import Singleton

logger = logging.getLogger(__name__)


class Secrets(metaclass=Singleton):
    def __init__(self):
        self.token: Optional[str] = None

    def save(self):
        with open('.secrets', 'w') as file:
            file.write(json.dumps(self.__dict__))
        logger.info('已保存 Secrets')

    def load(self):
        if not os.path.exists('.secrets'):
            return
        with open('.secrets', 'r') as file:
            self.__dict__.update(json.load(file))
        logger.info('已加载 Secrets')

    def set_token(self, token: str):
        self.token = token
        self.save()
