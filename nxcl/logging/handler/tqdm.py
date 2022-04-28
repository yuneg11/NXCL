from logging import Handler
from typing import TYPE_CHECKING

from nxcl.core.misc.module import LazyModule

if TYPE_CHECKING:
    from tqdm.auto import tqdm
else:
    tqdm = LazyModule("tqdm.auto.tqdm")


__all__ = [
    "TqdmHandler",
]


class TqdmHandler(Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)
        except (KeyboardInterrupt, SystemExit):
            raise
