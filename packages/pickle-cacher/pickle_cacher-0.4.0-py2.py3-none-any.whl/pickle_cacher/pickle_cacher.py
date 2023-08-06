import gzip
import pickle  # noqa: S403
from abc import ABC
from abc import abstractmethod
from functools import update_wrapper
from hashlib import md5
from inspect import signature
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import FrozenSet
from typing import Generic
from typing import Optional
from typing import overload
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from atomic_write_path import atomic_write_path


Key = Tuple[Tuple, FrozenSet[Tuple[str, Any]]]
T = TypeVar("T")


class cached(Generic[T]):  # noqa: N801
    """Decorator for methods of the the pickling class."""

    def __init__(self: "cached[T]", func: Callable[..., T]) -> None:
        self.func = func
        self.signature = signature(func)
        self.full_cache: Dict["PickleCacher", Dict[Key, T]] = {}

    @overload
    def __get__(  # noqa: U100
        self: "cached[T]", instance: None, owner: Type["PickleCacher"],
    ) -> "cached[T]":
        pass

    @overload
    def __get__(  # noqa: F811, U100
        self: "cached[T]", instance: "PickleCacher", owner: Type["PickleCacher"],
    ) -> "_CachedPartial[T]":
        pass

    def __get__(  # noqa: F811, U100
        self: "cached[T]", instance: Optional["PickleCacher"], owner: Type["PickleCacher"],
    ) -> Union["cached[T]", "_CachedPartial[T]"]:
        if instance is None:
            return self
        else:
            return _CachedPartial(decorator=self, instance=instance)


class _CachedPartial(Generic[T]):
    def __init__(
        self: "_CachedPartial[T]", decorator: "cached[T]", instance: "PickleCacher",
    ) -> None:
        self.decorator = decorator
        self.instance = instance
        try:
            self.cache = decorator.full_cache[instance]
        except KeyError:
            decorator.full_cache[instance] = {}
            self.cache = decorator.full_cache[instance]
        update_wrapper(self, self.decorator.func)

    def __call__(
        self: "_CachedPartial[T]", *args: Any, overwrite: bool = False, **kwargs: Any,
    ) -> T:
        if overwrite:
            return self._call_and_persist(*args, overwrite=overwrite, **kwargs)
        else:
            key = self._get_key(*args, **kwargs)
            try:
                return self.cache[key]
            except KeyError:
                path = self._get_path(key)
                try:
                    with gzip.open(str(path), mode="rb") as fh:
                        output = self.cache[key] = pickle.loads(fh.read())  # noqa: S301
                except FileNotFoundError:
                    return self._call_and_persist(*args, overwrite=overwrite, **kwargs)
                else:
                    return output

    def _get_key(self: "_CachedPartial[T]", *args: Any, **kwargs: Any) -> Key:
        bound_args = self.decorator.signature.bind(self.instance, *args, **kwargs)
        bound_args.apply_defaults()
        return (
            bound_args.args[1:],
            frozenset(bound_args.kwargs.items()),
        )

    def _get_path(self: "_CachedPartial[T]", key: Key) -> Path:
        return self.instance.path.joinpath(
            self.decorator.func.__name__, md5(pickle.dumps(key)).hexdigest(),  # noqa: S303
        )

    def _call_and_persist(
        self: "_CachedPartial[T]", *args: Any, overwrite: bool = False, **kwargs: Any,
    ) -> T:
        key = self._get_key(*args, **kwargs)
        output = self.cache[key] = self.decorator.func(self.instance, *args, **kwargs)
        path = self._get_path(key)
        with atomic_write_path(path, overwrite=overwrite) as temp:
            with gzip.open(temp, mode="wb") as fh:
                fh.write(pickle.dumps(output))
        return output


class PickleCacher(ABC):
    """Pickling class."""

    @abstractmethod
    def __eq__(self: "PickleCacher", other: Any) -> bool:  # noqa: U100
        pass

    @abstractmethod
    def __hash__(self: "PickleCacher") -> int:
        pass

    @property
    @abstractmethod
    def path(self: "PickleCacher") -> Path:
        """Get the path associated with the cacher."""
