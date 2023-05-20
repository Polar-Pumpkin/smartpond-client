import logging.config
import os
import sys
import threading

import qdarktheme
import yaml
from PySide6.QtWidgets import QApplication

from client.util import handle_exception

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def main():
    logger = logging.getLogger(__name__)
    with open('logging.yml', 'r') as config:
        os.makedirs('logs', exist_ok=True)
        logging.config.dictConfig(yaml.load(config, Loader))
        logger.info('已加载日志配置文件')

    sys.excepthook = handle_exception
    # threading.excepthook = handle_exception

    # log.info('检查依赖库可用性')
    # try:
    #     subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    # except CalledProcessError as ex:
    #     log.exception('依赖库检查失败', exc_info=ex)

    # 加载所有 Websocket 数据包
    # noinspection PyUnresolvedReferences
    import client.network.serializable.packet

    logger.info('正在启动窗体')
    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme='dark_blue.xml')
    qdarktheme.setup_theme('auto')

    from client.ui.window import MainWindow
    window = MainWindow()
    window.showMaximized()
    code = app.exec_()
    logger.info('窗体已停止')

    from client.network.backend import Backend
    from client.network.websocket import Client
    Backend().stop()
    Client().stop(reason='Exit').result(1)
    logger.info('连接已停止')

    sys.exit(code)


if __name__ == '__main__':
    main()
