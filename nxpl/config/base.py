from __future__ import annotations

from typing import Any, Union


__all__ = [
    "AttrDict",
    "Config",
    "ModuleConfig",
    "BuilderConfig",
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
    yaml_tag = "!nxpl-config"  # Automatically loaded by YAML. Do not needed.

    @classmethod
    def from_yaml(cls, loader, node) -> Config:
        data = loader.construct_mapping(node)

        if not isinstance(data, dict):
            raise TypeError(f"NXPL config should be dict, not {type(data)}")

        return Config(**data)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_mapping(cls.yaml_tag, data)

    def update(self, other: Union[dict, AttrDict]) -> None:
        for key, value in other.items():
            if key in self:
                old_value = self[key]
                if isinstance(old_value, Config):
                    old_value.update(value)
                else:
                    if isinstance(value, dict):
                        value = Config(**value)
                    self[key] = value
            else:
                if isinstance(value, dict):
                    value = Config(**value)
                self[key] = value

    def __repr__(self) -> str:
        # TODO: Improve representation
        kv_reprs = [f"'{k}': {repr(v)}" for k, v in self.items()]
        return f"{self.__class__.__name__}({', '.join(kv_reprs)})"


class ModuleConfig(Config):
    yaml_tag = "!nxpl-module"

    def __init__(self, nxpl_id: str = "nxpl:none", **kwargs):
        if nxpl_id is None:
            raise ValueError("ModuleConfig requires 'nxpl_id'")
        super().__init__(nxpl_id=nxpl_id, **kwargs)


class BuilderConfig(Config):
    yaml_tag = "!nxpl-builder"

    def __init__(self, nxpl_id: str = "nxpl:none", **kwargs):
        if nxpl_id is None:
            raise ValueError("BuilderConfig requires 'nxpl_id'")
        super().__init__(nxpl_id=nxpl_id, **kwargs)
