import io
import unittest
from unittest import mock
from unittest.mock import mock_open

from generator import generator_text


class TestModel(unittest.TestCase):
    def test_generator_failed(self):
        with self.assertRaises(TypeError) as err:
            list(generator_text(2, []))
        self.assertEqual(type(err.exception), TypeError)
        with self.assertRaises(TypeError) as err:
            list(generator_text("../text", 1))
        self.assertEqual(type(err.exception), TypeError)
        with self.assertRaises(FileNotFoundError) as err:
            list(generator_text("asd", []))
        self.assertEqual(str(err.exception), "Такого файла не существует")

    def test_generator(self):
        file_content = 'МоРе вода трава\nжук'
        expected_output = ['МоРе вода трава']
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            result = list(generator_text('test.txt', ['трава']))
            self.assertEqual(result, expected_output)
            result = list(generator_text('test.txt', ['трава', 'вода']))
            self.assertEqual(result, expected_output)
            result = list(generator_text('test.txt', ['море']))
            self.assertEqual(result, expected_output)
            expected_output = ['жук']
            result = list(generator_text('test.txt', ['жук']))
            self.assertEqual(result, expected_output)

    def test_generator_multiple_str(self):
        file_content = 'МоРе вода трава\nжук'
        expected_output = ['МоРе вода трава', 'жук']
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            result = list(generator_text('test.txt', ['трава', 'жук']))
            self.assertEqual(result, expected_output)

    def test_generator_different_arguments_type(self):
        file = io.StringIO("МоРе вода трава\nжук")
        result = list(generator_text(file, ['море', 'вода']))
        self.assertEqual(len(result), 1)
        self.assertIn("МоРе вода трава", result)
        result = list(generator_text('C:\\Users\\pletn\\PycharmProjects\\vk_deep_python\\text', ['море', 'вода']))
        self.assertEqual(len(result), 2)
        self.assertIn("океан крыша море вода", result)
        self.assertIn("джеймс бонд морей море", result)


    def test_generator_not_find(self):
        file_content = 'А Роза упала на лапу Азора'
        expected_output = []
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            result = list(generator_text('test.txt', ['роз']))
            self.assertEqual(result, expected_output)
            result = list(generator_text('test.txt', ['розау']))
            self.assertEqual(result, expected_output)
