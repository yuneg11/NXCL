from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import Parser
from yaml.composer import Composer
from yaml.constructor import BaseConstructor, SafeConstructor, FullConstructor, Constructor
from yaml.resolver import Resolver
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.representer import BaseRepresenter, SafeRepresenter, Representer
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


YAML_TAG_MAP = "tag:yaml.org,2002:map"


class NXCLConstructorMixin(BaseConstructor):
    def construct_yaml_map(self, node):
        data = ConfigDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

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

    def represent_block(self, data):
        # TODO: Implement this
        raise NotImplementedError
        return self.represent_scalar("!block:" + data.block_id, data.to_dict())


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


add_constructor(YAML_TAG_MAP, NXCLConstructorMixin.construct_yaml_map)
add_constructor(ConfigDict.yaml_tag, NXCLConstructorMixin.construct_yaml_map)
# add_multi_constructor(ConfigDict.yaml_tag + u":", NXCLConstructorMixin.construct_yaml_multi_map)

add_representer(ConfigDict, NXCLRepresenterMixin.represent_config)
