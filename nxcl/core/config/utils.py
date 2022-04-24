from os import PathLike
from pathlib import Path

import yaml

from .base import ConfigDict
from .yaml import NXCLLoader, NXCLDumper


__all__ = [
    "load_config",
    "save_config",
]


# TODOs
# - Support stream as file input.


def load_config(file: PathLike, Loader=NXCLLoader):
    """
    Load config from file.
    """

    path = Path(file).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    with path.open("r") as f:
        return yaml.load(f, Loader=Loader)


def save_config(config: ConfigDict, file: PathLike, Dumper=NXCLDumper, **yaml_kwargs):
    """
    Save config to file.
    """

    yaml_kwargs.setdefault("sort_keys", False)

    path = Path(file).expanduser()

    with path.open("w") as f:
        yaml.dump(config, f, Dumper=Dumper, **yaml_kwargs)
