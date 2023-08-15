from datetime import datetime
from typing import List, Dict

from client.abstract.monitor import Monitor


class PredictionMonitor(Monitor):
    count = 0
    serials: Dict[str, Dict[str, float]] = {}
    weathers: Dict[str, Dict[str, float]] = {}

    def append_serial(self, values: Dict[str, float]):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.serials[timestamp] = values

    def append_weather(self, values: Dict[str, float]):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.weathers[timestamp] = values

    @property
    def name(self) -> str:
        return '预测'

    @property
    def is_online(self) -> bool:
        return True

    async def report(self):
        self.count += 1
        if self.count < 30:
            return
        self.count = 0
        await self.pull()

    async def close(self):
        pass

    async def pull(self) -> List[float]:
        # TODO run prediction
        pass
