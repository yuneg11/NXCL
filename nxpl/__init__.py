from typing import TYPE_CHECKING

from nxpl import core

if TYPE_CHECKING:
    from nxpl import config
else:
    config = core.misc.ModuleWrapper("nxpl.config")


__version__ = "0.0.2"
