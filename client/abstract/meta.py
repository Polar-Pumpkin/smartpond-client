from abc import ABCMeta

from PySide6.QtCore import QObject
from jsonobject import JsonObject


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class QABCMeta(type(QObject), ABCMeta):
    pass


class JsonABCMeta(type(JsonObject), ABCMeta):
    pass
