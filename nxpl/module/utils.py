import re
from typing import Any, Optional

from nxpl.config import Config
from nxpl.module.registers import MODULES


__all__ = [
    "build_module",
]


MODULE_NAME_REGEX = re.compile(
    r"^\@(?P<package>[^/]+)?/(?P<name>[^/:]+(?:/[^/:]+)*)(?:\:(?P<version>.+))?$"
)
MODULE_PATH_REGEX = re.compile(
    r"^(?P<directory>[^:]+(?:/[^/:]+)*):(?P<package>[^.:]+(?:\.[^.:]+)*)(?:\:(?P<module>[^.:]+(?:.[^.:]+)*))?$"
)


def _import_module_by_name(package: str, name: str, version: Optional[str] = None):
    """
    Import a module by name.
    """

    if version is not None:
        raise NotImplementedError("Specifying a version is not yet supported.")

    # if version is None:
    #     module = __import__(package, fromlist=[name])
    # else:
    #     module = __import__(package, fromlist=[name], level=0)
    #     module = getattr(module, name)
    #     module = getattr(module, version)
    # return module


def _import_module_by_path(directory: str, package: str, module: Optional[str] = None):
    """
    Import a module by path.
    """
    # if module is None:
    #     module = __import__(package, fromlist=[directory])
    # else:
    #     module = __import__(package, fromlist=[directory], level=0)
    #     module = getattr(module, directory)
    #     module = getattr(module, module)
    # return module


def _parse_nxpl_id(nxpl_id: str) -> str:
    """
    Parse the nxpl_id and return the module name.

    :param nxpl_id:
    :return:
    """
    name_match = MODULE_NAME_REGEX.fullmatch(nxpl_id)
    if name_match:
        pass  # TODO: Implement module name parsing

    path_match = MODULE_PATH_REGEX.fullmatch(nxpl_id)
    if path_match:
        pass  # TODO: Implement module path parsing


def build_module(nxpl_id: str, config: Config) -> Any:
    """
    Builds a module from the given nxpl_id and config.
    """
    module_path = _parse_nxpl_id(nxpl_id)
