# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base

from fastapi_oauth2_service.db.sqlalchemy_engine import engine
from fastapi_oauth2_service.db.sqlalchemy_session import SessionLocal
from fastapi_oauth2_service.db.sqlalchemy_session import get_db


__all__ = [
    'engine',
    'SessionLocal',
    'Base',
    'get_db',
]

Base = declarative_base()
