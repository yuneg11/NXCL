from typing import TYPE_CHECKING

from . import core
from .core.misc import LazyModule

if TYPE_CHECKING:
    # from . import cli
    from . import config
    from . import logging
    from . import rich
    from . import utils
    from . import dev
    from . import experimental   # deprecated
else:
    # cli = LazyModule(".cli", "cli", globals(), __package__)
    config = LazyModule(".config", "config", globals(), __package__)
    logging = LazyModule(".logging", "logging", globals(), __package__)
    rich = LazyModule(".rich", "rich", globals(), __package__)
    utils = LazyModule(".utils", "utils", globals(), __package__)
    dev = LazyModule(".dev", "dev", globals(), __package__)
    experimental = LazyModule(".experimental", "experimental", globals(), __package__)  # deprecated


__all__ = [
    "core",
    # "cli",
    "config",
    "logging",
    "rich",
    "utils",
    "dev",
    "experimental",  # deprecated
]

__version__ = "0.0.4"
