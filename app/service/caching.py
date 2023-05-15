from datetime import datetime


class ListNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class CustomDict:
    def __init__(self):
        self.dict = {}

    def __contains__(self, key):
        return key in self.dict

    def get(self, key, default=None):
        return self.dict.get(key, default)

    def put(self, key, value):
        self.dict[key] = value

    def popitem(self, last=True):
        if last:
            return self.dict.popitem()
        else:
            key, value = next(iter(self.dict.items()))
            del self.dict[key]
            return key, value


class MagicCache:
    def __init__(self, capacity=500):
        self.cache = CustomDict()
        self.capacity = capacity
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def __contains__(self, key):
        return key in self.cache

    def get(self, key, default=None):
        node = self.cache.get(key)
        if node is not None:
            return node.value
        return default

    def put(self, key, value):
        if key in self.cache:
            node = self.cache.get(key)
            node.value = value
            self._remove(node)

        if len(self.cache.dict) >= self.capacity:
            self._remove(self.tail.prev)

        new_node = ListNode(key, value)
        self._add(new_node)
        self.cache.put(key, new_node)

    def clear(self):
        self.cache = CustomDict()

    @staticmethod
    def _remove(node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node):
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node

    def popitem(self, last=True):
        if last:
            last_node = self.tail.prev
            if last_node != self.head:
                self._remove(last_node)
                del self.cache[last_node.key]
                return last_node.key, last_node.value
        else:
            first_node = self.head.next
            if first_node != self.tail:
                self._remove(first_node)
                del self.cache[first_node.key]
                return first_node.key, first_node.value

        raise KeyError('cache is empty')


class RequestBatch:
    def __init__(self, ip_address: str, count: int, last_time: datetime):
        self.ip_address = ip_address
        self.count = count
        self.last_time = last_time