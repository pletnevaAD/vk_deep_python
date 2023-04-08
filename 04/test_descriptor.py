import datetime
import unittest

from descriptor import ReleaseYearField, Movie, NotValidReleaseYear, NotValidDuration, NotValidMoneySum, \
    DurationField, MoneyField


class TestDescriptors(unittest.TestCase):
    def setUp(self) -> None:
        self.movie = Movie("Harry Potter", 2001, datetime.time(2, 36), "$1000000")

    def test_release_year_field(self):
        self.assertEqual(self.movie.release_year, self.movie._year_field_release_year)
        self.assertEqual(self.movie.release_year, 2001)
        year_field = ReleaseYearField()
        self.assertIsNone(year_field.__get__(None, None))
        self.assertIsNone(year_field.__set__(None, None))
        self.assertIsNone(year_field.__delete__(None))
        with self.assertRaises(NotValidReleaseYear) as err:
            self.movie.release_year = 2309
        self.assertEqual(type(err.exception), NotValidReleaseYear)
        self.assertEqual(str(err.exception),
                         "Release year must be int, positive and  less than or equal to the present year")
        with self.assertRaises(NotValidReleaseYear) as err:
            self.movie.release_year = 12.4
        self.assertEqual(type(err.exception), NotValidReleaseYear)
        self.assertEqual(str(err.exception),
                         "Release year must be int, positive and  less than or equal to the present year")
        self.movie.release_year = 2002
        self.assertEqual(self.movie.release_year, 2002)
        del self.movie.release_year
        with self.assertRaises(AttributeError):
            self.movie.release_year

    def test_duration_field(self):
        self.assertEqual(self.movie.duration, self.movie._duration_field_duration)
        self.assertEqual(self.movie.duration, datetime.time(2, 36))
        duration_field = DurationField()
        self.assertIsNone(duration_field.__get__(None, None))
        self.assertIsNone(duration_field.__set__(None, None))
        self.assertIsNone(duration_field.__delete__(None))
        with self.assertRaises(NotValidDuration) as err:
            self.movie.duration = 2309
        self.assertEqual(type(err.exception), NotValidDuration)
        self.assertEqual(str(err.exception), "Duration must be time")
        self.movie.duration = datetime.time(2, 40)
        self.assertEqual(self.movie.duration, datetime.time(2, 40))
        del self.movie.duration
        with self.assertRaises(AttributeError):
            self.movie.duration

    def test_money_field(self):
        self.assertEqual(self.movie.fees, self.movie._money_field_fees)
        self.assertEqual(self.movie.fees, "$1000000")
        money_field = MoneyField()
        self.assertIsNone(money_field.__get__(None, None))
        self.assertIsNone(money_field.__set__(None, None))
        self.assertIsNone(money_field.__delete__(None))
        with self.assertRaises(NotValidMoneySum) as err:
            self.movie.fees = 38384
        self.assertEqual(type(err.exception), NotValidMoneySum)
        self.assertEqual(str(err.exception), "Money sum must consist of $ or ₽ or ¥ or € and an number")
        with self.assertRaises(NotValidMoneySum) as err:
            self.movie.fees = '$38384,3,4'
        self.assertEqual(type(err.exception), NotValidMoneySum)
        self.assertEqual(str(err.exception), "Money sum must consist of $ or ₽ or ¥ or € and an number")
        self.movie.fees = '$12345.6'
        self.assertEqual(self.movie.fees, '$12345.6')
        del self.movie.fees
        with self.assertRaises(AttributeError):
            self.movie.fees
