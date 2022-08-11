from typing import TYPE_CHECKING

from nxcl.core.misc.module import LazyObject

if TYPE_CHECKING:
    from .rich import RichHandler, RichFileHandler
    from .tqdm import TqdmHandler
else:
    RichHandler     = LazyObject("RichHandler",     ".rich", "rich", globals(), __package__)
    RichFileHandler = LazyObject("RichFileHandler", ".rich", "rich", globals(), __package__)
    TqdmHandler     = LazyObject("TqdmHandler",     ".tqdm", "tqdm", globals(), __package__)


__all__ = [
    "RichHandler",
    "RichFileHandler",
    "TqdmHandler",
]
