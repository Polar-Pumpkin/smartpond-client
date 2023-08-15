from abc import ABCMeta, abstractmethod
from typing import List


class Monitor(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_online(self) -> bool:
        pass

    @abstractmethod
    async def report(self):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def pull(self) -> List[float]:
        pass
