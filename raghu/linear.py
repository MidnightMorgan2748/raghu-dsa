"""Linear data structures: Stack, Queue, Deque, SinglyLinkedList, DoublyLinkedList."""

from collections import deque as _deque
from typing import Any, Generic, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")

__all__ = ["Deque", "DoublyLinkedList", "Queue", "SinglyLinkedList", "Stack"]


class Stack(Generic[T]):
    """LIFO stack backed by a Python list.

    Space: O(n).
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._items: List[T] = list(items) if items is not None else []

    def push(self, item: T) -> None:
        """Push ``item`` on top. Time: O(1) amortized."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item. Time: O(1).

        Raises:
            IndexError: if the stack is empty.
        """
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it. Time: O(1).

        Raises:
            IndexError: if the stack is empty.
        """
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack has no items. Time: O(1)."""
        return not self._items

    def size(self) -> int:
        """Return the number of items. Time: O(1)."""
        return len(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(reversed(self._items))

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


class Queue(Generic[T]):
    """FIFO queue backed by ``collections.deque``.

    Space: O(n).
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._items: "_deque[T]" = _deque(items) if items is not None else _deque()

    def enqueue(self, item: T) -> None:
        """Add ``item`` to the back. Time: O(1)."""
        self._items.append(item)

    def dequeue(self) -> T:
        """Remove and return the front item. Time: O(1).

        Raises:
            IndexError: if the queue is empty.
        """
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def front(self) -> T:
        """Return the front item without removing it. Time: O(1).

        Raises:
            IndexError: if the queue is empty.
        """
        if not self._items:
            raise IndexError("front of empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        """Return True if the queue has no items. Time: O(1)."""
        return not self._items

    def size(self) -> int:
        """Return the number of items. Time: O(1)."""
        return len(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Queue({list(self._items)!r})"


class Deque(Generic[T]):
    """Double-ended queue backed by ``collections.deque``.

    Space: O(n).
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._items: "_deque[T]" = _deque(items) if items is not None else _deque()

    def append_left(self, item: T) -> None:
        """Add ``item`` to the left end. Time: O(1)."""
        self._items.appendleft(item)

    def append_right(self, item: T) -> None:
        """Add ``item`` to the right end. Time: O(1)."""
        self._items.append(item)

    def pop_left(self) -> T:
        """Remove and return the leftmost item. Time: O(1).

        Raises:
            IndexError: if the deque is empty.
        """
        if not self._items:
            raise IndexError("pop_left from empty deque")
        return self._items.popleft()

    def pop_right(self) -> T:
        """Remove and return the rightmost item. Time: O(1).

        Raises:
            IndexError: if the deque is empty.
        """
        if not self._items:
            raise IndexError("pop_right from empty deque")
        return self._items.pop()

    def peek_left(self) -> T:
        """Return the leftmost item without removing it. Time: O(1)."""
        if not self._items:
            raise IndexError("peek_left from empty deque")
        return self._items[0]

    def peek_right(self) -> T:
        """Return the rightmost item without removing it. Time: O(1)."""
        if not self._items:
            raise IndexError("peek_right from empty deque")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the deque has no items. Time: O(1)."""
        return not self._items

    def size(self) -> int:
        """Return the number of items. Time: O(1)."""
        return len(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Deque({list(self._items)!r})"


class _SNode(Generic[T]):
    __slots__ = ("next", "value")

    def __init__(self, value: T, next: "Optional[_SNode[T]]" = None) -> None:
        self.value = value
        self.next = next


class SinglyLinkedList(Generic[T]):
    """Singly linked list with head and tail pointers.

    Space: O(n).
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._head: Optional[_SNode[T]] = None
        self._tail: Optional[_SNode[T]] = None
        self._size = 0
        if items is not None:
            for item in items:
                self.insert_tail(item)

    def insert_head(self, value: T) -> None:
        """Insert ``value`` at the front. Time: O(1)."""
        node = _SNode(value, self._head)
        self._head = node
        if self._tail is None:
            self._tail = node
        self._size += 1

    def insert_tail(self, value: T) -> None:
        """Insert ``value`` at the end. Time: O(1)."""
        node = _SNode(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def delete(self, value: T) -> bool:
        """Delete the first node equal to ``value``. Time: O(n).

        Returns:
            True if a node was removed, False if ``value`` was not found.
        """
        prev: Optional[_SNode[T]] = None
        cur = self._head
        while cur is not None:
            if cur.value == value:
                if prev is None:
                    self._head = cur.next
                else:
                    prev.next = cur.next
                if cur is self._tail:
                    self._tail = prev
                self._size -= 1
                return True
            prev = cur
            cur = cur.next
        return False

    def search(self, value: T) -> bool:
        """Return True if ``value`` is in the list. Time: O(n)."""
        cur = self._head
        while cur is not None:
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def reverse(self) -> None:
        """Reverse the list in place. Time: O(n). Space: O(1)."""
        prev: Optional[_SNode[T]] = None
        cur = self._head
        self._tail = self._head
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self._head = prev

    def to_list(self) -> List[T]:
        """Return the values as a Python list. Time: O(n). Space: O(n)."""
        return list(self)

    def __iter__(self) -> Iterator[T]:
        cur = self._head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: Any) -> bool:
        return self.search(value)

    def __repr__(self) -> str:
        return f"SinglyLinkedList({self.to_list()!r})"


class _DNode(Generic[T]):
    __slots__ = ("next", "prev", "value")

    def __init__(self, value: T) -> None:
        self.value = value
        self.prev: Optional[_DNode[T]] = None
        self.next: Optional[_DNode[T]] = None


class DoublyLinkedList(Generic[T]):
    """Doubly linked list with head and tail pointers.

    Space: O(n).
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._head: Optional[_DNode[T]] = None
        self._tail: Optional[_DNode[T]] = None
        self._size = 0
        if items is not None:
            for item in items:
                self.insert_tail(item)

    def insert_head(self, value: T) -> None:
        """Insert ``value`` at the front. Time: O(1)."""
        node = _DNode(value)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def insert_tail(self, value: T) -> None:
        """Insert ``value`` at the end. Time: O(1)."""
        node = _DNode(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._size += 1

    def insert(self, index: int, value: T) -> None:
        """Insert ``value`` so that it ends up at position ``index``.

        Walks from whichever end is closer. Time: O(min(index, n - index)).

        Raises:
            IndexError: if ``index`` is outside ``0 <= index <= len(self)``.
        """
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        if index == 0:
            self.insert_head(value)
            return
        if index == self._size:
            self.insert_tail(value)
            return
        target = self._node_at(index)
        node = _DNode(value)
        before = target.prev
        node.prev = before
        node.next = target
        target.prev = node
        if before is not None:
            before.next = node
        self._size += 1

    def delete(self, value: T) -> bool:
        """Delete the first node equal to ``value``. Time: O(n).

        Returns:
            True if a node was removed, False if ``value`` was not found.
        """
        cur = self._head
        while cur is not None:
            if cur.value == value:
                self._unlink(cur)
                return True
            cur = cur.next
        return False

    def search(self, value: T) -> bool:
        """Return True if ``value`` is in the list. Time: O(n)."""
        cur = self._head
        while cur is not None:
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def traverse_forward(self) -> List[T]:
        """Return values from head to tail. Time: O(n). Space: O(n)."""
        return list(self)

    def traverse_backward(self) -> List[T]:
        """Return values from tail to head. Time: O(n). Space: O(n)."""
        return list(reversed(self))

    def to_list(self) -> List[T]:
        """Return the values as a Python list. Time: O(n). Space: O(n)."""
        return self.traverse_forward()

    def _node_at(self, index: int) -> _DNode[T]:
        if index <= self._size // 2:
            cur = self._head
            for _ in range(index):
                cur = cur.next  # type: ignore[union-attr]
        else:
            cur = self._tail
            for _ in range(self._size - 1 - index):
                cur = cur.prev  # type: ignore[union-attr]
        return cur  # type: ignore[return-value]

    def _unlink(self, node: _DNode[T]) -> None:
        if node.prev is None:
            self._head = node.next
        else:
            node.prev.next = node.next
        if node.next is None:
            self._tail = node.prev
        else:
            node.next.prev = node.prev
        self._size -= 1

    def __iter__(self) -> Iterator[T]:
        cur = self._head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __reversed__(self) -> Iterator[T]:
        cur = self._tail
        while cur is not None:
            yield cur.value
            cur = cur.prev

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: Any) -> bool:
        return self.search(value)

    def __repr__(self) -> str:
        return f"DoublyLinkedList({self.to_list()!r})"
