from datetime import datetime
from typing import Dict, List, Any

from pandas import DataFrame
from sqlalchemy import select

import client.service.mariadb as mariadb
import client.util.weather as weather_util

_datetime_format = '%Y-%m-%d %H:%M'
_keys = ['时间', '温度', '溶解氧', 'pH', '氨氮', '硝氮', '天气状况', '风速', '气温']


def _transform_key(key) -> datetime:
    value = datetime.strftime(key, _datetime_format)
    return datetime.strptime(value, _datetime_format)


def prepare(value: Dict[str, float]) -> List[float]:
    return list(map(lambda key: value.get(key, 0.0), _keys))


def pull(sensor_id: str, amount: int) -> DataFrame:
    # col = mongodb.db['report']
    session = mariadb.Session()
    values: Dict[datetime, Dict[str, float]] = {}

    sensors: Dict[datetime, Dict[str, float]] = {}
    # for sensor in col.find({'type': 'sensor'}).sort({'created': -1}).limit(amount):
    #     key = _transform_key(sensor['created'])
    #     sensors[key] = sensor['context']['fields']
    statement = (
        select(mariadb.Report)
        .where(mariadb.Report.sensor_id == sensor_id)
        .order_by(mariadb.Report.created.desc())
        .limit(amount)
    )
    for sensor in session.execute(statement).scalars():
        key = _transform_key(sensor.created)
        sensors[key] = sensor.context['fields']

    weathers: Dict[datetime, Dict[str, float]] = {}
    # for weather in col.find({'type': 'weather'}).sort({'created': -1}).limit(amount):
    #     key = _transform_key(weather['created'])
    #     weathers[key] = weather_util.extract(weather['context'])
    statement = (
        select(mariadb.Report)
        .where(mariadb.Report.type == 'weather')
        .order_by(mariadb.Report.created.desc())
        .limit(amount)
    )
    for weather in session.execute(statement).scalars():
        key = _transform_key(weather.created)
        weathers[key] = weather_util.extract(weather.context)

    sensors = {key: sensors[key] for key in sorted(sensors)}
    weathers = {key: weathers[key] for key in sorted(weathers)}
    if len(weathers) > 0:
        for sensor_key, sensor in sensors.items():
            value: Dict[str, float] = {}
            value.update(sensor)
            for weather_key, weather in weathers.items():
                if sensor_key > weather_key:
                    value.update(weather)
            if len(value) > 0:
                value.update(list(weathers.values())[-1])
            values[sensor_key] = value

    frame = []
    for key, elements in values.items():
        row: Dict[str, Any] = {'时间': key}
        row.update(elements)
        frame.append(row)
        # frame.append(key)
        # frame += prepare(row)
    frame = DataFrame(frame)
    if '溶解氧' in frame.columns:
        frame['溶解氧'] = frame['溶解氧'].fillna(0.0)
    return frame
