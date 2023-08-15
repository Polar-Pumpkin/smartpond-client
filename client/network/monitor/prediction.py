import logging
from typing import List

import client.service.predict as predict
from client.abstract.monitor import Monitor
from client.model.api import run
from client.model.scaler import MeanScaler
from client.network.serializable import Sensor
from client.network.websocket import Client

_logger = logging.getLogger(__name__)


class PredictionMonitor(Monitor):
    count = 0

    def __init__(self, sensor: Sensor):
        self.sensor = sensor
        self.fields = ['溶解氧', '温度', 'pH', '氨氮', '硝氮']

    @property
    def name(self) -> str:
        return f'{self.sensor.name}[Pred]'

    @property
    def is_online(self) -> bool:
        return True

    async def report(self):
        # self.count += 1
        # if self.count < 30:
        #     return
        # self.count = 0
        frame = predict.pull(self.sensor.id, 200)
        if len(frame) < 200:
            _logger.warning('数据不足 200 条, 暂不执行预测')
            return
        context = {
            'sensorId': self.sensor.id
        }
        for field in self.fields:
            values = run(field, frame, MeanScaler())
            context[field] = values
            _logger.info(f'已完成参数 {field} 的预测')
        from client.network.serializable.packet import RawReport
        Client().send(RawReport('PREDICTION', context))
        _logger.info('已上传预测数据')

    async def close(self):
        pass

    async def pull(self) -> List[float]:
        pass
