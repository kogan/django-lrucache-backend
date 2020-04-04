from django.core.cache.backends.locmem import DEFAULT_TIMEOUT, LocMemCache


class LocMemObjectCache(LocMemCache):
    """
    A subclass of the Django built in LocMemCache that:

    1. Does not pickle values
    2. Does not validate cache keys

    This cache backend has better performance, but also serves a different
    function from regular Django Cache backends. It serves as a global object
    cache where instances of objects are shared.
    """

    def validate_key(self, key):
        """
        Don't perform char validation, which can be substantial overhead for no
        gain. This backend is not used like a memcache backend would be.
        """
        return

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        with self._lock:
            if self._has_expired(key):
                self._set(key, value, timeout)
                return True
            return False

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        with self._lock:
            if self._has_expired(key):
                self._delete(key)
                return default
            value = self._cache[key]
            self._cache.move_to_end(key, last=False)
        return value

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        with self._lock:
            self._set(key, value, timeout)

    def incr(self, key, delta=1, version=None):
        key = self.make_key(key, version=version)
        with self._lock:
            if self._has_expired(key):
                self._delete(key)
                raise ValueError(f"Key '{key}' not found")
            value = self._cache[key]
            new_value = value + delta
            self._cache[key] = new_value
            self._cache.move_to_end(key, last=False)
        return new_value
