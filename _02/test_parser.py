import unittest
from unittest.mock import Mock, call

from _02.parser import parse_json


class TestModel(unittest.TestCase):
    def setUp(self) -> None:
        self.json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'

    def test_incorrect_args(self):
        with self.assertRaises(ValueError) as err:
            parse_json(self.json_str, [], ['word2'], Mock())
        self.assertEqual(type(err.exception), ValueError)
        self.assertEqual(str(err.exception), "Pass not none arguments")
        with self.assertRaises(ValueError) as err:
            parse_json(self.json_str, ['word2'], keyword_callback=Mock())
        self.assertEqual(type(err.exception), ValueError)
        self.assertEqual(str(err.exception), "Pass not none arguments")
        with self.assertRaises(ValueError) as err:
            parse_json(self.json_str, ['word2'], ['asd'])
        self.assertEqual(type(err.exception), ValueError)
        self.assertEqual(str(err.exception), "Pass not none arguments")
        with self.assertRaises(TypeError) as err:
            parse_json(self.json_str, ['key1'], ['word2'], keyword_callback=lambda k, v, r: print(k, v, r))
        self.assertEqual(type(err.exception), TypeError)
        self.assertEqual(str(err.exception), "Wrong number of arguments in keyword_callback")
        with self.assertRaises(ValueError) as err:
            parse_json('', ['word2'], ['asd'], keyword_callback=Mock())
        self.assertEqual(type(err.exception), ValueError)
        self.assertEqual(str(err.exception), "Empty JSON string")

    def test_required_fields_or_keywords_not_found(self):
        keyword_callback = Mock()
        parse_json(self.json_str, ['qwerty'], ['word2'], keyword_callback)
        self.assertEqual(keyword_callback.call_count, 0)
        keyword_callback = Mock()
        parse_json(self.json_str, ['key1'], ['qwerty'], keyword_callback)
        self.assertEqual(keyword_callback.call_count, 0)

    def test_parser_successfully(self):
        keyword_callback = Mock()
        parse_json(self.json_str, ['key2'], ['word2'], keyword_callback)
        keyword_callback.assert_called_once_with('key2', 'word2')
        keyword_callback = Mock()
        parse_json(self.json_str, ['key1'], ['Word1', 'word2'], keyword_callback)
        keyword_callback.assert_has_calls([call('key1', 'Word1'), call('key1', 'word2')], any_order=True)
        keyword_callback = Mock()
        parse_json(self.json_str, ['key1', 'key2'], ['Word1', 'word2'], keyword_callback)
        keyword_callback.assert_has_calls([call('key1', 'Word1'), call('key1', 'word2'), call('key2', 'word2')],
                                          any_order=True)
