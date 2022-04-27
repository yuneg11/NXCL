from __future__ import annotations

from typing import Iterable, Any, List, Tuple, Union

from textwrap import indent
from contextlib import contextmanager
from collections.abc import Mapping


__all__ = [
    "ConfigDict",
]


SEPERATOR = "."


# TODOs
# - Type checking of values using ConfigValue
# - Freezing of ConfigDict with FrozenConfigDict
# - Reference values


def is_valid_key(key) -> bool:
    if not isinstance(key, str):
        return False
    elif len(key) == 0:
        return False
    elif key[0].isdigit():
        return False
    elif " " in key:
        return False
    else:
        return True


def is_atomic_key(key: str) -> bool:
    return SEPERATOR not in key


def tokenize_key(key: str) -> List[str]:
    return key.split(SEPERATOR)


class ConfigDict(dict):
    """
    ConfigDict
    """

    yaml_tag = u"!config"

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        super(ConfigDict, obj).__setattr__("__children", {})
        super(ConfigDict, obj).__setattr__("__locked", False)
        return obj

    # TODO: support iterable as args
    def __init__(
        self,
        *args,
        convert_mapping: bool = True,
        lock: bool = False,
        **kwargs,
    ):
        super().__init__()

        # self.__super_setattr("children", {})
        # self.__super_setattr("locked", False)

        for arg in args:
            if isinstance(arg, Mapping):
                for key in arg:
                    self.__set_value(key, arg[key], convert_mapping=convert_mapping)
            else:
                raise TypeError(f"ConfigDict only accepts Mapping as arguments, not {type(arg)}.")

        for key, value in kwargs.items():
            self.__set_value(key, value, convert_mapping=convert_mapping)

        self.lock(mode=lock)

    def __super_getattr(self, key):
        return super(ConfigDict, self).__getattribute__("__" + key)

    def __super_setattr(self, key, value):
        super(ConfigDict, self).__setattr__("__" + key, value)

    def __convert_value(self, value: Any, convert_mapping: bool = True) -> Any:
        if isinstance(value, ConfigDict):
            return value
        elif convert_mapping and isinstance(value, Mapping):
            return ConfigDict(value)
        else:
            return value

    def __get_child(self, atomic_key: str) -> Any:
        # if not is_atomic_key(atomic_key):
        #     raise KeyError(f"Invalid atomic key '{atomic_key}'")

        if super().__contains__(atomic_key):
            return super().__getitem__(atomic_key)
        else:
            raise KeyError(f"'{atomic_key}' not found.")

    def __set_child(self, atomic_key: str, value: Any, convert_mapping: bool = True):
        # if not is_atomic_key(atomic_key):
        #     raise KeyError(f"Invalid atomic key '{atomic_key}'")

        if self.is_locked() and not super().__contains__(atomic_key):
            raise RuntimeError(f"Cannot add '{atomic_key}' in locked ConfigDict.")

        value = self.__convert_value(value, convert_mapping=convert_mapping)
        if isinstance(value, ConfigDict):
            self.__super_getattr("children")[atomic_key] = value
        else:
            self.__super_getattr("children").pop(atomic_key, None)
        super().__setitem__(atomic_key, value)
        return value

    def __del_child(self, atomic_key: str):
        # if not is_atomic_key(atomic_key):
        #     raise KeyError(f"Invalid atomic key '{atomic_key}'")

        if self.is_locked():
            raise RuntimeError(f"Cannot delete '{atomic_key}' in locked ConfigDict.")

        if super().__contains__(atomic_key):
            self.__super_getattr("children").pop(atomic_key, None)
            super().__delitem__(atomic_key)
        else:
            raise KeyError(f"'{atomic_key}' not found.")

    def __iter_children(self, recursive: bool = False) -> Tuple[str, Any]:
        for key, value in self.__super_getattr("children").items():
            if recursive:
                for subkey, subvalue in value.__iter_children(recursive=recursive):
                    yield SEPERATOR.join([key, subkey]), subvalue
            else:
                yield key, value

    def __iter_items(self, recursive: bool = False) -> Tuple[str, Any]:
        for key, value in super().items():
            if recursive and isinstance(value, ConfigDict):
                for subkey, subvalue in value.__iter_items(recursive=recursive):
                    yield SEPERATOR.join([key, subkey]), subvalue
            else:
                yield key, value

    def __get_penultimate(
        self,
        key: str,
        create_if_not_exist: bool = False,
        none_if_not_exist: bool = False,
    ) -> Union[Tuple[ConfigDict, str], None]:
        if not is_valid_key(key):
            raise KeyError(f"Invalid key '{key}'")

        sub_keys = tokenize_key(key)
        cursor = self

        for idx, sub_key in enumerate(sub_keys[:-1]):
            if not isinstance(cursor, ConfigDict):
                cur_key = SEPERATOR.join(sub_key[:idx])
                raise KeyError(f"Invalid key '{key}': '{cur_key}' is not a ConfigDict.")
            elif not super(ConfigDict, cursor).__contains__(sub_key):
                if create_if_not_exist:
                    cursor = cursor.__set_child(sub_key, ConfigDict())
                elif none_if_not_exist:
                    return None
                else:
                    cur_key = SEPERATOR.join(sub_key[:idx])
                    raise KeyError(f"Invalid key '{key}': '{cur_key}' not found.")
            else:
                cursor = super(ConfigDict, cursor).__getitem__(sub_key)

        return cursor, sub_keys[-1]

    def __get_value(self, key: str) -> Any:
        pen_node, pen_key = self.__get_penultimate(key)
        return pen_node.__get_child(pen_key)

    def __set_value(self, key: str, value: Any, convert_mapping: bool = True):
        pen_node, pen_key = self.__get_penultimate(key, create_if_not_exist=True)
        return pen_node.__set_child(pen_key, value, convert_mapping=convert_mapping)

    def __del_value(self, key: str):
        pen_node, pen_key = self.__get_penultimate(key)
        pen_node.__del_child(pen_key)

    def lock(self, mode: bool = True):
        if mode is True or mode is False:
            self.__super_setattr("locked", mode)
            for _, child in self.__iter_children():
                child.lock(mode=mode)
        else:
            raise ValueError(f"Invalid lock mode '{mode}'")
        return self

    def unlock(self):
        return self.lock(mode=False)

    def is_locked(self) -> bool:
        return self.__super_getattr("locked")

    @contextmanager
    def locked(self, mode=True):
        prev_mode = self.is_locked()
        if prev_mode != mode:
            self.lock(mode=mode)
        yield self
        if prev_mode != mode:
            self.lock(mode=prev_mode)

    def unlocked(self):
        return self.locked(mode=False)

    def __getitem__(self, key: str):
        return self.__get_value(key)

    def __getattr__(self, key: str):
        return self.__get_child(key)

    def __setitem__(self, key: str, value: Any):
        try:
            self.__set_value(key, value)
        except:
            print(key, super().__dir__())
            raise

    def __setattr__(self, key: str, value: Any):
        self.__set_child(key, value)

    def __delitem__(self, key: str):
        if self.is_locked():
            raise RuntimeError(f"Cannot delete '{key}' in locked ConfigDict.")

        self.__del_value(key)

    def __delattr__(self, key: str):
        if self.is_locked():
            raise RuntimeError(f"Cannot delete '{key}' in locked ConfigDict.")

        self.__del_child(key)

    def __contains__(self, key: str) -> bool:
        pen = self.__get_penultimate(key, none_if_not_exist=True)
        if pen is None:
            return False
        else:
            pen_node, pen_key = pen
            return super(ConfigDict, pen_node).__contains__(pen_key)

    def __repr__(self):
        kvs = []
        for key, value in self.__iter_items(recursive=True):
            kvs.append(f"'{key}': {value}")
        return "ConfigDict({" + ", ".join(kvs) + "})"

    def __str__(self):
        lines = []
        for key, value in self.__iter_items(recursive=True):
            lines.append(indent(f"{key}: {value},", " " * 4))
        if lines:
            return "\n".join(["ConfigDict({"] + lines + ["})"])
        else:
            return "ConfigDict({})"

    def __getstate__(self):
        state = {
            "__locked": self.__super_getattr("locked"),
            "__dict__": self.to_dict(),
        }
        return state

    def __setstate__(self, state):
        self.__super_setattr("children", {})
        self.__super_setattr("locked", False)
        self.update(state["__dict__"])

        if state["__locked"] is True:
            self.lock()

    def __iter__(self):
        for key, _ in self.__iter_items():
            yield key

    # TODO: Change implementation from list to dictview

    def keys(self, flatten: bool = False) -> Iterable[str]:
        return list(k for k, _ in self.__iter_items(recursive=flatten))

    def values(self, flatten: bool = False) -> Iterable[Any]:
        return list(v for _, v in self.__iter_items(recursive=flatten))

    def items(self, flatten: bool = False) -> Iterable[Tuple[str, Any]]:
        return list((k, v) for k, v in self.__iter_items(recursive=flatten))

    def get(self, key: str, default: Any = None) -> Any:
        if key in self:
            return self.__get_value(key)
        else:
            return default

    def pop(self, key: str, default: Any = None) -> Any:
        if self.is_locked():
            raise RuntimeError(f"Cannot pop '{key}' from locked ConfigDict.")

        if key in self:
            value = self.__get_value(key)
            self.__del_value(key)
            return value
        else:
            return default

    def clear(self):
        if self.is_locked():
            raise RuntimeError(f"Cannot clear locked ConfigDict.")

        super().clear()
        self.__super_getattr("children").clear()

    def popitem(self) -> tuple[str, Any]:
        if self.is_locked():
            raise RuntimeError(f"Cannot popitem from locked ConfigDict.")

        key, value = super().popitem()
        if isinstance(value, ConfigDict):
            self.__super_getattr("children").pop(key)
        return key, value

    def setdefault(self, key: str, default: Any) -> Any:
        if key not in self:
            return self.__set_value(key, default)
        else:
            return self.__get_value(key)

    # TODO: Same as __init__, support iterable as args
    def update(self, *args, convert_mapping: bool = True, **kwargs):
        for arg in args:
            if isinstance(arg, Mapping):
                for key in arg:
                    self.__set_value(key, arg[key], convert_mapping=convert_mapping)
            else:
                raise TypeError(f"ConfigDict only accepts Mapping as arguments, not {type(arg)}.")

        for key, value in kwargs.items():
            self.__set_value(key, value, convert_mapping=convert_mapping)

    @classmethod
    def fromkeys(cls, keys: Iterable[str], value: Any = None) -> ConfigDict:
        return ConfigDict(dict.fromkeys(keys, value))

    # FIXME: Improve this implementation
    def copy(self, recursive: bool = False) -> ConfigDict:
        kvs = dict(self.__iter_items(recursive=recursive))
        return ConfigDict(**kvs).lock(mode=self.is_locked())

    # TODO: Improve this implementation
    def to_dict(self, flatten: bool = False):
        d = {}
        for key, value in self.__iter_items(recursive=flatten):
            if isinstance(value, ConfigDict):
                d[key] = value.to_dict()
            else:
                d[key] = value
        return d


# Need to implement or check
# - __eq__
# - __format__
# - __ge__
# - __gt__
# - __hash__
# - __ior__
# - __le__
# - __lt__
# - __ne__
# - __or__
# - __ror__
# - __getstate__
# - __setstate__
