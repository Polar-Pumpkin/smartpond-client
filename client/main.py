import logging.config
import os
import sys

import yaml
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from client.network import Client, Backend
from client.ui import MainWindow

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def main():
    logger = logging.getLogger(__name__)
    with open('logging.yml', 'r') as config:
        os.makedirs('../logs', exist_ok=True)
        logging.config.dictConfig(yaml.load(config, Loader))
        logger.info('已加载日志配置文件')

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.exception('Uncaught exception', exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

    # log.info('检查依赖库可用性')
    # try:
    #     subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    # except CalledProcessError as ex:
    #     log.exception('依赖库检查失败', exc_info=ex)

    # TODO Application Entry point
    logger.info('正在启动窗体')
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')

    window = MainWindow()
    window.showMaximized()
    code = app.exec_()
    logger.info('窗体已停止运行')
    Backend().stop()
    Client().stop(reason='Exit').result()
    logger.info('连接已停止')
    sys.exit(code)


if __name__ == '__main__':
    main()
