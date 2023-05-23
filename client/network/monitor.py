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


class MonitorThread(Thread):
    def __init__(self):
        super().__init__()
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
        logger.info('协程已启动')
        count = 0
        while not self.stop_sign.is_set():
            await asyncio.sleep(1)
            count = count + 1
            if count < 10:
                continue
            count = 0
            for key, monitor in self.monitors.items():
                timestamp = time.time()
                results = await monitor.pull()
                elapsed = time.time() - timestamp
                logger.info(f'获取设备 {key} 报告({int(elapsed * 1000)}ms)')
                # TODO show results
            # TODO send reports
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

    def test(self, port: str) -> Future[bool]:
        if not self.is_alive():
            logger.info('线程已经结束, 无法测试连接可用性')
            future = Future()
            future.set_result(False)
            return future
        return asyncio.run_coroutine_threadsafe(self.__test(port), self.loop)

    @staticmethod
    async def __test(port: str) -> bool:
        client = AsyncModbusSerialClient(port=port, baudrate=9600, bytesize=8, parity='N', stopbits=1)
        try:
            await client.connect()
            await asyncio.sleep(1)
            await client.close()
        except:
            logger.error(f'测试与 {port} 通信时遇到错误')
            return False
        return True


class Monitors(metaclass=Singleton):
    def __init__(self):
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
        self.thread = MonitorThread()
        self.thread.start()

    def stop(self) -> Future[None]:
        self.thread.stop_sign.set()
        return self.thread.stopped

    def test(self, port: str) -> Future[bool]:
        if self.thread is None:
            logger.info('未启动线程, 无法测试连接可用性')
            future = Future()
            future.set_result(False)
            return future
        return self.thread.test(port)
