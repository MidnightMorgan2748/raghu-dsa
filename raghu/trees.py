"""Tree data structures: BinaryTree, BST, MinHeap, MaxHeap, Trie."""

from collections import deque as _deque
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

T = TypeVar("T")
KeyFunc = Optional[Callable[[Any], Any]]

__all__ = [
    "BST",
    "BinaryTree",
    "BinaryTreeNode",
    "MaxHeap",
    "MinHeap",
    "Trie",
]


class BinaryTreeNode(Generic[T]):
    """Node in a binary tree.

    Space: O(1).
    """

    def __init__(
        self,
        value: T,
        left: Optional["BinaryTreeNode[T]"] = None,
        right: Optional["BinaryTreeNode[T]"] = None,
    ) -> None:
        """Initialize a binary tree node.

        Args:
            value: Value stored in the node.
            left: Left child node.
            right: Right child node.

        Space: O(1).
        """
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"BinaryTreeNode({self.value!r})"


class BinaryTree(Generic[T]):
    """Binary tree with iterative traversals.

    Space: O(n).
    """

    Node = BinaryTreeNode

    def __init__(
        self,
        values: Optional[Union[Sequence[Optional[T]], BinaryTreeNode[T]]] = None,
    ) -> None:
        """Initialize a binary tree from an optional level-order sequence or root node.

        Args:
            values: Optional level-order sequence where None represents a missing
                child, or an existing BinaryTreeNode root.

        Space: O(n).
        """
        self.root: Optional[BinaryTreeNode[T]] = None
        if isinstance(values, BinaryTreeNode):
            self.root = values
        elif values is not None:
            self._build_from_level_order(values)

    def _build_from_level_order(self, values: Sequence[Optional[T]]) -> None:
        if not values or values[0] is None:
            return
        self.root = BinaryTreeNode(values[0])
        queue: _deque[BinaryTreeNode[T]] = _deque([self.root])
        i = 1
        n = len(values)
        while queue and i < n:
            curr = queue.popleft()
            if i < n:
                left_val = values[i]
                if left_val is not None:
                    curr.left = BinaryTreeNode(left_val)
                    queue.append(curr.left)
                i += 1
            if i < n:
                right_val = values[i]
                if right_val is not None:
                    curr.right = BinaryTreeNode(right_val)
                    queue.append(curr.right)
                i += 1

    def inorder(self) -> List[T]:
        """Return values in inorder traversal (left, root, right).

        Time: O(n). Space: O(n).
        """
        result: List[T] = []
        stack: List[BinaryTreeNode[T]] = []
        curr = self.root
        while curr is not None or stack:
            while curr is not None:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            result.append(curr.value)
            curr = curr.right
        return result

    def preorder(self) -> List[T]:
        """Return values in preorder traversal (root, left, right).

        Time: O(n). Space: O(n).
        """
        if self.root is None:
            return []
        result: List[T] = []
        stack: List[BinaryTreeNode[T]] = [self.root]
        while stack:
            curr = stack.pop()
            result.append(curr.value)
            if curr.right is not None:
                stack.append(curr.right)
            if curr.left is not None:
                stack.append(curr.left)
        return result

    def postorder(self) -> List[T]:
        """Return values in postorder traversal (left, right, root).

        Time: O(n). Space: O(n).
        """
        if self.root is None:
            return []
        result: List[T] = []
        stack: List[BinaryTreeNode[T]] = [self.root]
        while stack:
            curr = stack.pop()
            result.append(curr.value)
            if curr.left is not None:
                stack.append(curr.left)
            if curr.right is not None:
                stack.append(curr.right)
        return result[::-1]

    def level_order(self) -> List[T]:
        """Return values in level-order traversal.

        Time: O(n). Space: O(n).
        """
        if self.root is None:
            return []
        result: List[T] = []
        queue: _deque[BinaryTreeNode[T]] = _deque([self.root])
        while queue:
            curr = queue.popleft()
            result.append(curr.value)
            if curr.left is not None:
                queue.append(curr.left)
            if curr.right is not None:
                queue.append(curr.right)
        return result

    def height(self) -> int:
        """Return the height of the tree (number of levels, 0 for empty tree).

        Time: O(n). Space: O(w) where w is the maximum width of the tree.
        """
        if self.root is None:
            return 0
        h = 0
        queue: _deque[BinaryTreeNode[T]] = _deque([self.root])
        while queue:
            for _ in range(len(queue)):
                curr = queue.popleft()
                if curr.left is not None:
                    queue.append(curr.left)
                if curr.right is not None:
                    queue.append(curr.right)
            h += 1
        return h

    def size(self) -> int:
        """Return the number of nodes in the tree.

        Time: O(n). Space: O(w) where w is the maximum width of the tree.
        """
        if self.root is None:
            return 0
        count = 0
        queue: _deque[BinaryTreeNode[T]] = _deque([self.root])
        while queue:
            curr = queue.popleft()
            count += 1
            if curr.left is not None:
                queue.append(curr.left)
            if curr.right is not None:
                queue.append(curr.right)
        return count

    def __len__(self) -> int:
        return self.size()

    def __repr__(self) -> str:
        return f"BinaryTree({self.level_order()!r})"


class _BSTNode(Generic[T]):
    __slots__ = ("left", "right", "value")

    def __init__(
        self,
        value: T,
        left: Optional["_BSTNode[T]"] = None,
        right: Optional["_BSTNode[T]"] = None,
    ) -> None:
        self.value = value
        self.left = left
        self.right = right


class BST(Generic[T]):
    """Binary Search Tree supporting unique elements.

    Space: O(n).
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        """Initialize an empty or populated binary search tree.

        Args:
            items: Optional iterable of initial items to insert.

        Space: O(n).
        """
        self.root: Optional[_BSTNode[T]] = None
        self._size: int = 0
        if items is not None:
            for item in items:
                self.insert(item)

    def insert(self, value: T) -> None:
        """Insert ``value`` into the tree. Duplicates are ignored.

        Args:
            value: Value to insert.

        Time: O(h) where h is the tree height. Space: O(1).
        """
        if self.root is None:
            self.root = _BSTNode(value)
            self._size += 1
            return
        curr = self.root
        curr_val: Any
        while True:
            if value == curr.value:
                return
            curr_val = curr.value
            if value < curr_val:
                if curr.left is None:
                    curr.left = _BSTNode(value)
                    self._size += 1
                    return
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = _BSTNode(value)
                    self._size += 1
                    return
                curr = curr.right

    def search(self, value: T) -> bool:
        """Return True if ``value`` exists in the tree.

        Args:
            value: Value to look up.

        Time: O(h) where h is the tree height. Space: O(1).
        """
        curr = self.root
        curr_val: Any
        while curr is not None:
            if value == curr.value:
                return True
            curr_val = curr.value
            if value < curr_val:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def delete(self, value: T) -> bool:
        """Delete ``value`` from the tree if present.

        Args:
            value: Value to remove.

        Returns:
            True if an element was removed, False otherwise.

        Time: O(h) where h is the tree height. Space: O(1).
        """
        parent: Optional[_BSTNode[T]] = None
        curr = self.root
        curr_val: Any
        while curr is not None and curr.value != value:
            parent = curr
            curr_val = curr.value
            if value < curr_val:
                curr = curr.left
            else:
                curr = curr.right
        if curr is None:
            return False

        if curr.left is None or curr.right is None:
            child = curr.left if curr.left is not None else curr.right
            if parent is None:
                self.root = child
            elif parent.left is curr:
                parent.left = child
            else:
                parent.right = child
            self._size -= 1
            return True

        succ_parent = curr
        succ = curr.right
        while succ.left is not None:
            succ_parent = succ
            succ = succ.left

        curr.value = succ.value
        if succ_parent.left is succ:
            succ_parent.left = succ.right
        else:
            succ_parent.right = succ.right
        self._size -= 1
        return True

    def find_min(self) -> T:
        """Return the minimum value in the tree.

        Time: O(h) where h is the tree height. Space: O(1).

        Raises:
            IndexError: if the tree is empty.
        """
        if self.root is None:
            raise IndexError("find_min on empty BST")
        curr = self.root
        while curr.left is not None:
            curr = curr.left
        return curr.value

    def find_max(self) -> T:
        """Return the maximum value in the tree.

        Time: O(h) where h is the tree height. Space: O(1).

        Raises:
            IndexError: if the tree is empty.
        """
        if self.root is None:
            raise IndexError("find_max on empty BST")
        curr = self.root
        while curr.right is not None:
            curr = curr.right
        return curr.value

    def inorder(self) -> List[T]:
        """Return values in ascending sorted order via inorder traversal.

        Time: O(n). Space: O(n).
        """
        result: List[T] = []
        stack: List[_BSTNode[T]] = []
        curr = self.root
        while curr is not None or stack:
            while curr is not None:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            result.append(curr.value)
            curr = curr.right
        return result

    def height(self) -> int:
        """Return the height of the tree (number of levels, 0 for empty tree).

        Time: O(n). Space: O(w) where w is the maximum width of the tree.
        """
        if self.root is None:
            return 0
        h = 0
        queue: _deque[_BSTNode[T]] = _deque([self.root])
        while queue:
            for _ in range(len(queue)):
                curr = queue.popleft()
                if curr.left is not None:
                    queue.append(curr.left)
                if curr.right is not None:
                    queue.append(curr.right)
            h += 1
        return h

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: Any) -> bool:
        return self.search(value)

    def __iter__(self) -> Iterator[T]:
        stack: List[_BSTNode[T]] = []
        curr = self.root
        while curr is not None or stack:
            while curr is not None:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            yield curr.value
            curr = curr.right

    def __repr__(self) -> str:
        return f"BST({self.inorder()!r})"


class _Heap(Generic[T]):
    """Base class for array-backed binary heaps.

    Space: O(n).
    """

    def __init__(
        self,
        items: Optional[Iterable[T]] = None,
        key: KeyFunc = None,
    ) -> None:
        """Initialize an array-backed binary heap.

        Args:
            items: Optional initial elements to populate and heapify in O(n).
            key: Optional function to extract comparison key.

        Space: O(n).
        """
        self._data: List[T] = []
        self._key = key
        if items is not None:
            self._data = list(items)
            n = len(self._data)
            for i in range(n // 2 - 1, -1, -1):
                self._sift_down(i)

    @classmethod
    def heapify(cls, iterable: Iterable[T], key: KeyFunc = None) -> Any:
        """Create a new heap from ``iterable`` in O(n) time via sift-down.

        Args:
            iterable: Elements to heapify.
            key: Optional function to extract comparison key.

        Time: O(n). Space: O(n).
        """
        instance = cls(key=key)
        instance._data = list(iterable)
        n = len(instance._data)
        for i in range(n // 2 - 1, -1, -1):
            instance._sift_down(i)
        return instance

    def _eval_key(self, item: T) -> Any:
        return item if self._key is None else self._key(item)

    def _is_better(self, a: T, b: T) -> bool:
        raise NotImplementedError

    def push(self, item: T) -> None:
        """Insert ``item`` into the heap.

        Args:
            item: Item to insert.

        Time: O(log n). Space: O(1) amortized.
        """
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        """Remove and return the highest priority item.

        Time: O(log n). Space: O(1).

        Raises:
            IndexError: if the heap is empty.
        """
        if not self._data:
            raise IndexError("pop from empty heap")
        if len(self._data) == 1:
            return self._data.pop()
        top = self._data[0]
        self._data[0] = self._data.pop()
        self._sift_down(0)
        return top

    def peek(self) -> T:
        """Return the top item without removing it.

        Time: O(1). Space: O(1).

        Raises:
            IndexError: if the heap is empty.
        """
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def is_empty(self) -> bool:
        """Return True if the heap contains no elements.

        Time: O(1). Space: O(1).
        """
        return not self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent_idx = (idx - 1) // 2
            if self._is_better(self._data[idx], self._data[parent_idx]):
                self._data[idx], self._data[parent_idx] = (
                    self._data[parent_idx],
                    self._data[idx],
                )
                idx = parent_idx
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._data)
        while True:
            best_idx = idx
            left_idx = 2 * idx + 1
            right_idx = 2 * idx + 2
            if left_idx < n and self._is_better(
                self._data[left_idx], self._data[best_idx]
            ):
                best_idx = left_idx
            if right_idx < n and self._is_better(
                self._data[right_idx], self._data[best_idx]
            ):
                best_idx = right_idx
            if best_idx != idx:
                self._data[idx], self._data[best_idx] = (
                    self._data[best_idx],
                    self._data[idx],
                )
                idx = best_idx
            else:
                break


class MinHeap(_Heap[T]):
    """Binary min-heap where smallest element has highest priority.

    Space: O(n).
    """

    def _is_better(self, a: T, b: T) -> bool:
        return bool(self._eval_key(a) < self._eval_key(b))


class MaxHeap(_Heap[T]):
    """Binary max-heap where largest element has highest priority.

    Space: O(n).
    """

    def _is_better(self, a: T, b: T) -> bool:
        return bool(self._eval_key(a) > self._eval_key(b))


class _TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: Dict[str, _TrieNode] = {}
        self.is_end: bool = False


class Trie:
    """Prefix tree (trie) for string storage and prefix lookups.

    Space: O(total number of characters across all words).
    """

    def __init__(self, words: Optional[Iterable[str]] = None) -> None:
        """Initialize an empty or populated trie.

        Args:
            words: Optional iterable of strings to insert.

        Space: O(total length of all words).
        """
        self._root = _TrieNode()
        self._size = 0
        if words is not None:
            for word in words:
                self.insert(word)

    def insert(self, word: str) -> None:
        """Insert ``word`` into the trie.

        Args:
            word: String to insert.

        Time: O(m) where m is len(word). Space: O(m) worst case.
        """
        curr = self._root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = _TrieNode()
            curr = curr.children[ch]
        if not curr.is_end:
            curr.is_end = True
            self._size += 1

    def search(self, word: str) -> bool:
        """Return True if the exact ``word`` is in the trie.

        Args:
            word: String to search for.

        Time: O(m) where m is len(word). Space: O(1).
        """
        curr = self._root
        for ch in word:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return curr.is_end

    def starts_with(self, prefix: str) -> bool:
        """Return True if any word in the trie starts with ``prefix``.

        Args:
            prefix: String prefix to look for.

        Time: O(p) where p is len(prefix). Space: O(1).
        """
        if self._size == 0:
            return False
        curr = self._root
        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return True

    def __len__(self) -> int:
        return self._size

    def __contains__(self, word: Any) -> bool:
        if not isinstance(word, str):
            return False
        return self.search(word)

    def __repr__(self) -> str:
        return f"Trie(size={self._size})"
