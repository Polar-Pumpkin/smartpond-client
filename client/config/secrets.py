import copy
import json
import logging
import os.path
from typing import Optional

import machineid

from client.abstract.meta import Singleton

logger = logging.getLogger(__name__)


class Secrets(metaclass=Singleton):
    def __init__(self):
        self.token: Optional[str] = None
        self.pond_id: Optional[str] = None
        self.signature: str = machineid.hashed_id('smartpond')

    def save(self):
        values = copy.deepcopy(self.__dict__)
        values.pop('signature', None)
        with open('.secrets', 'w') as file:
            file.write(json.dumps(values))
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
