import json
import logging
import os
from datetime import datetime, timezone

from pymongo import MongoClient

_logger = logging.getLogger(__name__)

config_path = os.path.join('config', 'mongodb.json')
with open(config_path, 'r') as file:
    config = json.load(file)

host = config['host'] or 'localhost'
port = config['port'] or 27017
username = config['username']
password = config['password']
database = config['database'] or 'smartpond'
authSource = config['authSource']
authMechanism = config['authMechanism']

client = MongoClient(host, int(port),
                     username=username,
                     password=password,
                     authSource=authSource,
                     authMechanism=authMechanism)
db = client[database]


def save_report(index: int, context, report_id=None):
    col = db['report']
    document = {
        'index': index,
        'type': 'sensor' if report_id is None else 'weather',
        'context': context,
        'reportId': report_id,
        'created': datetime.now(tz=timezone.utc)
    }
    result = col.insert_one(document)
    _logger.info(f'已保存 #{index} 号报告: {result.inserted_id} (ReportId: {report_id})')


def attach_report_id(index: int, report_id):
    col = db['report']
    col.update_one(
        {'index': index},
        {
            '$set': {
                'reportId': report_id,
                'modified': datetime.now(tz=timezone.utc)
            }
        }
    )
    _logger.info(f'已关联 #{index} 号报告的 ReportId: {report_id}')
