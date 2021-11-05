from typing import Optional
from pathlib import Path

from nxpl.config.base import Config
from nxpl.config.utils import read_config


__all__ = ["get_default"]


# Config paths

_nxpl_path: Path = Path(__file__).absolute().parent.parent.joinpath("default.yaml")

_home_path: Path = Path.home()
_home_nxplrc_path: Path = _home_path.joinpath(".nxplrc")
_home_nxplrc_yaml_path: Path = _home_path.joinpath(".nxplrc.yaml")

_project_path: Path = Path.cwd()
_project_nxplrc_path: Path = _project_path.joinpath(".nxplrc")
_project_nxplrc_yaml_path: Path = _project_path.joinpath(".nxplrc.yaml")

# Load default configs

_DEFAULT_CONFIG: Config = read_config(_nxpl_path)

if _home_nxplrc_path.exists():
    _HOME_NXPL_CONFIG: Config = read_config(_home_nxplrc_path)
    _DEFAULT_CONFIG.update(_HOME_NXPL_CONFIG)
elif _home_nxplrc_yaml_path.exists():
    _HOME_NXPL_CONFIG: Config = read_config(_home_nxplrc_yaml_path)
    _DEFAULT_CONFIG.update(_HOME_NXPL_CONFIG)

if _project_nxplrc_path.exists():
    _PROJECT_NXPL_CONFIG: Config = read_config(_project_nxplrc_path)
    _DEFAULT_CONFIG.update(_PROJECT_NXPL_CONFIG)
elif _project_nxplrc_yaml_path.exists():
    _PROJECT_NXPL_CONFIG: Config = read_config(_project_nxplrc_yaml_path)
    _DEFAULT_CONFIG.update(_PROJECT_NXPL_CONFIG)


# Functions


def get_default(key: Optional[str] = None) -> Config:
    if key is None:
        return _DEFAULT_CONFIG
    else:
        current_config = _DEFAULT_CONFIG
        for sub_key in key.split("."):
            current_config = current_config[sub_key]
        return current_config
