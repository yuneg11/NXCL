import sys
from typing import Optional


class Logger:
    def init(
        self,
        project: str,
        name: str,
        id: Optional[str] = None,
    ):
        """
        Args: TODO
        """

        mods = sys.modules
        if mods.get("tqdm"):
            pass

        pass

    def finish(self):
        pass
