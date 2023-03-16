import unittest
from unittest import mock
import model_eval


class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = model_eval.SomeModel()

    def test_predict_model(self):
        with mock.patch("model_eval.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.1
            self.assertEqual(model_eval.predict_message_mood("Вулкан", self.model), "неуд")
            mock_predict.return_value = 0.9
            self.assertEqual(model_eval.predict_message_mood("Чапаев и пустота", self.model), "отл")
            mock_predict.return_value = 0.7
            self.assertEqual(model_eval.predict_message_mood("Нормально сообщение", self.model), "норм")

    def test_predict_model_change_thresholds(self):
        with mock.patch("model_eval.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.1
            self.assertEqual(model_eval.predict_message_mood("Вулкан", self.model, bad_thresholds=0.15), "неуд")
            mock_predict.return_value = 0.9
            self.assertEqual(model_eval.predict_message_mood("Чапаев и пустота", self.model, good_thresholds=0.9),
                             "норм")
            mock_predict.return_value = 0.7
            self.assertEqual(model_eval.predict_message_mood("Нормально сообщение", self.model, bad_thresholds=0.15,
                                                             good_thresholds=0.6), "отл")

    def test_predict_model_failed(self):
        with self.assertRaises(AttributeError) as err:
            model_eval.predict_message_mood("Текст", "not a model")
        self.assertEqual(type(err.exception), AttributeError)
        with self.assertRaises(TypeError) as err:
            model_eval.predict_message_mood("Текст", self.model, bad_thresholds='r')
        self.assertEqual(type(err.exception), TypeError)
        with self.assertRaises(TypeError) as err:
            model_eval.predict_message_mood("Текст", self.model, good_thresholds='r')
        self.assertEqual(type(err.exception), TypeError)
        with self.assertRaises(ValueError) as err:
            model_eval.predict_message_mood("Текст", self.model, bad_thresholds=0.8, good_thresholds=0.2)
        self.assertEqual(type(err.exception), ValueError)

    def test_predict(self):
        self.assertEqual(type(self.model.predict("Something")), float)
