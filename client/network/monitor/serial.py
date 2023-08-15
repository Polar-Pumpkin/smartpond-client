import copy
import logging
import struct
import time
from datetime import datetime
from typing import Tuple, List, Dict, Optional

from pymodbus.client import AsyncModbusSerialClient
from pymodbus.register_read_message import ReadHoldingRegistersResponse

from client.abstract.monitor import Monitor
from client.network.monitor.prediction import PredictionMonitor
from client.network.serializable import Sensor, SensorStructure
from client.network.websocket import Client

logger = logging.getLogger(__name__)
commands = {
    'TNET_100': (100, 24, 33)
}


class SerialMonitor(Monitor):
    def __init__(self, sensor: Sensor, structure: SensorStructure, prediction: Optional[PredictionMonitor] = None):
        self.sensor: Sensor = sensor
        self.structure: SensorStructure = structure
        self.prediction = prediction
        self.command: Tuple[int, int, int] = commands[sensor.type]
        self.client: AsyncModbusSerialClient = AsyncModbusSerialClient(port=self.sensor.port,
                                                                       baudrate=9600, bytesize=8,
                                                                       parity='N', stopbits=1)
        self.payload: List[float] | None = None
        self.timestamp: datetime | None = None
        self.history: Dict[str, Dict[datetime, float]] = {}

    @property
    def name(self) -> str:
        return self.sensor.name

    @property
    def is_online(self) -> bool:
        return self.client.connected

    @property
    def last_values(self) -> Dict[str, float] | None:
        datas = self.payload
        if datas is None:
            return None
        return self.match(datas)

    @property
    def last_update(self) -> datetime | None:
        return self.timestamp

    def match(self, values: List[float]) -> Dict[str, float]:
        return dict(filter(lambda x: x[1] != 0.0, zip(self.structure.fields.keys(), values)))

    def record(self):
        timestamp = copy.deepcopy(self.last_update)
        timestamp.replace(second=0, microsecond=0)
        values = self.last_values
        for key, value in values.items():
            records = self.history.get(key, {})
            delta = None
            if len(records) > 0:
                delta = timestamp - max(records.keys())
            if delta is not None and delta.total_seconds() < 60:
                continue
            records[timestamp] = value
            if len(records) > 60:
                records = {x[0]: x[1] for x in records.items() if (timestamp - x[0]).total_seconds() < 3600}
            self.history[key] = records
        for key in list(filter(lambda x: x not in values, self.history.keys())):
            self.history.pop(key)

    async def connect(self):
        await self.client.connect()

    async def close(self):
        await self.client.close()

    async def pull(self) -> List[float] | None:
        if not self.is_online:
            logger.info('正在尝试重新连接至传感器')
            await self.connect()
        if not self.is_online:
            return None
        timestamp = time.time()
        # noinspection PyUnresolvedReferences
        response = await self.client.read_holding_registers(*self.command)
        if not isinstance(response, ReadHoldingRegistersResponse):
            logger.warning(f'与设备通信时收到的响应无效: ({type(response).__name__}) {response}')
            return None
        payload = response.encode()

        values = []
        for index in range(1, payload[0], 4):
            upper = payload[index:index + 2]
            lower = payload[index + 2:index + 4]
            values.append(struct.unpack('>f', lower + upper)[0])
        self.payload = values
        self.timestamp = datetime.now()
        self.record()
        elapsed = int((time.time() - timestamp) * 1000)
        logger.info(f'获取设备 {self.sensor.name} 报告({elapsed}ms)')
        return values

    async def lazy_pull(self):
        if self.payload is None or self.timestamp is None:
            return await self.pull()
        delta = datetime.now() - self.timestamp
        if delta.total_seconds() >= 60:
            return await self.pull()
        return self.payload

    async def report(self):
        datas: List[float] | None = await self.lazy_pull()
        if datas is None:
            return
        fields: Dict[str, float] = self.match(datas)
        logger.info(fields)
        if self.prediction:
            self.prediction.append_serial(fields)
        self.sensor.fields.clear()
        self.sensor.fields.update({x: True for x in fields.keys()})
        from client.network.serializable import SensorReport
        report = SensorReport(node_id=self.sensor.nodeId, sensor_id=self.sensor.id, model=self.sensor.type,
                              fields=fields, timestamp=datetime.now())
        from client.network.serializable.packet import Report
        Client().send(Report(report))
