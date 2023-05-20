import asyncio
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

logger = logging.getLogger(__name__)
commands = {
    'TNET100': (100, 22, 33)
}


class Monitor:
    def __init__(self, sensor: Sensor, structure: SensorStructure):
        self.sensor: Sensor = sensor
        self.structure: SensorStructure = structure
        self.command: Tuple[int, int, int] = commands[sensor.type]
        self.client: AsyncModbusSerialClient = AsyncModbusSerialClient(port=self.sensor.port,
                                                                       baudrate=9600, bytesize=8,
                                                                       parity='N', stopbits=1)
        self.timestamp: datetime | None = None

    @property
    def is_online(self):
        return self.client.connected

    @property
    def last_update(self) -> datetime | None:
        return self.timestamp

    async def connect(self):
        await self.client.connect()

    async def close(self):
        await self.client.close()

    async def pull(self) -> List[float] | None:
        response = self.client.read_holding_registers(*self.command)
        if not isinstance(response, ReadHoldingRegistersResponse):
            logger.warning(f'与设备通信时收到的响应无效: ({type(response).__name__}) {response}')
            return None
        payload = response.encode()

        results = []
        for index in range(1, payload[0], 4):
            upper = payload[index:index + 2]
            lower = payload[index + 2:index + 4]
            results.append(struct.unpack('>f', lower + upper)[0])
        self.timestamp = datetime.now()
        return results


class Monitors(metaclass=Singleton):
    def __init__(self):
        self.monitors: Dict[str, Monitor] = {}
        self.__loop: AbstractEventLoop = asyncio.new_event_loop()
        self.__stop_sign: Event = Event()
        self.__stopped: Future = Future()
        self.__thread: Thread | None = None

    @property
    def loop(self) -> AbstractEventLoop:
        return self.__loop

    @property
    def stop_sign(self) -> Event:
        return self.__stop_sign

    @property
    def stopped(self) -> Future:
        return self.__stopped

    @property
    def thread(self) -> Thread | None:
        return self.__thread

    def launch(self, restart: bool = False):
        if self.thread is not None and self.thread.is_alive():
            if not restart:
                logger.info('线程已经启动')
                return
            logger.info('正在取消先前线程')
            self.stop_sign.set()
            self.stopped.result()
        self.__stop_sign = Event()
        self.__stopped = Future()
        self.__thread = Thread(target=self.__thread)
        self.thread.start()

    def stop(self) -> Future[None]:
        self.__stop_sign.set()
        return self.stopped

    def monitor(self, sensor: Sensor) -> Future[None]:
        if not self.thread.is_alive():
            logger.info('线程已经结束, 无法创建监控')
            future = Future()
            future.set_result(None)
            return future
        return asyncio.run_coroutine_threadsafe(self.__monitor(sensor), self.loop)

    async def __monitor(self, sensor: Sensor):
        monitor = Monitor(sensor)
        try:
            await monitor.connect()
        except Exception as ex:
            logger.error(f'连接至设备 {sensor.name} 时遇到问题: {ex}', exc_info=ex)
        self.monitors[sensor.name] = monitor
        logger.info(f'开始监控设备 {sensor.name}')

    async def __corotine(self):
        logger.info('协程已启动')
        while not self.stop_sign.is_set():
            for key, monitor in self.monitors.items():
                timestamp = time.time()
                results = await monitor.pull()
                elapsed = time.time() - timestamp
                logger.info(f'获取设备 {key} 报告({int(elapsed * 1000)}ms)')
                # TODO show results
            # TODO send reports
            await asyncio.sleep(10)
        logger.info('协程准备结束')
        for key, monitor in self.monitors.items():
            await monitor.close()
        logger.info('所有设备已断开连接')
        self.stopped.set_result(None)

    def __thread(self):
        logger.info('线程已启动')
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.__corotine())
        logger.info('线程准备结束')
