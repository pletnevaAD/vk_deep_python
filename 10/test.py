import json
import unittest

import cjson
import ujson


class TestCJson(unittest.TestCase):
    def setUp(self) -> None:
        self.str_json = '{"qwerty": "asd", "dd": -0.5}'
        self.incorrect_str = 'qwerty'
        self.incorrect_str2 = '{1:2}'
        self.incorrect_dict = [1, 2, 3]
        self.incorrect_dict2 = '{"qwerty": "asd", "dd": -0.5}'

    def test_loads(self):
        json_doc = json.loads(self.str_json)
        ujson_doc = ujson.loads(self.str_json)
        cjson_doc = cjson.loads(self.str_json)
        self.assertEqual(json_doc, cjson_doc)
        self.assertEqual(ujson_doc, cjson_doc)

    def test_dump(self):
        cjson_str = cjson.dumps(cjson.loads(self.str_json))
        self.assertEqual(cjson_str, self.str_json)

    def test_incorrect_input(self):
        with self.assertRaises(TypeError) as err:
            cjson.loads(self.incorrect_str)
        self.assertEqual(type(err.exception), TypeError)
        self.assertEqual(str(err.exception), "Expected object or value")
        with self.assertRaises(TypeError) as err:
            cjson.loads(self.incorrect_str2)
        self.assertEqual(type(err.exception), TypeError)
        self.assertEqual(str(err.exception), "Expected object or value")
        with self.assertRaises(TypeError) as err:
            cjson.dumps(self.incorrect_dict)
        self.assertEqual(type(err.exception), TypeError)
        self.assertEqual(str(err.exception), "Expected dict object")
        with self.assertRaises(TypeError) as err:
            cjson.dumps(self.incorrect_dict2)
        self.assertEqual(type(err.exception), TypeError)
        self.assertEqual(str(err.exception), "Expected dict object")


if __name__ == "__main__":
    test_json = TestCJson()
    test_json.setUp()
    test_json.test_loads()
    test_json.test_dump()
    test_json.test_incorrect_input()
