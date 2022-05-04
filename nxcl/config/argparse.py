from typing import Optional
from argparse import SUPPRESS, ArgumentParser, ArgumentTypeError  #, Action

from nxcl.core.config import ConfigDict


__all__ = [
    # "ConfigAction",
    "add_config_arguments",
]


def convert_to_bool(v):
    if isinstance(v, bool):
        return v
    elif isinstance(v, str):
        if v.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif v.lower() in ("no", "false", "f", "n", "0"):
            return False
        else:
            raise ArgumentTypeError("Boolean value expected.")
    else:
        raise ArgumentTypeError("Boolean value expected.")


# class ConfigAction(Action):
#     def __init__(
#         self,
#         option_strings,
#         dest,
#         nargs=None,
#         const=None,
#         default=None,
#         type=None,
#         choices=None,
#         required=False,
#         help=None,
#         metavar=None,
#     ):
#         super().__init__(option_strings, dest)
#
#     def __call__(self, parser, namespace, values, option_string=None):
#         setattr(namespace, self.dest, values)


def add_config_arguments(
    parser: ArgumentParser,
    config: ConfigDict,
    prefix: Optional[str] = None,
    aliases: Optional[dict] = None,
):
    if aliases is None:
        aliases = {}

    for key, value in config.items(flatten=True):
        if key.startswith("_"):
            continue

        key = f"{prefix}.{key}" if prefix else key
        key_flag = f"--{key}"

        if key in aliases:
            alias = aliases[key]
            if isinstance(alias, str):
                flags = [alias, key_flag]
            elif isinstance(alias, (list, tuple)):
                flags = [*alias, key_flag]
            else:
                raise TypeError(f"Invalid alias type: {type(alias)}")
        else:
            flags = [key_flag]

        if isinstance(value, (list, tuple)):
            t = type(value[0]) if value else str
            nargs = "*"
        elif isinstance(value, bool):
            t = convert_to_bool
        else:
            t = type(value)
            nargs = None

        parser.add_argument(
            *flags,
            type=t,
            nargs=nargs,
            default=SUPPRESS,
            metavar=key.split(".")[-1].upper(),
            dest=key,
            help=f"Default: {value}",
        )
