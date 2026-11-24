"""Custom container data structures: HashMap and LRUCache."""

from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    cast,
)

K = TypeVar("K")
V = TypeVar("V")

_MISSING = object()

__all__ = ["HashMap", "LRUCache"]


class _HashEntry(Generic[K, V]):
    __slots__ = ("key", "value")

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value


class HashMap(Generic[K, V]):
    """Hash table implemented with separate chaining buckets.

    Does not use dict, OrderedDict, or collections for internal storage.
    Automatically doubles capacity and rehashes when load factor exceeds 0.75.

    Space: O(n).
    """

    def __init__(self, items: Optional[Iterable[Tuple[K, V]]] = None) -> None:
        """Initialize an empty or populated hash map.

        Args:
            items: Optional iterable of (key, value) pairs.

        Space: O(n).
        """
        self._capacity: int = 16
        self._size: int = 0
        self._buckets: List[List[_HashEntry[K, V]]] = [
            [] for _ in range(self._capacity)
        ]
        if items is not None:
            for k, v in items:
                self.put(k, v)

    def _bucket_index(self, key: K, capacity: int) -> int:
        return hash(key) % capacity

    def _resize(self) -> None:
        new_capacity = self._capacity * 2
        new_buckets: List[List[_HashEntry[K, V]]] = [
            [] for _ in range(new_capacity)
        ]
        for bucket in self._buckets:
            for entry in bucket:
                idx = self._bucket_index(entry.key, new_capacity)
                new_buckets[idx].append(entry)
        self._capacity = new_capacity
        self._buckets = new_buckets

    def put(self, key: K, value: V) -> None:
        """Insert or update a key-value pair in the map.

        Args:
            key: Hashable key.
            value: Value associated with key.

        Time: O(1) average, O(n) worst case. Space: O(1) amortized.
        """
        idx = self._bucket_index(key, self._capacity)
        bucket = self._buckets[idx]
        for entry in bucket:
            if entry.key == key:
                entry.value = value
                return
        bucket.append(_HashEntry(key, value))
        self._size += 1
        if self._size / self._capacity > 0.75:
            self._resize()

    def get(self, key: K, default: Any = _MISSING) -> Any:
        """Retrieve the value associated with ``key``, or ``default`` if provided.

        Args:
            key: Key to look up.
            default: Fallback value if key is not found.

        Returns:
            The value associated with the key, or default if specified.

        Raises:
            KeyError: if key is not in the map and no default is provided.

        Time: O(1) average, O(n) worst case. Space: O(1).
        """
        idx = self._bucket_index(key, self._capacity)
        for entry in self._buckets[idx]:
            if entry.key == key:
                return entry.value
        if default is not _MISSING:
            return default
        raise KeyError(f"Key {key!r} not found in HashMap")

    def remove(self, key: K) -> V:
        """Remove ``key`` and return its associated value.

        Args:
            key: Key to remove.

        Returns:
            The value that was associated with key.

        Raises:
            KeyError: if key is not found in the map.

        Time: O(1) average, O(n) worst case. Space: O(1).
        """
        idx = self._bucket_index(key, self._capacity)
        bucket = self._buckets[idx]
        for i, entry in enumerate(bucket):
            if entry.key == key:
                val = entry.value
                bucket.pop(i)
                self._size -= 1
                return val
        raise KeyError(f"Key {key!r} not found in HashMap")

    def contains(self, key: K) -> bool:
        """Return True if ``key`` is present in the map.

        Args:
            key: Key to check.

        Time: O(1) average, O(n) worst case. Space: O(1).
        """
        idx = self._bucket_index(key, self._capacity)
        for entry in self._buckets[idx]:
            if entry.key == key:
                return True
        return False

    def keys(self) -> List[K]:
        """Return a list of all keys in the map.

        Time: O(n). Space: O(n).
        """
        return [entry.key for bucket in self._buckets for entry in bucket]

    def values(self) -> List[V]:
        """Return a list of all values in the map.

        Time: O(n). Space: O(n).
        """
        return [entry.value for bucket in self._buckets for entry in bucket]

    def items(self) -> List[Tuple[K, V]]:
        """Return a list of all (key, value) pairs in the map.

        Time: O(n). Space: O(n).
        """
        return [
            (entry.key, entry.value)
            for bucket in self._buckets
            for entry in bucket
        ]

    def clear(self) -> None:
        """Remove all entries from the map.

        Time: O(capacity). Space: O(1).
        """
        self._capacity = 16
        self._size = 0
        self._buckets = [[] for _ in range(self._capacity)]

    def __len__(self) -> int:
        return self._size

    def __getitem__(self, key: K) -> V:
        return cast(V, self.get(key))

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def __delitem__(self, key: K) -> None:
        self.remove(key)

    def __contains__(self, key: Any) -> bool:
        return self.contains(key)

    def __iter__(self) -> Iterator[K]:
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.key

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"HashMap({{{pairs}}})"


class _LRUNode(Generic[K, V]):
    __slots__ = ("key", "next", "prev", "value")

    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.prev: Optional[_LRUNode[K, V]] = None
        self.next: Optional[_LRUNode[K, V]] = None


class LRUCache(Generic[K, V]):
    """Least Recently Used (LRU) Cache backed by a dict and a custom doubly linked list.

    Does not use OrderedDict or functools.lru_cache.

    Space: O(capacity).
    """

    def __init__(self, capacity: int) -> None:
        """Initialize an LRU cache with fixed maximum capacity.

        Args:
            capacity: Maximum number of elements to cache (must be >= 1).

        Raises:
            ValueError: if capacity is less than 1.

        Space: O(capacity).
        """
        if capacity < 1:
            raise ValueError(f"capacity must be >= 1, got {capacity}")
        self._capacity: int = capacity
        self._cache: Dict[K, _LRUNode[K, V]] = {}
        self._head: _LRUNode[K, V] = _LRUNode(None, None)
        self._tail: _LRUNode[K, V] = _LRUNode(None, None)
        self._head.next = self._tail
        self._tail.prev = self._head

    def _remove_node(self, node: _LRUNode[K, V]) -> None:
        prev_node = node.prev
        next_node = node.next
        if prev_node is not None:
            prev_node.next = next_node
        if next_node is not None:
            next_node.prev = prev_node

    def _add_to_front(self, node: _LRUNode[K, V]) -> None:
        node.next = self._head.next
        node.prev = self._head
        if self._head.next is not None:
            self._head.next.prev = node
        self._head.next = node

    def _move_to_front(self, node: _LRUNode[K, V]) -> None:
        self._remove_node(node)
        self._add_to_front(node)

    def get(self, key: K, default: Any = None) -> Any:
        """Retrieve the value for ``key`` and mark it as most recently used.

        Args:
            key: Key to look up.
            default: Fallback value if key is not found.

        Returns:
            The value associated with key, or default if missing.

        Time: O(1). Space: O(1).
        """
        if key not in self._cache:
            return default
        node = self._cache[key]
        self._move_to_front(node)
        return node.value

    def put(self, key: K, value: V) -> None:
        """Insert or update a key-value pair, evicting the LRU item if over capacity.

        Args:
            key: Key to insert or update.
            value: Value to store.

        Time: O(1). Space: O(1).
        """
        if key in self._cache:
            node = self._cache[key]
            node.value = value
            self._move_to_front(node)
            return

        node = _LRUNode(key, value)
        self._cache[key] = node
        self._add_to_front(node)

        if len(self._cache) > self._capacity:
            lru_node = self._tail.prev
            if lru_node is not None and lru_node is not self._head:
                self._remove_node(lru_node)
                del self._cache[lru_node.key]

    def keys(self) -> List[K]:
        """Return a list of keys ordered from most to least recently used.

        Time: O(n). Space: O(n).
        """
        result: List[K] = []
        curr = self._head.next
        while curr is not None and curr is not self._tail:
            result.append(curr.key)
            curr = curr.next
        return result

    def values(self) -> List[V]:
        """Return a list of values ordered from most to least recently used.

        Time: O(n). Space: O(n).
        """
        result: List[V] = []
        curr = self._head.next
        while curr is not None and curr is not self._tail:
            result.append(curr.value)
            curr = curr.next
        return result

    def items(self) -> List[Tuple[K, V]]:
        """Return a list of (key, value) pairs ordered from most to least recently used.

        Time: O(n). Space: O(n).
        """
        result: List[Tuple[K, V]] = []
        curr = self._head.next
        while curr is not None and curr is not self._tail:
            result.append((curr.key, curr.value))
            curr = curr.next
        return result

    def clear(self) -> None:
        """Remove all entries from the cache.

        Time: O(1). Space: O(1).
        """
        self._cache.clear()
        self._head.next = self._tail
        self._tail.prev = self._head

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, key: Any) -> bool:
        return key in self._cache

    def __getitem__(self, key: K) -> V:
        val = self.get(key, default=_MISSING)
        if val is _MISSING:
            raise KeyError(f"Key {key!r} not found in LRUCache")
        return cast(V, val)

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def __repr__(self) -> str:
        return f"LRUCache(capacity={self._capacity}, size={len(self._cache)})"
