from __future__ import annotations

from typing import Any, Dict, Tuple, Iterator


__all__ = [
    "Config",
]


class AttrDict(dict):
    def __getattr__(self, name: str) -> Any:
        if name in self:
            return self.__getitem__(name)
        else:
            raise AttributeError(f"No attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        self.__setitem__(name, value)

    def __delattr__(self, name: str) -> None:
        self.__delitem__(name)


class Config(AttrDict):
    yaml_tag = "!nxpl"

    @classmethod
    def from_yaml(cls, loader, node) -> Config:
        data = loader.construct_mapping(node)

        if not isinstance(data, dict):
            raise TypeError(f"NXPL config should be dict, not {type(data)}")

        return Config(**data)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_mapping(cls.yaml_tag, data)
