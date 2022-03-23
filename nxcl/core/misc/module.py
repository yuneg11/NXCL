import inspect

from types import ModuleType
from typing import Any, Iterable, Optional
from importlib import import_module


__all__ = [
    "LazyModule",
    "LazyObject",
]


class LazyModule(ModuleType):
    """
    A wrapper for modules that delays the import until it is needed
    """

    def __init__(self, name: str, package: Optional[str] = None, doc: Optional[str] = None):
        super().__init__(name=name, doc=doc)
        if self.__doc__ is None:
            self.__doc__ = f"Wrapper of the '{self.__name__}' module"
        self.__package__ = package

    def _load(self):
        return import_module(name=self.__name__, package=self.__package__)

    def __dir__(self) -> Iterable[str]:
        return self._load().__dir__()

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._load(), name)
        if inspect.ismodule(attr):
            attr = LazyModule(attr.__name__)
        return attr


class LazyObject(ModuleType):
    """
    A wrapper for modules that delays the import until it is needed
    """

    def __init__(self, name: str, package: str, doc: Optional[str] = None):
        super().__init__(name=name, doc=doc)
        if self.__doc__ is None:
            self.__doc__ = f"Wrapper of the '{self.__name__}' module"
        self.__package__ = package

    def _load(self):
        return getattr(import_module(name=self.__package__), self.__name__)

    def __dir__(self) -> Iterable[str]:
        return self._load().__dir__()

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._load(), name)
        return attr

    def __call__(self, *args, **kwargs):
        return self._load()(*args, **kwargs)
