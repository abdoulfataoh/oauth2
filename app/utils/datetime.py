# coding: utf-8

from datetime import datetime
from zoneinfo import ZoneInfo

from app import settings


def now():
    """
    Return current time
    based on settings timezone
    """
    return datetime.now(tz=ZoneInfo(settings.TIMEZONE))
