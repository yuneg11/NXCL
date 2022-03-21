from typing import TYPE_CHECKING

from nxcl import core

if TYPE_CHECKING:
    from nxcl import cli
    from nxcl import config
    from nxcl import utils
else:
    cli    = core.misc.ModuleWrapper("nxcl.cli")
    config = core.misc.ModuleWrapper("nxcl.config")
    utils  = core.misc.ModuleWrapper("nxcl.utils")


__version__ = "0.0.2"
