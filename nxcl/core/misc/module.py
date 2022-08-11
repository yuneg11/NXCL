# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


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

    def __init__(
        self,
        module_name: str,
        local_module_name: str,
        parent_globals: dict[str, Any],
        base_package: Optional[str] = None,
        doc: Optional[str] = None,
    ):
        super().__init__(name=module_name, doc=doc)
        self._package = base_package
        self._local_module_name = local_module_name
        self._parent_globals = parent_globals

    def _load(self) -> ModuleType:
        module = import_module(name=self.__name__, package=self._package)
        self._parent_globals[self._local_module_name] = module
        self.__dict__.update(module.__dict__)
        return module

    def __dir__(self) -> Iterable[str]:
        module = self._load()
        return dir(module)

    def __getattr__(self, name: str) -> Any:
        module = self._load()
        return getattr(module, name)


class LazyObject(object):
    """
    A wrapper for object that delays the import until it is needed
    """

    def __init__(
        self,
        object_name: str,
        module_name: str,
        local_module_name: str,
        parent_globals: dict[str, Any],
        base_package: Optional[str] = None,
        doc: Optional[str] = None,
    ):
        self._module = LazyModule(
            module_name=module_name,
            local_module_name=local_module_name,
            parent_globals=parent_globals,
            base_package=base_package,
            doc=doc,
        )
        self._object_name = object_name

    def _load(self) -> Any:
        module = self._module._load()
        obj = getattr(module, self._object_name)
        self.__dict__.update(obj.__dict__)
        return obj

    def __dir__(self) -> Iterable[str]:
        obj = self._load()
        return dir(obj)

    def __getattr__(self, name: str) -> Any:
        obj = self._load()
        return getattr(obj, name)

    def __call__(self, *args, **kwargs):
        return self._load()(*args, **kwargs)
