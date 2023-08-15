import json
import logging
import os
from typing import Dict, Any, Optional

from sqlalchemy import create_engine, Column, BigInteger, String, JSON, DateTime, update
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

_logger = logging.getLogger(__name__)
Entity = declarative_base()


class Report(Entity):
    __tablename__ = 'report'
    id = Column(BigInteger, primary_key=True)
    index = Column(BigInteger, nullable=False)
    type = Column(String(length=255), nullable=False)
    context = Column(JSON, nullable=False)
    sensor_id = Column(String(length=255), nullable=True)
    report_id = Column(String(length=24), nullable=True)
    created = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    modified = Column(DateTime, nullable=False, server_default=func.current_timestamp(),
                      onupdate=func.current_timestamp())


config_path = os.path.join('config', 'mariadb.json')
with open(config_path, 'r') as file:
    config = json.load(file)
url = config['url']
database = config['database'] or 'smartpond'
engine = create_engine(url)

with engine.connect() as conn:
    conn.execute('commit')
    conn.execute(f'create database if not exist {database};')
    conn.execute(f'use {database};')

Session = sessionmaker(bind=engine)
Entity.metadata.create_all(engine)


def save_report(index: int, context: Dict[str, Any], sensor_id: Optional[str] = None, report_id: Optional[str] = None):
    session = Session()
    report = Report(index=index,
                    type='sensor' if report_id is None else 'weather',
                    context=context,
                    sensor_id=sensor_id,
                    report_id=report_id)
    session.add(report)
    session.commit()
    _logger.info(f'已保存 #{index} 号报告: {report.id} (ReportId: {report_id})')


def attach_report_id(index: int, report_id: str):
    session = Session()
    statement = (
        update(Report)
        .where(Report.index == index)
        .values(report_id=report_id)
    )
    session.execute(statement)
    session.commit()
    _logger.info(f'已关联 #{index} 号报告的 ReportId: {report_id}')
