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

    def _remove(self, elem):
        if elem == self.head:
            if self.head != self.tail:
                self.head = elem.next
                elem.next.prev = elem.prev
            else:
                self.head, self.tail = None, None
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
            return None
        elem = self.cache[key]
        self._remove(elem)
        self._append(elem)
        return elem.value

    def set(self, key, value):
        if key in self.cache.keys():
            elem = self.cache[key]
            self._remove(elem)
        elif len(self.cache) >= self.limit:
            self._remove(self.head)
        elem = self.Element(value)
        self.cache[key] = elem
        self._append(elem)
