import logging

logger = logging.getLogger(__name__)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # sys.__excepthook__(exc_type, exc_value, exc_traceback)
        logger.info('通过 KeyboardInterrupt 退出')
        return
    logger.exception(f'未捕获的异常: {exc_value}', exc_info=(exc_type, exc_value, exc_traceback))
