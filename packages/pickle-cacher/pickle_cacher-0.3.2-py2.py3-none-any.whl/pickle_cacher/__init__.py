"""Pickle-based caching."""
from pickle_cacher.pickle_cacher import cached  # noqa: S403
from pickle_cacher.pickle_cacher import PickleCacher  # noqa: S403


__all__ = ["cached", "PickleCacher"]
__version__ = "0.3.2"
