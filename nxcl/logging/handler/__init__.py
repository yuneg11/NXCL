from typing import TYPE_CHECKING

from nxcl.core.misc.module import LazyObject

if TYPE_CHECKING:
    from .rich import RichHandler, RichFileHandler
    from .tqdm import TqdmHandler
else:
    RichHandler     = LazyObject("RichHandler",     "nxcl.logging.handler.rich")
    RichFileHandler = LazyObject("RichFileHandler", "nxcl.logging.handler.rich")
    TqdmHandler     = LazyObject("TqdmHandler",     "nxcl.logging.handler.tqdm")


__all__ = [
    "RichHandler",
    "RichFileHandler",
    "TqdmHandler",
]
