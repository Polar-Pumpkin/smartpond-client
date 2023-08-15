from typing import List

from client.abstract.monitor import Monitor
from client.network.monitor.prediction import PredictionMonitor
from client.network.websocket import Client


class WeatherMonitor(Monitor):
    count = 0
    predictions: List[PredictionMonitor] = []

    def register_prediction(self, prediction: PredictionMonitor):
        self.predictions.append(prediction)

    @property
    def name(self) -> str:
        return '天气状况'

    @property
    def is_online(self) -> bool:
        return True

    async def report(self):
        self.count += 1
        if self.count < 30:
            return
        self.count = 0

        from client.network.serializable.packet import RequestWeather
        Client().send(RequestWeather())

    async def close(self):
        pass

    async def pull(self) -> List[float]:
        pass
