from typing import TYPE_CHECKING

from . import core
from .core.misc import LazyModule

if TYPE_CHECKING:
    # from . import cli
    from . import config
    from . import logging
    from . import rich
    from . import utils
    from . import experimental
else:
    # cli = LazyModule("nxcl.cli")
    config = LazyModule("nxcl.config")
    logging = LazyModule("nxcl.logging")
    rich = LazyModule("nxcl.rich")
    utils = LazyModule("nxcl.utils")
    experimental = LazyModule("nxcl.experimental")


__all__ = [
    "core",
    # "cli",
    "config",
    "logging",
    "rich",
    "utils",
    "experimental",
]

__version__ = "0.0.3.dev3"
