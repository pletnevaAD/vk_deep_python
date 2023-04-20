import unittest

from lru_cache import LRUCache


class TestCache(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = LRUCache(2)
        self.cache_limit_3 = LRUCache(3)

    def test_not_existing_keys(self):
        self.assertEqual(self.cache.get("key"), None)
        self.cache.set('first', 'value1')
        self.assertEqual(self.cache.get("first"), 'value1')

    def test_limit(self):
        self.cache.set('first', 'value1')
        self.cache.set(2, 'value2')
        second_key = self.cache.get(2)
        first_key = self.cache.get("first")
        self.assertEqual(second_key, 'value2')
        self.assertEqual(first_key, 'value1')
        self.cache.set(3, 'value3')
        self.assertEqual(self.cache.get(2), None)
        self.assertEqual(self.cache.get("first"), 'value1')
        self.assertEqual(self.cache.get(3), 'value3')

    def test_set_existing_keys(self):
        self.cache.set('first', 'value1')
        self.cache.set('first', 'changed_value1')
        self.assertEqual(len(self.cache.cache), 1)
        self.assertEqual(self.cache.get('first'), 'changed_value1')

    def test_middle_of_cache(self):
        self.cache_limit_3.set('first', 'value1')
        self.cache_limit_3.set(2, 'value2')
        self.cache_limit_3.set(3, 'value3')
        self.cache_limit_3.get(2)
        self.cache_limit_3.set(4, 'value4')
        self.cache_limit_3.set(5, 'value5')
        self.assertEqual(self.cache_limit_3.get(2), 'value2')
