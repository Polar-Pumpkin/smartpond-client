from abc import ABCMeta

from PySide6.QtCore import QObject


class QABCMeta(type(QObject), ABCMeta):
    pass
