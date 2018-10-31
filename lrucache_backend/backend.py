# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time
from threading import RLock

from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache
from lru import LRU  # dependency: lru-dict

"Thread-safe in-memory LRU object cache backend."
# Global in-memory store of cache data. Keyed by name, to provide
# multiple named local memory caches.
_caches = {}
_locks = {}


class LRUObjectCache(BaseCache):
    """
    A local memory cache that:

        1. Avoids serialization and deserialization
        2. Implements an LRU eviction strategy
        3. Implements timeouts on add()/get()/has_key()

    Uses a C based LRU dict for performance. See: https://github.com/amitdev/lru-dict

    Honours `MAX_ENTRIES` but not `CULL_FREQUENCY`, as the LRU algorithm will
    evict the least recently used value as required.
    """

    def __init__(self, name, params):
        BaseCache.__init__(self, params)
        self._cache = _caches.setdefault(name, LRU(self._max_entries))
        self._lock = _locks.setdefault(name, RLock())

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        new_key = self.make_key(key, version=version)
        with self._lock:
            if self._has_expired(key, version=version):
                self._set(new_key, value, timeout)
                return True
            return False

    def get(self, key, default=None, version=None):
        value, timeout = self._get(key, default, version)
        return value

    def _get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        with self._lock:
            value, expiration = self._cache.get(key, (default, -1))
        if not self._is_expired(expiration):
            return value, expiration
        with self._lock:
            try:
                del self._cache[key]
            except KeyError:
                pass
            return default, -1

    def _set(self, key, value, timeout=DEFAULT_TIMEOUT):
        timeout = self.get_backend_timeout(timeout)
        self._cache[key] = (value, timeout)

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        with self._lock:
            self._set(key, value, timeout)

    def incr(self, key, delta=1, version=None):
        with self._lock:
            # remain locked the entire time so the incr is guaranteed to be correct
            value, exp = self._get(key, version=version)
            if value is None:
                raise ValueError("Key '%s' not found" % key)
            new_value = value + delta
            new_key = self.make_key(key, version=version)
            self._cache[new_key] = (new_value, exp)
        return new_value

    def has_key(self, key, version=None):
        # _has_expired will do the locking
        if not self._has_expired(key, version=version):
            return True

        with self._lock:
            try:
                del self._cache[key]
            except KeyError:
                pass
            return False

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        with self._lock:
            try:
                del self._cache[key]
            except KeyError:
                pass

    def clear(self):
        with self._lock:
            self._cache.clear()

    def _has_expired(self, key, version=None):
        _, exp = self._get(key, version=version)
        return self._is_expired(exp)

    def _is_expired(self, expiration):
        if expiration is None or expiration > time.time():
            return False
        return True
