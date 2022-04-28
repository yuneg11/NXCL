from pathlib import Path

import yaml
from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import Parser
from yaml.composer import Composer
from yaml.constructor import (
    BaseConstructor,
    SafeConstructor,
    FullConstructor,
    Constructor,
    ConstructorError,
)
from yaml.resolver import Resolver
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.representer import (
    BaseRepresenter,
    SafeRepresenter,
    Representer,
)
from yaml.resolver import Resolver

from .base import ConfigDict


__all__ = [
    "NXCLSafeConstructor",
    "NXCLFullConstructor",
    "NXCLConstructor",
    "NXCLSafeLoader",
    "NXCLFullLoader",
    "NXCLLoader",
    "NXCLSafeRepresenter",
    "NXCLRepresenter",
    "NXCLSafeDumper",
    "NXCLDumper",
    "add_constructor",
    "add_multi_constructor",
    "add_representer",
    "add_multi_representer",
]


_TEMP_PATHS = {
    "@": "./configs/",
}

YAML_TAG_MAP = "tag:yaml.org,2002:map"
YAML_TAG_INCLUDE = u"!include"
YAML_TAG_PYTHON_NAME_ALIAS = u"!name:"
YAML_TAG_PYTHON_OBJECT_ALIAS = u"!object:"
YAML_TAG_PYTHON_OBJECT_NEW_ALIAS = u"!object/new:"
YAML_TAG_PYTHON_OBJECT_APPLY_ALIAS = u"!object/apply:"


class NXCLConstructorMixin(BaseConstructor):
    def construct_yaml_map(self, node):
        data = ConfigDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    # TODO: As a prototype, the implementation just loads the include file using the default loader.
    #       But this approach does not support yaml operations (i.e. anchors, references, etc.) in
    #       the include file. In the future, we need to implement a custom constructor to support
    #       load the include yaml file as a node. Check below:
    #           - https://realpython.com/python-yaml/#parse-a-stream-of-events
    #           - https://pyyaml.org/wiki/PyYAMLDocumentation
    #           - https://pyyaml.docsforge.com
    #       Further, we need to support custom path aliases when NXCL supports global config storage.
    def construct_yaml_include(self, node):
        if not isinstance(node, yaml.ScalarNode):
            raise ConstructorError("value of include must be a string")

        path = str(node.value)
        for symbol, value in _TEMP_PATHS.items():
            path = path.replace(symbol, value)
        path = Path(path).expanduser()

        if not path.exists():
            raise FileNotFoundError(f"include file not found: {path}")

        with path.open("r") as f:
            return yaml.load(f, Loader=self.__class__)
            # return yaml.compose(f, Loader=self.__class__)

    # def construct_yaml_multi_map(self, tag_suffix, node):
    #     print(node.tag, tag_suffix)
    #     data = ConfigDict()
    #     yield data
    #     value = self.construct_mapping(node)
    #     data.update(value)


class NXCLSafeConstructor(SafeConstructor, NXCLConstructorMixin):
    pass


class NXCLFullConstructor(FullConstructor, NXCLConstructorMixin):
    pass


class NXCLConstructor(Constructor, NXCLConstructorMixin):
    pass


class NXCLSafeLoader(Reader, Scanner, Parser, Composer, NXCLSafeConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        NXCLSafeConstructor.__init__(self)
        Resolver.__init__(self)


class NXCLFullLoader(Reader, Scanner, Parser, Composer, NXCLFullConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        NXCLFullConstructor.__init__(self)
        Resolver.__init__(self)


class NXCLLoader(Reader, Scanner, Parser, Composer, NXCLConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        NXCLConstructor.__init__(self)
        Resolver.__init__(self)


class NXCLRepresenterMixin(BaseRepresenter):
    def represent_config(self, data):
        return self.represent_mapping(YAML_TAG_MAP, data.to_dict())

    def represent_module(self, data):
        # TODO: Implement this
        raise NotImplementedError
        # return self.represent_scalar("!module:" + data.module_id, data.to_dict())


class NXCLSafeRepresenter(SafeRepresenter, NXCLRepresenterMixin):
    pass


class NXCLRepresenter(Representer, NXCLRepresenterMixin):
    pass


class NXCLSafeDumper(Emitter, Serializer, NXCLSafeRepresenter, Resolver):
    def __init__(
        self, stream, default_style=None, default_flow_style=False, canonical=None,
        indent=None, width=None, allow_unicode=None, line_break=None, encoding=None,
        explicit_start=None, explicit_end=None, version=None, tags=None, sort_keys=True,
    ):
        Emitter.__init__(
            self, stream, canonical=canonical, indent=indent, width=width,
            allow_unicode=allow_unicode, line_break=line_break,
        )
        Serializer.__init__(
            self, encoding=encoding, explicit_start=explicit_start,
            explicit_end=explicit_end, version=version, tags=tags,
        )
        NXCLSafeRepresenter.__init__(
            self, default_style=default_style, default_flow_style=default_flow_style,
            sort_keys=sort_keys,
        )
        Resolver.__init__(self)


class NXCLDumper(Emitter, Serializer, NXCLRepresenter, Resolver):
    def __init__(
        self, stream, default_style=None, default_flow_style=False, canonical=None,
        indent=None, width=None, allow_unicode=None, line_break=None, encoding=None,
        explicit_start=None, explicit_end=None, version=None, tags=None, sort_keys=True,
    ):
        Emitter.__init__(
            self, stream, canonical=canonical, indent=indent, width=width,
            allow_unicode=allow_unicode, line_break=line_break,
        )
        Serializer.__init__(
            self, encoding=encoding, explicit_start=explicit_start,
            explicit_end=explicit_end, version=version, tags=tags,
        )
        NXCLRepresenter.__init__(
            self, default_style=default_style, default_flow_style=default_flow_style,
            sort_keys=sort_keys,
        )
        Resolver.__init__(self)


def add_constructor(tag, constructor, Loader=None):
    """
    Add a constructor for the given tag.
    Constructor is a function that accepts a Loader instance
    and a node object and produces the corresponding Python object.
    """
    if Loader is None:
        NXCLSafeLoader.add_constructor(tag, constructor)
        NXCLFullLoader.add_constructor(tag, constructor)
        NXCLLoader.add_constructor(tag, constructor)
    else:
        Loader.add_constructor(tag, constructor)


def add_multi_constructor(tag_prefix, multi_constructor, Loader=None):
    """
    Add a multi-constructor for the given tag prefix.
    Multi-constructor is called for a node if its tag starts with tag_prefix.
    Multi-constructor accepts a Loader instance, a tag suffix,
    and a node object and produces the corresponding Python object.
    """
    if Loader is None:
        NXCLSafeLoader.add_multi_constructor(tag_prefix, multi_constructor)
        NXCLFullLoader.add_multi_constructor(tag_prefix, multi_constructor)
        NXCLLoader.add_multi_constructor(tag_prefix, multi_constructor)
    else:
        Loader.add_multi_constructor(tag_prefix, multi_constructor)


def add_representer(data_type, representer, Dumper=None):
    """
    Add a representer for the given type.
    Representer is a function accepting a Dumper instance
    and an instance of the given data type
    and producing the corresponding representation node.
    """
    if Dumper is None:
        NXCLSafeDumper.add_representer(data_type, representer)
        NXCLDumper.add_representer(data_type, representer)
    else:
        Dumper.add_representer(data_type, representer)


def add_multi_representer(data_type, multi_representer, Dumper=None):
    """
    Add a representer for the given type.
    Multi-representer is a function accepting a Dumper instance
    and an instance of the given data type or subtype
    and producing the corresponding representation node.
    """
    if Dumper is None:
        NXCLSafeDumper.add_multi_representer(data_type, multi_representer)
        NXCLDumper.add_multi_representer(data_type, multi_representer)
    else:
        Dumper.add_multi_representer(data_type, multi_representer)


# Alias
add_constructor(YAML_TAG_MAP, NXCLConstructorMixin.construct_yaml_map)

NXCLFullConstructor.add_multi_constructor(YAML_TAG_PYTHON_NAME_ALIAS, FullConstructor.construct_python_name)
NXCLFullConstructor.add_multi_constructor(YAML_TAG_PYTHON_OBJECT_ALIAS, FullConstructor.construct_python_object)
NXCLFullConstructor.add_multi_constructor(YAML_TAG_PYTHON_OBJECT_NEW_ALIAS, FullConstructor.construct_python_object_new)
NXCLFullConstructor.add_multi_constructor(YAML_TAG_PYTHON_OBJECT_APPLY_ALIAS, FullConstructor.construct_python_object_apply)

NXCLConstructor.add_multi_constructor(YAML_TAG_PYTHON_NAME_ALIAS, Constructor.construct_python_name)
NXCLConstructor.add_multi_constructor(YAML_TAG_PYTHON_OBJECT_ALIAS, Constructor.construct_python_object)
NXCLConstructor.add_multi_constructor(YAML_TAG_PYTHON_OBJECT_NEW_ALIAS, Constructor.construct_python_object_new)
NXCLConstructor.add_multi_constructor(YAML_TAG_PYTHON_OBJECT_APPLY_ALIAS, Constructor.construct_python_object_apply)

# NXCL extensions
add_constructor(YAML_TAG_INCLUDE, NXCLConstructorMixin.construct_yaml_include)
add_constructor(ConfigDict.yaml_tag, NXCLConstructorMixin.construct_yaml_map)
# add_multi_constructor(ConfigDict.yaml_tag, NXCLConstructorMixin.construct_yaml_multi_map)

add_representer(ConfigDict, NXCLRepresenterMixin.represent_config)
