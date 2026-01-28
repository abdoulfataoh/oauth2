# coding: utf-8

import logging
from typing import Callable, Any, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar('T')
R = TypeVar('R')


def trace(f: Callable[..., R]) -> Callable[..., R]:
    def wrapper(*args: T, **kwargs: Any) -> R:
        logger.info(f"[{f.__name__}] call with args={args} kwargs={kwargs}")
        result = f(*args, **kwargs)
        return result
    return wrapper
