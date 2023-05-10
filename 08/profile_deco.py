import cProfile
import pstats


def profile_deco(fun):
    pr = cProfile.Profile()

    def inner(*args, **kwargs):
        nonlocal pr
        pr.enable()
        res = fun(*args, **kwargs)
        pr.disable()
        return res

    def print_stat():
        nonlocal pr
        ps = pstats.Stats(pr)
        ps.print_stats()

    inner.print_stat = print_stat
    return inner


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)

add.print_stat()  # выводится результат профилирования суммарно по всем вызовам функции add (всего два вызова)
sub.print_stat()  # выводится результат профилирования суммарно по всем вызовам функции sub (всего один вызов)
