import cProfile
import time
import weakref
from memory_profiler import profile


class OrdinaryClass:
    def __init__(self, first_attr, second_attr, third_attr, fourth_attr):
        self.first_attr = first_attr
        self.second_attr = second_attr
        self.third_attr = third_attr
        self.fourth_attr = fourth_attr


class SlotsClass:
    __slots__ = ('first_attr', 'second_attr', 'third_attr', 'fourth_attr')

    def __init__(self, first_attr, second_attr, third_attr, fourth_attr):
        self.first_attr = first_attr
        self.second_attr = second_attr
        self.third_attr = third_attr
        self.fourth_attr = fourth_attr


class WeakRefClass:

    def __init__(self, first_attr, second_attr, third_attr, fourth_attr):
        self.first_attr = weakref.ref(first_attr)
        self.second_attr = weakref.ref(second_attr)
        self.third_attr = weakref.ref(third_attr)
        self.fourth_attr = weakref.ref(fourth_attr)


class ClassAttr:
    def __init__(self, attr):
        self.attr = attr


def time_deco(fun):
    def inner(*args, **kwargs):
        start_time = time.time()
        result = fun(*args, **kwargs)
        end_time = time.time()
        print(f'{end_time - start_time}')
        return result

    return inner


# @profile
# @time_deco
def fill_ordinary(n, first_attr, second_attr, third_attr, fourth_attr):
    print('Создание пачки экземпляров для класса с обычными атрибутами')
    ordinary_classes = [OrdinaryClass(first_attr, second_attr, third_attr, fourth_attr) for _ in range(n)]
    return ordinary_classes


# @profile
# @time_deco
def fill_slots(n, first_attr, second_attr, third_attr, fourth_attr):
    print('Создание пачки экземпляров для класса со слотами')
    slots_classes = [SlotsClass(first_attr, second_attr, third_attr, fourth_attr) for _ in range(n)]
    return slots_classes


# @profile
# @time_deco
def fill_weak_ref(n, first_attr, second_attr, third_attr, fourth_attr):
    print('Создание пачки экземпляров для класса с атрибутами weakref')
    weak_ref_classes = [WeakRefClass(first_attr, second_attr, third_attr, fourth_attr) for _ in range(n)]
    return weak_ref_classes


# @profile
# @time_deco
def get_attr(list_classes):
    print('Чтение пачки экземпляров')
    for instance in list_classes:
        instance.first_attr
        instance.second_attr
        instance.third_attr
        instance.fourth_attr
    return True


# @profile
# @time_deco
def upd_attr(list_classes, first_attr, second_attr, third_attr, fourth_attr):
    print('Изменение пачки экземпляров')
    for instance in list_classes:
        instance.first_attr = first_attr
        instance.second_attr = second_attr
        instance.third_attr = third_attr
        instance.fourth_attr = fourth_attr
    return True


def get_statistic(elems):
    first_attr, second_attr, third_attr, fourth_attr = ClassAttr('first_attr'), ClassAttr('second_attr'), ClassAttr(
        'third_attr'), ClassAttr('fourth_attr')
    first_attr_upd, second_attr_upd, third_attr_upd, fourth_attr_upd = ClassAttr('first_attr_upd'), ClassAttr(
        'second_attr_upd'), ClassAttr('third_attr_upd'), ClassAttr('fourth_attr_upd')
    ordinary_class = fill_ordinary(elems, first_attr, second_attr, third_attr, fourth_attr)
    get_attr(ordinary_class)
    upd_attr(ordinary_class, first_attr_upd, second_attr_upd, third_attr_upd, fourth_attr_upd)
    print('')
    slots_class = fill_slots(elems, first_attr, second_attr, third_attr, fourth_attr)
    get_attr(slots_class)
    upd_attr(slots_class, first_attr_upd, second_attr_upd, third_attr_upd, fourth_attr_upd)
    print('')
    weak_ref_class = fill_weak_ref(elems, first_attr, second_attr, third_attr, fourth_attr)
    get_attr(weak_ref_class)
    upd_attr(weak_ref_class, first_attr_upd, second_attr_upd, third_attr_upd, fourth_attr_upd)


N = 5_000_000
# get_statistic(N)
first_attr, second_attr, third_attr, fourth_attr = ClassAttr('first_attr'), ClassAttr('second_attr'), ClassAttr(
    'third_attr'), ClassAttr('fourth_attr')
first_attr_upd, second_attr_upd, third_attr_upd, fourth_attr_upd = ClassAttr('first_attr_upd'), ClassAttr(
    'second_attr_upd'), ClassAttr('third_attr_upd'), ClassAttr('fourth_attr_upd')
cProfile.run('ordinary_class = fill_ordinary(N, first_attr, second_attr, third_attr, fourth_attr)')
cProfile.run('get_attr(ordinary_class)')
cProfile.run('upd_attr(ordinary_class, first_attr_upd, second_attr_upd, third_attr_upd, fourth_attr_upd)')
cProfile.run('slots_class = fill_slots(N, first_attr, second_attr, third_attr, fourth_attr)')
cProfile.run('get_attr(slots_class)')
cProfile.run('upd_attr(slots_class, first_attr_upd, second_attr_upd, third_attr_upd, fourth_attr_upd)')
cProfile.run('weak_ref_class = fill_weak_ref(N, first_attr, second_attr, third_attr, fourth_attr)')
cProfile.run('get_attr(weak_ref_class)')
cProfile.run('upd_attr(weak_ref_class, first_attr_upd, second_attr_upd, third_attr_upd, fourth_attr_upd)')
