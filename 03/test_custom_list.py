import unittest

from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def setUp(self) -> None:
        self.custom_list1 = CustomList([1, 2, 3])
        self.custom_list2 = CustomList([6, 39])
        self.custom_list4 = CustomList([0])
        self.list1 = [-1]
        self.list2 = [1, 4, 5]

    def test_add_function(self):
        custom_list3 = self.custom_list2 + self.custom_list1
        self.assertEqual(list(self.custom_list1 + self.custom_list2), [7, 41, 3])
        self.assertEqual(list(self.custom_list2 + self.custom_list1), [7, 41, 3])
        self.assertEqual(list(self.custom_list1 + self.custom_list2), list(custom_list3))
        self.assertEqual(list(self.list1 + self.custom_list4), [-1])
        self.assertEqual(list(self.list2 + self.custom_list4), self.list2)
        self.assertEqual(list(self.custom_list4 + self.list2), self.list2)
        self.assertEqual(list(self.list1 + self.custom_list2), [5, 39])
        self.assertEqual(list(self.list1 + self.custom_list2), list(self.custom_list2 + self.list1))
        self.assertEqual(list(CustomList() + CustomList()), [])
        self.assertIs(type(custom_list3), CustomList)
        self.assertEqual(list(self.custom_list1), [1, 2, 3])
        self.assertEqual(list(self.custom_list2), [6, 39])
        self.assertEqual(list(self.list1), [-1])
        self.assertEqual(list(self.custom_list4), [0])

    def test_sub_function(self):
        custom_list3 = self.custom_list2 - self.custom_list1
        self.assertEqual(list(self.custom_list1 - self.custom_list2), [-5, -37, 3])
        self.assertEqual(list(custom_list3), [5, 37, -3])
        self.assertEqual(list(self.list1 - self.custom_list2), [-7, -39])
        self.assertEqual(list(self.custom_list2 - self.list1), [7, 39])
        self.assertEqual(list(self.list1 - self.custom_list4), [-1])
        self.assertEqual(list(self.custom_list4 - self.list1), [1])
        self.assertEqual(list(self.list2 - self.custom_list4), self.list2)
        self.assertEqual(list(self.custom_list4 - self.list2), self.list2 * (-1))
        self.assertEqual(list(CustomList() - CustomList()), [])
        self.assertIs(type(self.custom_list1 - self.custom_list2), CustomList)
        self.assertEqual(list(self.custom_list1), [1, 2, 3])
        self.assertEqual(list(self.custom_list2), [6, 39])
        self.assertEqual(list(self.list1), [-1])
        self.assertEqual(list(self.custom_list4), [0])

    def test_lt(self):
        self.assertTrue(self.custom_list1 < self.custom_list2)
        self.assertFalse(self.custom_list1 < self.custom_list1)
        self.assertTrue(CustomList([20]) < CustomList([1, 19, 2]))
        self.assertEqual(list(self.custom_list1), [1, 2, 3])
        self.assertEqual(list(self.custom_list2), [6, 39])
        self.assertEqual(list(self.custom_list1), [1, 2, 3])
        self.assertEqual(list(self.custom_list2), [6, 39])

    def test_le(self):
        self.assertTrue(self.custom_list1 <= self.custom_list2)
        self.assertTrue(self.custom_list1 <= self.custom_list1)
        self.assertTrue(CustomList([20]) <= CustomList([1, 19]))
        self.assertEqual(list(self.custom_list1), [1, 2, 3])
        self.assertEqual(list(self.custom_list2), [6, 39])

    def test_gt(self):
        self.assertTrue(self.custom_list2 > self.custom_list1)
        self.assertFalse(self.custom_list1 > self.custom_list1)
        self.assertTrue(CustomList([1, 20]) > CustomList([2, 18]))
        self.assertEqual(list(self.custom_list1), [1, 2, 3])
        self.assertEqual(list(self.custom_list2), [6, 39])

    def test_ge(self):
        self.assertTrue(self.custom_list2 >= self.custom_list1)
        self.assertTrue(self.custom_list1 >= self.custom_list1)
        self.assertTrue(CustomList([1, 20]) >= CustomList([2, 19]))
        self.assertEqual(list(self.custom_list1), [1, 2, 3])
        self.assertEqual(list(self.custom_list2), [6, 39])

    def test_eq(self):
        self.assertTrue(self.custom_list1 == self.custom_list1)
        self.assertFalse(self.custom_list1 == self.custom_list2)
        self.assertTrue(CustomList([1, 20]) == CustomList([2, 19]))
        self.assertEqual(list(self.custom_list1), [1, 2, 3])
        self.assertEqual(list(self.custom_list2), [6, 39])

    def test_ne(self):
        self.assertTrue(self.custom_list1 != self.custom_list2)
        self.assertFalse(self.custom_list1 != self.custom_list1)
        self.assertEqual(list(self.custom_list1), [1, 2, 3])
        self.assertEqual(list(self.custom_list2), [6, 39])

    def test_str(self):
        self.assertTrue(
            str(self.custom_list1) == f"Список: {str(list(self.custom_list1))}\nСумма элементов списка: 6")
        self.assertTrue(
            str(CustomList()) == f"Список: {[]}\nСумма элементов списка: 0")
