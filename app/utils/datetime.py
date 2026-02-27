# coding: utf-8

from datetime import datetime, timezone


def utcnow() -> datetime:
    """
    Return current UTC datetime
    """
    return datetime.now(tz=timezone.utc)
