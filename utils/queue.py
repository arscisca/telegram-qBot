class Queue:
    """A queue of objects patiently waiting in line"""
    def __init__(self):
        self._items = []
        self._data = {}

    def append(self, item, **data):
        """Append an item in the queue
        Args:
            item: the item to be appended
            data: additional information bound to the item. For example it
                is possible to associate to the object its time of insertion
                in the queue"""
        self._items.append(item)
        if data:
            self._data[item] = data

    def insert(self, index, item, **data):
        """Insert an item in the requested position in line.
        Args:
            index: insertion position
            item: item to be inserted
            kwargs: additional information associated to the item
         """
        self._items.insert(index, item)
        if data:
            self._data[item] = data

    def pop(self):
        """Pick the first element in the queue
        Return:
            (item, dict) First element of the queue and its data
        """
        return self.remove(0)

    def remove(self, index):
        """Remove the element in under the requested index
        Return:
            (item, dict) popped item and its data
        """
        item = self._items.pop(index)
        if item in self._data:
            data = self._data.pop(item)
        else:
            data = None
        return item, data

    def clear(self):
        self._items = []
        self._data = {}

    def index(self, item):
        """Return the index of the item in line"""
        return self._items.index(item)

    def format(self, **format_functions):
        res = 'Current queue:\n'
        index_length = len(str(len(self)))
        for i, item in enumerate(self._items):
            # Show item index
            res += "  {index:>{size}}. {item}".format(index=i + 1, size=index_length, item=item)
            for field in self._data.get(item, []):
                formatter = format_functions.get(field, lambda f: str(f))
                res += ' ' + formatter(self._data[item][field])
            res += '\n'
        return res

    def is_empty(self):
        return len(self) == 0

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)

    def __str__(self):
        items = map(lambda obj: str(obj), self._items)
        return '[' + ', '.join(items) + ']'
