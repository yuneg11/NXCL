from nxpl.core.utils import copy_signature
from typing import Optional

from . import base
from . import handler

from .base import Logger


__all__ = []


_ROOT_LOGGER: Optional[Logger] = None


def _get_root_logger():
    global _ROOT_LOGGER
    if _ROOT_LOGGER is None:
        raise RuntimeError("Logger not initialized. You should call nxpl.init() first.")
    return _ROOT_LOGGER


@copy_signature(Logger.init, remove_self=True)
def init(*args, **kwargs):
    global _ROOT_LOGGER
    _ROOT_LOGGER = Logger(*args, **kwargs)
    return _ROOT_LOGGER


@copy_signature(Logger.finish, remove_self=True)
def finish():
    global _ROOT_LOGGER
    _ROOT_LOGGER.finish()
    _ROOT_LOGGER = None
