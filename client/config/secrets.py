import json
import logging
import os.path
from typing import Optional

import machineid

from client.abstract import Singleton

logger = logging.getLogger(__name__)


class Secrets(metaclass=Singleton):
    def __init__(self):
        self.token: Optional[str] = None
        self.pond_id: Optional[str] = None
        self.signature: str = machineid.hashed_id('smartpond')

    def save(self):
        secrets = self.__dict__
        secrets.pop('signature')
        with open('.secrets', 'w') as file:
            file.write(json.dumps(secrets))
        logger.info('已保存 Secrets')

    def load(self):
        if not os.path.exists('.secrets'):
            return
        with open('.secrets', 'r') as file:
            self.__dict__.update(json.load(file))
        logger.info('已加载 Secrets')

    def set(self, **kwargs):
        self.__dict__.update(kwargs)
        self.save()
