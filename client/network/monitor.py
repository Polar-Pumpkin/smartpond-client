import asyncio
import copy
import logging
import struct
import time
from asyncio import Event, AbstractEventLoop
from concurrent.futures import Future
from datetime import datetime
from threading import Thread
from typing import Tuple, List, Dict

from pymodbus.client import AsyncModbusSerialClient
from pymodbus.register_read_message import ReadHoldingRegistersResponse

from client.abstract.meta import Singleton
from client.network.serializable import Sensor, SensorStructure
from client.network.websocket import Client
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)
commands = {
    'TNET_100': (100, 24, 33)
}


class Monitor:
    def __init__(self, sensor: Sensor, structure: SensorStructure):
        self.sensor: Sensor = sensor
        self.structure: SensorStructure = structure
        self.command: Tuple[int, int, int] = commands[sensor.type]
        self.client: AsyncModbusSerialClient = AsyncModbusSerialClient(port=self.sensor.port,
                                                                       baudrate=9600, bytesize=8,
                                                                       parity='N', stopbits=1)
        self.payload: List[float] | None = None
        self.timestamp: datetime | None = None
        self.history: Dict[str, Dict[datetime, float]] = {}

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
        self.sensor.fields.clear()
        self.sensor.fields.update({x: True for x in fields.keys()})
        from client.network.serializable import SensorReport
        report = SensorReport(node_id=self.sensor.nodeId, sensor_id=self.sensor.id, model=self.sensor.type,
                              fields=fields, timestamp=datetime.now())
        from client.network.serializable.packet import Report
        Client().connection.send(Report(report))


class MonitorThread(Thread):
    def __init__(self, window: MainWindow):
        super().__init__()
        self.window: MainWindow = window
        self.monitors: Dict[str, Monitor] = {}
        self.__loop: AbstractEventLoop = asyncio.new_event_loop()
        self.__stop_sign: Event = Event()
        self.__stopped: Future = Future()

    @property
    def loop(self) -> AbstractEventLoop:
        return self.__loop

    @property
    def stop_sign(self) -> Event:
        return self.__stop_sign

    @property
    def stopped(self) -> Future[None]:
        return self.__stopped

    def end(self):
        self.__stop_sign.set()
        self.__stopped.result()

    def run(self) -> None:
        logger.info('线程已启动')
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.__corotine())
        logger.info('线程准备结束')

    async def __corotine(self):
        from client.ui.page.dashboard import DashboardPage
        logger.info('协程已启动')
        count = 0
        while not self.stop_sign.is_set():
            await asyncio.sleep(1)
            count = count + 1
            if count < 10:
                continue
            count = 0

            page: DashboardPage | None = None
            widget = self.window.centralWidget()
            if isinstance(widget, DashboardPage):
                page = widget
            for key, monitor in self.monitors.items():
                timestamp = time.time()
                await monitor.report()
                elapsed = int((time.time() - timestamp) * 1000)
                logger.info(f'处理设备 {key} 报告({elapsed}ms)')
                if page is not None:
                    widget = page.indexes.get(key, None)
                    if widget is not None:
                        widget.fetch.emit()

        logger.info('协程准备结束')
        for key, monitor in self.monitors.items():
            await monitor.close()
        logger.info('所有设备已断开连接')
        self.stopped.set_result(None)

    def monitor(self, sensor: Sensor, structure: SensorStructure) -> Future[None]:
        if not self.is_alive():
            logger.info('线程已经结束, 无法创建监控')
            future = Future()
            future.set_result(None)
            return future
        logger.info(f'准备监控传感器 ({sensor.type}) {sensor.name}: {sensor.id}')
        return asyncio.run_coroutine_threadsafe(self.__monitor(sensor, structure), self.loop)

    async def __monitor(self, sensor: Sensor, structure: SensorStructure):
        monitor = Monitor(sensor, structure)
        try:
            await monitor.connect()
        except Exception as ex:
            logger.error(f'连接至设备 {sensor.name} 时遇到问题: {ex}', exc_info=ex)
        self.monitors[sensor.name] = monitor
        logger.info(f'开始监控设备 {sensor.name}')

    def pull(self, monitor: Monitor) -> Future[List[float] | None]:
        if not self.is_alive():
            logger.info('线程已经结束, 无法获取报告')
            future = Future()
            future.set_result(None)
            return future
        return asyncio.run_coroutine_threadsafe(monitor.pull(), self.loop)


class Monitors(metaclass=Singleton):
    def __init__(self):
        self.window: MainWindow | None = None
        self.thread: MonitorThread | None = None

    @property
    def monitors(self) -> Dict[str, Monitor]:
        if self.thread is not None:
            return self.thread.monitors
        else:
            return {}

    def launch(self, restart: bool = False):
        if self.thread is not None and self.thread.is_alive():
            if not restart:
                logger.info('线程已经启动')
                return
            logger.info('正在取消先前线程')
            self.thread.end()
        self.thread = MonitorThread(self.window)
        self.thread.start()

    def stop(self) -> Future[None]:
        if self.thread is None:
            future = Future()
            future.set_result(None)
            return future
        self.thread.stop_sign.set()
        return self.thread.stopped
