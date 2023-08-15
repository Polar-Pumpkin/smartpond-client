import logging
import time
from threading import Thread
from typing import List

import client.service.predict as predict
from client.abstract.monitor import Monitor
from client.model.api import run
from client.model.scaler import MeanScaler
from client.network.serializable import Sensor
from client.network.websocket import Client

_logger = logging.getLogger(__name__)


class PredictThread(Thread):

    def __init__(self, sensor_id: str):
        super().__init__()
        self.sensor_id = sensor_id
        self.fields = ['溶解氧', '温度', 'pH', '氨氮', '硝氮']

    def run(self):
        frame = predict.pull(self.sensor_id, 200)
        if len(frame) < 200:
            _logger.warning('数据不足 200 条, 暂不执行预测')
            return
        context = {
            'sensorId': self.sensor_id
        }
        for field in self.fields:
            timestamp = time.time()
            _logger.info(f'开始预测参数: {field}')
            values = run(field, frame, MeanScaler())
            values = list(map(list, values))
            elapsed = int((time.time() - timestamp) * 1000)
            context[field] = values
            _logger.info(f'已完成参数 {field} 的预测({elapsed}ms)')
        from client.network.serializable.packet import RawReport
        Client().send(RawReport('PREDICTION', context))
        _logger.info('已上传预测数据')


class PredictionMonitor(Monitor):
    count = 30

    def __init__(self, sensor: Sensor):
        self.sensor = sensor

    @property
    def name(self) -> str:
        return f'{self.sensor.name}[Pred]'

    @property
    def is_online(self) -> bool:
        return True

    async def report(self):
        self.count += 1
        if self.count < 30:
            return
        self.count = 0
        PredictThread(self.sensor.id).start()

    async def close(self):
        pass

    async def pull(self) -> List[float]:
        pass
