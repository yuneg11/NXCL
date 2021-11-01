from typing import Callable
from inspect import signature
from functools import update_wrapper


def copy_signature(source: Callable, remove_self: bool = False):
    def copy(target: Callable):
        update_wrapper(target, source)
        sig = signature(source)
        if remove_self:
            parameters = list(sig.parameters.values())
            if parameters[0].name == "self":
                parameters = parameters[1:]
            sig = sig.replace(parameters=parameters)
        target.__signature__ = sig
        return target

    return copy
