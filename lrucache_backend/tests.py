# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import time

from django.test import TestCase

from lrucache_backend import LRUObjectCache


# functions/classes for complex data type tests
def f():
    return 42


class C(object):
    def m(n):
        return 24


class ObjectCacheTests(TestCase):

    # Tests copied from django/tests/cache/tests.py
    def setUp(self):
        self.cache = LRUObjectCache('lru', dict(max_entries=50))

    def tearDown(self):
        self.cache.clear()

    def test_eviction(self):
        cache = self.cache
        for r in range(50):
            cache.set(r, r)

        # The ordering below is very strict.

        # set will evict
        cache.set('a', 'a')
        self.assertIn('a', cache)
        self.assertIn(49, cache)
        self.assertNotIn(0, cache)

        # In promotes
        self.assertIn(1, cache)
        cache.set('b', 'b')
        self.assertNotIn(2, cache)

        # Add will evict
        self.assertFalse(cache.add('a', 'a'))
        self.assertIn(1, cache)
        self.assertTrue(cache.add('c', 'c'))
        self.assertNotIn(3, cache)

        # Get does not evict
        self.assertEqual(cache.get('c'), 'c')
        self.assertIn(4, cache)
        self.assertIsNone(cache.get('d'))
        self.assertIn(5, cache)

        # Get promotes
        self.assertEqual(cache.get(6), 6)
        cache.set('d', 'd')
        self.assertIn(6, cache)
        self.assertNotIn(7, cache)

    def test_multiple_caches(self):
        "Multiple caches are isolated"
        cache = self.cache
        cache2 = LRUObjectCache('lru2', dict(max_entries=50))
        self.cache.set('value', 42)
        self.assertEqual(cache.get('value'), 42)
        self.assertIsNone(cache2.get('value'))

    def test_incr_decr_timeout(self):
        """incr/decr does not modify expiry time (matches memcached behavior)"""
        cache = self.cache
        key = 'value'
        cache.set(key, 1, timeout=10000)
        _, exp = cache._get(key)
        cache.incr(key)
        self.assertEqual(exp, cache._get(key)[1])
        cache.decr(key)
        self.assertEqual(exp, cache._get(key)[1])

    def test_simple(self):
        # Simple cache set/get works
        cache = self.cache
        cache.set("key", "value")
        self.assertEqual(cache.get("key"), "value")

    def test_add(self):
        # A key can be added to a cache
        cache = self.cache
        cache.add("addkey1", "value")
        result = cache.add("addkey1", "newvalue")
        self.assertFalse(result)
        self.assertEqual(cache.get("addkey1"), "value")

    def test_prefix(self):
        # Test for same cache key conflicts between shared backend
        cache = self.cache
        prefixed_cache = LRUObjectCache('prefixed', dict(max_entries=50, KEY_PREFIX='yolo'))
        prefixed_cache._cache = cache._cache
        cache.set('somekey', 'value')

        # should not be set in the prefixed cache
        self.assertFalse(prefixed_cache.has_key('somekey'))  # noqa: W601

        prefixed_cache.set('somekey', 'value2')

        self.assertEqual(cache.get('somekey'), 'value')
        self.assertEqual(prefixed_cache.get('somekey'), 'value2')

    def test_non_existent(self):
        """Nonexistent cache keys return as None/default."""
        cache = self.cache
        self.assertIsNone(cache.get("does_not_exist"))
        self.assertEqual(cache.get("does_not_exist", "bang!"), "bang!")

    def test_get_many(self):
        # Multiple cache keys can be returned using get_many
        cache = self.cache
        cache.set('a', 'a')
        cache.set('b', 'b')
        cache.set('c', 'c')
        cache.set('d', 'd')
        self.assertEqual(cache.get_many(['a', 'c', 'd']), {'a': 'a', 'c': 'c', 'd': 'd'})
        self.assertEqual(cache.get_many(['a', 'b', 'e']), {'a': 'a', 'b': 'b'})

    def test_delete(self):
        # Cache keys can be deleted
        cache = self.cache
        cache.set("key1", "spam")
        cache.set("key2", "eggs")
        self.assertEqual(cache.get("key1"), "spam")
        cache.delete("key1")
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "eggs")

    def test_has_key(self):
        # The cache can be inspected for cache keys
        cache = self.cache
        cache.set("hello1", "goodbye1")
        self.assertTrue(cache.has_key("hello1"))  # noqa: W601
        self.assertFalse(cache.has_key("goodbye1"))  # noqa: W601
        cache.set("no_expiry", "here", None)
        self.assertTrue(cache.has_key("no_expiry"))  # noqa: W601

    def test_in(self):
        # The in operator can be used to inspect cache contents
        cache = self.cache
        cache.set("hello2", "goodbye2")
        self.assertIn("hello2", cache)
        self.assertNotIn("goodbye2", cache)

    def test_incr(self):
        # Cache values can be incremented
        cache = self.cache
        cache.set('answer', 41)
        self.assertEqual(cache.incr('answer'), 42)
        self.assertEqual(cache.get('answer'), 42)
        self.assertEqual(cache.incr('answer', 10), 52)
        self.assertEqual(cache.get('answer'), 52)
        self.assertEqual(cache.incr('answer', -10), 42)
        with self.assertRaises(ValueError):
            cache.incr('does_not_exist')

    def test_decr(self):
        # Cache values can be decremented
        cache = self.cache
        cache.set('answer', 43)
        self.assertEqual(cache.decr('answer'), 42)
        self.assertEqual(cache.get('answer'), 42)
        self.assertEqual(cache.decr('answer', 10), 32)
        self.assertEqual(cache.get('answer'), 32)
        self.assertEqual(cache.decr('answer', -10), 42)
        with self.assertRaises(ValueError):
            cache.decr('does_not_exist')

    def test_close(self):
        cache = self.cache
        self.assertTrue(hasattr(cache, 'close'))
        cache.close()

    def test_data_types(self):
        # Many different data types can be cached
        cache = self.cache
        stuff = {
            'string': 'this is a string',
            'int': 42,
            'list': [1, 2, 3, 4],
            'tuple': (1, 2, 3, 4),
            'dict': {'A': 1, 'B': 2},
            'function': f,
            'class': C,
        }
        cache.set("stuff", stuff)
        self.assertEqual(cache.get("stuff"), stuff)

    def test_expiration(self):
        # Cache values can be set to expire
        cache = self.cache
        cache.set('expire1', 'very quickly', 1)
        cache.set('expire2', 'very quickly', 1)
        cache.set('expire3', 'very quickly', 1)

        time.sleep(2)
        self.assertIsNone(cache.get("expire1"))

        cache.add("expire2", "newvalue")
        self.assertEqual(cache.get("expire2"), "newvalue")
        self.assertFalse(cache.has_key("expire3"))  # noqa: W601

    def test_unicode(self):
        # Unicode values can be cached
        cache = self.cache
        stuff = {
            'ascii': 'ascii_value',
            'unicode_ascii': 'Iñtërnâtiônàlizætiøn1',
            'Iñtërnâtiônàlizætiøn': 'Iñtërnâtiônàlizætiøn2',
            'ascii2': {'x': 1}
        }
        # Test `set`
        for (key, value) in stuff.items():
            cache.set(key, value)
            self.assertEqual(cache.get(key), value)

        # Test `add`
        for (key, value) in stuff.items():
            cache.delete(key)
            cache.add(key, value)
            self.assertEqual(cache.get(key), value)

        # Test `set_many`
        for (key, value) in stuff.items():
            cache.delete(key)
        cache.set_many(stuff)
        for (key, value) in stuff.items():
            self.assertEqual(cache.get(key), value)

    def test_binary_string(self):
        # Binary strings should be cacheable
        cache = self.cache
        from zlib import compress, decompress
        value = 'value_to_be_compressed'
        compressed_value = compress(value.encode())

        # Test set
        cache.set('binary1', compressed_value)
        compressed_result = cache.get('binary1')
        self.assertEqual(compressed_value, compressed_result)
        self.assertEqual(value, decompress(compressed_result).decode())

        # Test add
        cache.add('binary1-add', compressed_value)
        compressed_result = cache.get('binary1-add')
        self.assertEqual(compressed_value, compressed_result)
        self.assertEqual(value, decompress(compressed_result).decode())

        # Test set_many
        cache.set_many({'binary1-set_many': compressed_value})
        compressed_result = cache.get('binary1-set_many')
        self.assertEqual(compressed_value, compressed_result)
        self.assertEqual(value, decompress(compressed_result).decode())

    def test_set_many(self):
        # Multiple keys can be set using set_many
        cache = self.cache
        cache.set_many({"key1": "spam", "key2": "eggs"})
        self.assertEqual(cache.get("key1"), "spam")
        self.assertEqual(cache.get("key2"), "eggs")

    def test_set_many_expiration(self):
        # set_many takes a second ``timeout`` parameter
        cache = self.cache
        cache.set_many({"key1": "spam", "key2": "eggs"}, 1)
        time.sleep(2)
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))

    def test_delete_many(self):
        # Multiple keys can be deleted using delete_many
        cache = self.cache
        cache.set("key1", "spam")
        cache.set("key2", "eggs")
        cache.set("key3", "ham")
        cache.delete_many(["key1", "key2"])
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))
        self.assertEqual(cache.get("key3"), "ham")

    def test_clear(self):
        # The cache can be emptied using clear
        cache = self.cache
        cache.set("key1", "spam")
        cache.set("key2", "eggs")
        cache.clear()
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))

    def test_long_timeout(self):
        """
        Followe memcached's convention where a timeout greater than 30 days is
        treated as an absolute expiration timestamp instead of a relative
        offset (#12399).
        """
        cache = self.cache
        cache.set('key1', 'eggs', 60 * 60 * 24 * 30 + 1)  # 30 days + 1 second
        self.assertEqual(cache.get('key1'), 'eggs')

        cache.add('key2', 'ham', 60 * 60 * 24 * 30 + 1)
        self.assertEqual(cache.get('key2'), 'ham')

        cache.set_many({'key3': 'sausage', 'key4': 'lobster bisque'}, 60 * 60 * 24 * 30 + 1)
        self.assertEqual(cache.get('key3'), 'sausage')
        self.assertEqual(cache.get('key4'), 'lobster bisque')

    def test_forever_timeout(self):
        """
        Passing in None into timeout results in a value that is cached forever
        """
        cache = self.cache
        cache.set('key1', 'eggs', None)
        self.assertEqual(cache.get('key1'), 'eggs')

        cache.add('key2', 'ham', None)
        self.assertEqual(cache.get('key2'), 'ham')
        added = cache.add('key1', 'new eggs', None)
        self.assertIs(added, False)
        self.assertEqual(cache.get('key1'), 'eggs')

        cache.set_many({'key3': 'sausage', 'key4': 'lobster bisque'}, None)
        self.assertEqual(cache.get('key3'), 'sausage')
        self.assertEqual(cache.get('key4'), 'lobster bisque')

    def test_zero_timeout(self):
        """
        Passing in zero into timeout results in a value that is not cached
        """
        cache = self.cache
        cache.set('key1', 'eggs', 0)
        self.assertIsNone(cache.get('key1'))

        cache.add('key2', 'ham', 0)
        self.assertIsNone(cache.get('key2'))

        cache.set_many({'key3': 'sausage', 'key4': 'lobster bisque'}, 0)
        self.assertIsNone(cache.get('key3'))
        self.assertIsNone(cache.get('key4'))

    def test_float_timeout(self):
        # Make sure a timeout given as a float doesn't crash anything.
        cache = self.cache
        cache.set("key1", "spam", 100.2)
        self.assertEqual(cache.get("key1"), "spam")

    def test_cache_versioning_get_set(self):
        # set, using default version = 1
        cache = self.cache
        cache2 = LRUObjectCache('lru2', dict(VERSION=2))
        cache2._cache = cache._cache

        cache.set('answer1', 42)
        self.assertEqual(cache.get('answer1'), 42)
        self.assertEqual(cache.get('answer1', version=1), 42)
        self.assertIsNone(cache.get('answer1', version=2))

        self.assertIsNone(cache2.get('answer1'))
        self.assertEqual(cache2.get('answer1', version=1), 42)
        self.assertIsNone(cache2.get('answer1', version=2))

        # set, default version = 1, but manually override version = 2
        cache.set('answer2', 42, version=2)
        self.assertIsNone(cache.get('answer2'))
        self.assertIsNone(cache.get('answer2', version=1))
        self.assertEqual(cache.get('answer2', version=2), 42)

        self.assertEqual(cache2.get('answer2'), 42)
        self.assertIsNone(cache2.get('answer2', version=1))
        self.assertEqual(cache2.get('answer2', version=2), 42)

        # v2 set, using default version = 2
        cache2.set('answer3', 42)
        self.assertIsNone(cache.get('answer3'))
        self.assertIsNone(cache.get('answer3', version=1))
        self.assertEqual(cache.get('answer3', version=2), 42)

        self.assertEqual(cache2.get('answer3'), 42)
        self.assertIsNone(cache2.get('answer3', version=1))
        self.assertEqual(cache2.get('answer3', version=2), 42)

        # v2 set, default version = 2, but manually override version = 1
        cache2.set('answer4', 42, version=1)
        self.assertEqual(cache.get('answer4'), 42)
        self.assertEqual(cache.get('answer4', version=1), 42)
        self.assertIsNone(cache.get('answer4', version=2))

        self.assertIsNone(cache2.get('answer4'))
        self.assertEqual(cache2.get('answer4', version=1), 42)
        self.assertIsNone(cache2.get('answer4', version=2))

    def test_cache_versioning_add(self):
        # add, default version = 1, but manually override version = 2
        cache = self.cache
        cache2 = LRUObjectCache('lru2', dict(VERSION=2))
        cache2._cache = cache._cache

        cache.add('answer1', 42, version=2)
        self.assertIsNone(cache.get('answer1', version=1))
        self.assertEqual(cache.get('answer1', version=2), 42)

        cache.add('answer1', 37, version=2)
        self.assertIsNone(cache.get('answer1', version=1))
        self.assertEqual(cache.get('answer1', version=2), 42)

        cache.add('answer1', 37, version=1)
        self.assertEqual(cache.get('answer1', version=1), 37)
        self.assertEqual(cache.get('answer1', version=2), 42)

        # v2 add, using default version = 2
        cache2.add('answer2', 42)
        self.assertIsNone(cache.get('answer2', version=1))
        self.assertEqual(cache.get('answer2', version=2), 42)

        cache2.add('answer2', 37)
        self.assertIsNone(cache.get('answer2', version=1))
        self.assertEqual(cache.get('answer2', version=2), 42)

        cache2.add('answer2', 37, version=1)
        self.assertEqual(cache.get('answer2', version=1), 37)
        self.assertEqual(cache.get('answer2', version=2), 42)

        # v2 add, default version = 2, but manually override version = 1
        cache2.add('answer3', 42, version=1)
        self.assertEqual(cache.get('answer3', version=1), 42)
        self.assertIsNone(cache.get('answer3', version=2))

        cache2.add('answer3', 37, version=1)
        self.assertEqual(cache.get('answer3', version=1), 42)
        self.assertIsNone(cache.get('answer3', version=2))

        cache2.add('answer3', 37)
        self.assertEqual(cache.get('answer3', version=1), 42)
        self.assertEqual(cache.get('answer3', version=2), 37)

    def test_cache_versioning_has_key(self):
        cache = self.cache
        cache2 = LRUObjectCache('lru2', dict(VERSION=2))
        cache2._cache = cache._cache
        cache.set('answer1', 42)

        # has_key
        self.assertTrue(cache.has_key('answer1'))  # noqa: W601
        self.assertTrue(cache.has_key('answer1', version=1))  # noqa: W601
        self.assertFalse(cache.has_key('answer1', version=2))  # noqa: W601

        self.assertFalse(cache2.has_key('answer1'))  # noqa: W601
        self.assertTrue(cache2.has_key('answer1', version=1))  # noqa: W601
        self.assertFalse(cache2.has_key('answer1', version=2))  # noqa: W601

    def test_cache_versioning_delete(self):
        cache = self.cache
        cache2 = LRUObjectCache('lru2', dict(VERSION=2))
        cache2._cache = cache._cache

        cache.set('answer1', 37, version=1)
        cache.set('answer1', 42, version=2)
        cache.delete('answer1')
        self.assertIsNone(cache.get('answer1', version=1))
        self.assertEqual(cache.get('answer1', version=2), 42)

        cache.set('answer2', 37, version=1)
        cache.set('answer2', 42, version=2)
        cache.delete('answer2', version=2)
        self.assertEqual(cache.get('answer2', version=1), 37)
        self.assertIsNone(cache.get('answer2', version=2))

        cache.set('answer3', 37, version=1)
        cache.set('answer3', 42, version=2)
        cache2.delete('answer3')
        self.assertEqual(cache.get('answer3', version=1), 37)
        self.assertIsNone(cache.get('answer3', version=2))

        cache.set('answer4', 37, version=1)
        cache.set('answer4', 42, version=2)
        cache2.delete('answer4', version=1)
        self.assertIsNone(cache.get('answer4', version=1))
        self.assertEqual(cache.get('answer4', version=2), 42)

    def test_cache_versioning_incr_decr(self):
        cache = self.cache
        cache2 = LRUObjectCache('lru2', dict(VERSION=2))
        cache2._cache = cache._cache

        cache.set('answer1', 37, version=1)
        cache.set('answer1', 42, version=2)
        cache.incr('answer1')
        self.assertEqual(cache.get('answer1', version=1), 38)
        self.assertEqual(cache.get('answer1', version=2), 42)
        cache.decr('answer1')
        self.assertEqual(cache.get('answer1', version=1), 37)
        self.assertEqual(cache.get('answer1', version=2), 42)

        cache.set('answer2', 37, version=1)
        cache.set('answer2', 42, version=2)
        cache.incr('answer2', version=2)
        self.assertEqual(cache.get('answer2', version=1), 37)
        self.assertEqual(cache.get('answer2', version=2), 43)
        cache.decr('answer2', version=2)
        self.assertEqual(cache.get('answer2', version=1), 37)
        self.assertEqual(cache.get('answer2', version=2), 42)

        cache.set('answer3', 37, version=1)
        cache.set('answer3', 42, version=2)
        cache2.incr('answer3')
        self.assertEqual(cache.get('answer3', version=1), 37)
        self.assertEqual(cache.get('answer3', version=2), 43)
        cache2.decr('answer3')
        self.assertEqual(cache.get('answer3', version=1), 37)
        self.assertEqual(cache.get('answer3', version=2), 42)

        cache.set('answer4', 37, version=1)
        cache.set('answer4', 42, version=2)
        cache2.incr('answer4', version=1)
        self.assertEqual(cache.get('answer4', version=1), 38)
        self.assertEqual(cache.get('answer4', version=2), 42)
        cache2.decr('answer4', version=1)
        self.assertEqual(cache.get('answer4', version=1), 37)
        self.assertEqual(cache.get('answer4', version=2), 42)

    def test_cache_versioning_get_set_many(self):
        cache = self.cache
        cache2 = LRUObjectCache('lru2', dict(VERSION=2))
        cache2._cache = cache._cache

        # set, using default version = 1
        cache.set_many({'ford1': 37, 'arthur1': 42})
        self.assertEqual(cache.get_many(['ford1', 'arthur1']), {'ford1': 37, 'arthur1': 42})
        self.assertEqual(cache.get_many(['ford1', 'arthur1'], version=1), {'ford1': 37, 'arthur1': 42})
        self.assertEqual(cache.get_many(['ford1', 'arthur1'], version=2), {})

        self.assertEqual(cache2.get_many(['ford1', 'arthur1']), {})
        self.assertEqual(cache2.get_many(['ford1', 'arthur1'], version=1), {'ford1': 37, 'arthur1': 42})
        self.assertEqual(cache2.get_many(['ford1', 'arthur1'], version=2), {})

        # set, default version = 1, but manually override version = 2
        cache.set_many({'ford2': 37, 'arthur2': 42}, version=2)
        self.assertEqual(cache.get_many(['ford2', 'arthur2']), {})
        self.assertEqual(cache.get_many(['ford2', 'arthur2'], version=1), {})
        self.assertEqual(cache.get_many(['ford2', 'arthur2'], version=2), {'ford2': 37, 'arthur2': 42})

        self.assertEqual(cache2.get_many(['ford2', 'arthur2']), {'ford2': 37, 'arthur2': 42})
        self.assertEqual(cache2.get_many(['ford2', 'arthur2'], version=1), {})
        self.assertEqual(cache2.get_many(['ford2', 'arthur2'], version=2), {'ford2': 37, 'arthur2': 42})

        # v2 set, using default version = 2
        cache2.set_many({'ford3': 37, 'arthur3': 42})
        self.assertEqual(cache.get_many(['ford3', 'arthur3']), {})
        self.assertEqual(cache.get_many(['ford3', 'arthur3'], version=1), {})
        self.assertEqual(cache.get_many(['ford3', 'arthur3'], version=2), {'ford3': 37, 'arthur3': 42})

        self.assertEqual(cache2.get_many(['ford3', 'arthur3']), {'ford3': 37, 'arthur3': 42})
        self.assertEqual(cache2.get_many(['ford3', 'arthur3'], version=1), {})
        self.assertEqual(cache2.get_many(['ford3', 'arthur3'], version=2), {'ford3': 37, 'arthur3': 42})

        # v2 set, default version = 2, but manually override version = 1
        cache2.set_many({'ford4': 37, 'arthur4': 42}, version=1)
        self.assertEqual(cache.get_many(['ford4', 'arthur4']), {'ford4': 37, 'arthur4': 42})
        self.assertEqual(cache.get_many(['ford4', 'arthur4'], version=1), {'ford4': 37, 'arthur4': 42})
        self.assertEqual(cache.get_many(['ford4', 'arthur4'], version=2), {})

        self.assertEqual(cache2.get_many(['ford4', 'arthur4']), {})
        self.assertEqual(cache2.get_many(['ford4', 'arthur4'], version=1), {'ford4': 37, 'arthur4': 42})
        self.assertEqual(cache2.get_many(['ford4', 'arthur4'], version=2), {})

    def test_incr_version(self):
        cache = self.cache
        cache2 = LRUObjectCache('lru2', dict(VERSION=2))
        cache2._cache = cache._cache

        cache.set('answer', 42, version=2)
        self.assertIsNone(cache.get('answer'))
        self.assertIsNone(cache.get('answer', version=1))
        self.assertEqual(cache.get('answer', version=2), 42)
        self.assertIsNone(cache.get('answer', version=3))

        self.assertEqual(cache.incr_version('answer', version=2), 3)
        self.assertIsNone(cache.get('answer'))
        self.assertIsNone(cache.get('answer', version=1))
        self.assertIsNone(cache.get('answer', version=2))
        self.assertEqual(cache.get('answer', version=3), 42)

        cache2.set('answer2', 42)
        self.assertEqual(cache2.get('answer2'), 42)
        self.assertIsNone(cache2.get('answer2', version=1))
        self.assertEqual(cache2.get('answer2', version=2), 42)
        self.assertIsNone(cache2.get('answer2', version=3))

        self.assertEqual(cache2.incr_version('answer2'), 3)
        self.assertIsNone(cache2.get('answer2'))
        self.assertIsNone(cache2.get('answer2', version=1))
        self.assertIsNone(cache2.get('answer2', version=2))
        self.assertEqual(cache2.get('answer2', version=3), 42)

        with self.assertRaises(ValueError):
            cache.incr_version('does_not_exist')

    def test_decr_version(self):
        cache = self.cache
        cache2 = LRUObjectCache('lru2', dict(VERSION=2))
        cache2._cache = cache._cache

        cache.set('answer', 42, version=2)
        self.assertIsNone(cache.get('answer'))
        self.assertIsNone(cache.get('answer', version=1))
        self.assertEqual(cache.get('answer', version=2), 42)

        self.assertEqual(cache.decr_version('answer', version=2), 1)
        self.assertEqual(cache.get('answer'), 42)
        self.assertEqual(cache.get('answer', version=1), 42)
        self.assertIsNone(cache.get('answer', version=2))

        cache2.set('answer2', 42)
        self.assertEqual(cache2.get('answer2'), 42)
        self.assertIsNone(cache2.get('answer2', version=1))
        self.assertEqual(cache2.get('answer2', version=2), 42)

        self.assertEqual(cache2.decr_version('answer2'), 1)
        self.assertIsNone(cache2.get('answer2'))
        self.assertEqual(cache2.get('answer2', version=1), 42)
        self.assertIsNone(cache2.get('answer2', version=2))

        with self.assertRaises(ValueError):
            cache.decr_version('does_not_exist', version=2)


class BackendObjectCacheTests(ObjectCacheTests):

    def setUp(self):
        from django.core.cache import cache
        self.cache = cache
