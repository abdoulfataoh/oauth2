# coding: utf-8

from datetime import datetime, timezone


def utcnow() -> datetime:
    """
    Return current UTC datetime
    """
    return datetime.now(tz=timezone.utc)


def ensure_utc(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def is_expired(dt):
    dt = ensure_utc(dt)
    return dt < utcnow()
