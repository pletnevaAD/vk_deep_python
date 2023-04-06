import unittest

from _04.custom_meta import CustomClass


class TestMeta(unittest.TestCase):
    def setUp(self) -> None:
        self.inst = CustomClass()

    def test_class_attribute(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError) as err:
            CustomClass.x
        self.assertEqual(type(err.exception), AttributeError)

    def test_instance_attr(self):
        self.assertEqual(self.inst.custom_x, 50)
        self.assertEqual(self.inst.custom_val, 99)
        self.assertEqual(self.inst.custom_line(), 100)
        with self.assertRaises(AttributeError) as err:
            self.inst.x
        self.assertEqual(type(err.exception), AttributeError)
        with self.assertRaises(AttributeError) as err:
            self.inst.val
        self.assertEqual(type(err.exception), AttributeError)
        with self.assertRaises(AttributeError) as err:
            self.inst.line()
        self.assertEqual(type(err.exception), AttributeError)
        with self.assertRaises(AttributeError) as err:
            self.inst.attr
        self.assertEqual(type(err.exception), AttributeError)

    def test_dynamic_attr(self):
        self.inst.dynamic = "added later"
        self.assertEqual(self.inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError) as err:
            self.inst.dynamic
        self.assertEqual(type(err.exception), AttributeError)

    def test_magic_attr(self):
        self.assertEqual(str(self.inst), "Custom_by_metaclass")
        self.assertIn('__str__', dir(self.inst))
        self.assertNotIn('custom___str__', dir(self.inst))
