from __future__ import annotations

import os

from nxpl.config import read_config, Config

__all__ = [
    "Module",
]


class Module:
    """
    NXPL module.
    """

    @classmethod
    def from_file(cls, file_path: os.PathLike, strict: bool = True) -> Module:
        config = read_config(file_path, strict=strict)
        return cls.from_config(config)

    @classmethod
    def from_config(cls, config: Config, strict: bool = True) -> Module:
        raise NotImplementedError()

    @classmethod
    def to_config(cls) -> Config:
        raise NotImplementedError()
