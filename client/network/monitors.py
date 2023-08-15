import asyncio
import logging
import time
from asyncio import Event, AbstractEventLoop
from concurrent.futures import Future
from threading import Thread
from typing import List, Dict

from client.abstract.meta import Singleton
from client.abstract.monitor import Monitor
from client.network.monitor.prediction import PredictionMonitor
from client.network.monitor.serial import SerialMonitor
from client.network.monitor.weather import WeatherMonitor
from client.network.serializable import Sensor, SensorStructure
from client.ui.window import MainWindow

logger = logging.getLogger(__name__)
commands = {
    'TNET_100': (100, 24, 33)
}


class MonitorThread(Thread):
    def __init__(self, window: MainWindow):
        super().__init__()
        self.window: MainWindow = window
        self.monitors: Dict[str, Monitor] = {}

        self.weather: WeatherMonitor = WeatherMonitor()
        self.monitors['weather'] = self.weather

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
        count = 50
        while not self.stop_sign.is_set():
            await asyncio.sleep(1)
            count = count + 1
            if count < 60:
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
        monitor = self.monitors.get(sensor.name, None)
        if monitor is not None and monitor.is_online:
            logger.info(f'复用设备 {sensor.name} 的监控实例')
            return
        prediction = PredictionMonitor()
        monitor = SerialMonitor(sensor, structure, prediction)
        try:
            await monitor.connect()
        except Exception as ex:
            logger.error(f'连接至设备 {sensor.name} 时遇到问题: {ex}', exc_info=ex)
        self.monitors[sensor.name] = monitor
        self.monitors[f'{sensor.name}[prediction]'] = prediction
        self.weather.register_prediction(prediction)
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
