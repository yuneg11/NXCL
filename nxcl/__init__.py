from typing import TYPE_CHECKING

from nxcl import core
from nxcl.core.misc import LazyModule

if TYPE_CHECKING:
    from nxcl import cli
    from nxcl import config
    from nxcl import logging
    from nxcl import rich
    from nxcl import utils
else:
    cli     = LazyModule("nxcl.cli")
    config  = LazyModule("nxcl.config")
    logging = LazyModule("nxcl.logging")
    rich    = LazyModule("nxcl.rich")
    utils   = LazyModule("nxcl.utils")


__version__ = "0.0.2"
