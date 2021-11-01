from __future__ import annotations

from nxpl.config import (
    read_config,
    Config,
)
from nxpl.core.typing import PathLike

__all__ = [
    "Module",
]


class Module:
    """
    NXPL module.
    """

    @classmethod
    def from_file(cls, file_path: PathLike, strict: bool = True) -> Module:
        config = read_config(file_path, strict=strict)
        return cls.from_config(config)

    @classmethod
    def from_config(cls, config: Config, strict: bool = True) -> Module:
        raise NotImplementedError()

    @classmethod
    def to_config(cls) -> Config:
        raise NotImplementedError()
