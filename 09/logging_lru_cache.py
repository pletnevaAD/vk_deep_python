import argparse
import logging
import sys
import weakref


class LRUCache:
    class Element:
        def __init__(self, value):
            self.prev = None
            self.next = None
            self.value = value

    def __init__(self, limit=42):
        self.limit = limit
        self.cache = weakref.WeakValueDictionary()
        self.head = None
        self.tail = None
        default_logger.debug('Создание LRUCache размера %s', limit)

    def _remove(self, elem):
        if elem == self.head:
            if self.head != self.tail:
                self.head = elem.next
                elem.next.prev = elem.prev
            else:
                self.head, self.tail = None, None
                default_logger.debug('Кэш пуст')
        elif elem == self.tail:
            self.tail = elem.prev
            elem.prev.next = elem.next
        else:
            elem.prev.next = elem.next
            elem.next.prev = elem.prev

    def _append(self, elem):
        elem.prev, elem.next = self.tail, None
        if self.head is None:
            self.head = elem
        if self.tail is not None:
            self.tail.next = elem
        self.tail = elem

    def get(self, key):
        if key not in self.cache.keys():
            default_logger.warning("Ключ %s отсутствует в кэше", key)
            return None
        elem = self.cache[key]
        if elem != self.head:
            self._remove(elem)
            self._append(elem)
        default_logger.debug("Совершена операция get по ключу %s: найдено значение %s", key, elem.value)
        return elem.value

    def set(self, key, value):
        if key in self.cache.keys():
            elem = self.cache[key]
            self._remove(elem)
            default_logger.debug("Удалено старое значение %s по ключу %s", elem.value, key)
        elif len(self.cache) >= self.limit:
            key_to_del = [i for i in self.cache if self.cache[i] == self.head]
            default_logger.debug("Кэш переполнен, удаление элемента {%s: %s}", key_to_del.pop(),
                                 self.head.value)
            self._remove(self.head)
        elem = self.Element(value)
        self.cache[key] = elem
        self._append(elem)
        default_logger.debug("Совершена операция set: вставка значения %s по ключу %s", value, key)


class SetFilter(logging.Filter):
    def filter(self, record):
        return "set" in record.msg


if __name__ == "__main__":
    format_output_file = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")

    common_handler = logging.FileHandler("cache.log")
    common_handler.setFormatter(format_output_file)

    default_logger = logging.getLogger("cache")
    default_logger.setLevel(logging.DEBUG)
    default_logger.addHandler(common_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true')
    parser.add_argument('-f', action='store_true')
    input_args = parser.parse_args(sys.argv[1:])
    if input_args.s:
        format_stdout = logging.Formatter("%(asctime)s\t%(levelname)s\t[stdout]\t%(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(format_stdout)
        default_logger.addHandler(stream_handler)
    if input_args.f:
        default_logger.addFilter(SetFilter())

    # cache = LRUCache(2)
    # cache.set(1, 2)
    # cache.get(1)
    # cache.get(2)
    # cache.set(2, 2)
    # cache.set(3, 2)
    # cache.set(3, 4)
