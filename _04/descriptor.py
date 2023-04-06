import re
from datetime import datetime, time


class NotValidReleaseYear(Exception):
    pass


class NotValidDuration(Exception):
    pass


class NotValidMoneySum(Exception):
    pass


class ReleaseYearField:
    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_year_field_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self._instance_attr_name)

    def __set__(self, instance, value):
        if instance is None:
            return None
        if not isinstance(value, int) or value < 0 or value > datetime.now().year:
            raise NotValidReleaseYear("Release year must be int, positive and  less than or equal to the present year")
        return setattr(instance, self._instance_attr_name, value)

    def __delete__(self, instance):
        if instance is None:
            return None
        return delattr(instance, self._instance_attr_name)


class DurationField:
    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_duration_field_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self._instance_attr_name)

    def __set__(self, instance, value):
        if instance is None:
            return None
        if not isinstance(value, time):
            raise NotValidDuration("Duration must be time")
        return setattr(instance, self._instance_attr_name, value)

    def __delete__(self, instance):
        if instance is None:
            return None
        return delattr(instance, self._instance_attr_name)


class MoneyField:
    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_money_field_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self._instance_attr_name)

    def __set__(self, instance, value):
        if instance is None:
            return None
        if not isinstance(value, str) or not re.match('^[$|₽|¥|€][0-9]*[\.,]?[0-9]+$', value):
            raise NotValidMoneySum("Money sum must consist of $ or ₽ or ¥ or € and an number")
        return setattr(instance, self._instance_attr_name, value)

    def __delete__(self, instance):
        if instance is None:
            return None
        return delattr(instance, self._instance_attr_name)


class Movie:
    release_year = ReleaseYearField()
    duration = DurationField()
    fees = MoneyField()

    def __init__(self, name, release_year, duration, fees):
        self.name = name
        self.release_year = release_year
        self.duration = duration
        self.fees = fees
