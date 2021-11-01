import os
from typing import Any

import yaml
from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import Parser
from yaml.composer import Composer
from yaml.constructor import Constructor, SafeConstructor, FullConstructor
from yaml.resolver import Resolver
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.representer import Representer, SafeRepresenter
from yaml.resolver import Resolver

from nxpl.core.typing import PathLike
from nxpl.config.base import Config, ModuleConfig, BuilderConfig

__all__ = [
    "read_config",
    "write_config",
    "merge_configs",
]


DefaultConstructor = SafeConstructor
DefaultRepresenter = SafeRepresenter


class NXPLConstructor(DefaultConstructor):
    def construct_yaml_map(self, node):
        data = Config()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_nxpl_module_map(self, node):
        data = ModuleConfig()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_nxpl_builder_map(self, node):
        data = BuilderConfig()
        yield data
        value = self.construct_mapping(node)
        data.update(value)


NXPLConstructor.add_constructor("tag:yaml.org,2002:map", NXPLConstructor.construct_yaml_map)
NXPLConstructor.add_constructor(Config.yaml_tag, NXPLConstructor.construct_yaml_map)
NXPLConstructor.add_constructor(ModuleConfig.yaml_tag, NXPLConstructor.construct_nxpl_module_map)
NXPLConstructor.add_constructor(BuilderConfig.yaml_tag, NXPLConstructor.construct_nxpl_builder_map)


class NXPLLoader(Reader, Scanner, Parser, Composer, NXPLConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        NXPLConstructor.__init__(self)
        Resolver.__init__(self)


# class NXPLRepresenter(DefaultRepresenter):
#     pass


# class NXPLDumper(Emitter, Serializer, NXPLRepresenter, Resolver):
#     pass


NXPLDumper = yaml.SafeDumper


def read_config(file_path: PathLike) -> Any:
    """
    Reads a configuration file and returns a Config.

    :param file_path: Path to the configuration file.
    :return: Config object.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    try:
        with open(file_path, "r") as file:
            config = yaml.load(file, Loader=NXPLLoader)
        return config
    except yaml.YAMLError as e:
        print(f"Error in configuration file: '{file_path}'")
        print(e)


def write_config(config: Config, file_path: PathLike, makedirs: bool = True, **yaml_kwargs) -> None:
    """
    Writes a configuration file from a Config.

    :param config: Config object.
    :param file_path: Path to the configuration file.
    :param makedirs: Whether to create the directory if it does not exist.
    :param yaml_kwargs: Keyword arguments to pass to yaml.dump.
    """
    file_dir = os.path.dirname(file_path)

    if not os.path.exists(file_dir):
        if makedirs:
            os.makedirs(file_dir, exist_ok=True)
        else:
            raise FileNotFoundError(f"Directory not found: {file_dir}")

    try:
        with open(file_path, "w") as file:
            yaml.dump(config, file, Dumper=NXPLDumper, **yaml_kwargs)
    except yaml.YAMLError as e:
        print(f"Error in configuration file: '{file_path}'")
        print(e)


def merge_configs(*configs) -> Config:
    """
    Merges multiple Configs into a single Config.

    :param configs: Config objects to merge.
    :return: Merged Config.
    """
    config = configs[0].__class__()
    for c in configs:
        config.update(c)
    return config
