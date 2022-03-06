from argparse import Action

from nxpl.core.config import ConfigDict


__all__ = [
    "ConfigAction",
]


class ConfigAction(Action):
    def __init__(
        self,
        option_strings,
        dest,
        nargs=None,
        const=None,
        default=None,
        type=None,
        choices=None,
        required=False,
        help=None,
        metavar=None,
    ):
        super().__init__(option_strings, dest)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
