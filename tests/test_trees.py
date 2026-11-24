import heapq
import random

import pytest

import raghu
from raghu import (
    BST,
    BinaryTree,
    BinaryTreeNode,
    MaxHeap,
    MinHeap,
    Trie,
)


class TestBinaryTree:
    def test_empty_tree(self):
        tree = BinaryTree()
        assert tree.inorder() == []
        assert tree.preorder() == []
        assert tree.postorder() == []
        assert tree.level_order() == []
        assert tree.height() == 0
        assert tree.size() == 0
        assert len(tree) == 0

    def test_single_node(self):
        tree = BinaryTree([10])
        assert tree.inorder() == [10]
        assert tree.preorder() == [10]
        assert tree.postorder() == [10]
        assert tree.level_order() == [10]
        assert tree.height() == 1
        assert tree.size() == 1
        assert len(tree) == 1

    def test_level_order_construction_and_traversals(self):
        tree = BinaryTree([1, 2, 3, None, 4, 5, 6])
        assert tree.level_order() == [1, 2, 3, 4, 5, 6]
        assert tree.inorder() == [2, 4, 1, 5, 3, 6]
        assert tree.preorder() == [1, 2, 4, 3, 5, 6]
        assert tree.postorder() == [4, 2, 5, 6, 3, 1]
        assert tree.height() == 3
        assert tree.size() == 6

    def test_manual_node_construction(self):
        root = BinaryTree.Node(1, BinaryTree.Node(2), BinaryTree.Node(3))
        tree = BinaryTree(root)
        assert tree.inorder() == [2, 1, 3]
        assert tree.height() == 2
        assert tree.size() == 3

    def test_deep_skewed_tree_no_recursion_error(self):
        root = BinaryTreeNode(0)
        curr = root
        for i in range(1, 5000):
            curr.right = BinaryTreeNode(i)
            curr = curr.right
        tree = BinaryTree(root)
        assert tree.height() == 5000
        assert tree.size() == 5000
        assert tree.inorder() == list(range(5000))
        assert tree.preorder() == list(range(5000))
        assert tree.postorder() == list(range(4999, -1, -1))
        assert tree.level_order() == list(range(5000))


class TestBST:
    def test_empty_tree_and_errors(self):
        bst = BST()
        assert len(bst) == 0
        assert bst.height() == 0
        assert bst.inorder() == []
        assert list(bst) == []
        with pytest.raises(IndexError):
            bst.find_min()
        with pytest.raises(IndexError):
            bst.find_max()
        assert not bst.search(1)
        assert 1 not in bst
        assert not bst.delete(1)

    def test_single_node(self):
        bst = BST([42])
        assert len(bst) == 1
        assert bst.height() == 1
        assert bst.find_min() == 42
        assert bst.find_max() == 42
        assert 42 in bst
        assert bst.delete(42)
        assert len(bst) == 0
        assert bst.inorder() == []

    def test_insert_and_duplicate_ignored(self):
        bst = BST([5, 3, 7, 3, 5, 7, 2, 8])
        assert bst.inorder() == [2, 3, 5, 7, 8]
        assert len(bst) == 5
        assert list(bst) == [2, 3, 5, 7, 8]

    def test_delete_leaf_one_child_two_children(self):
        bst = BST([5, 3, 8, 2, 4, 7, 9, 6])
        assert bst.delete(2)
        assert 2 not in bst
        assert bst.inorder() == [3, 4, 5, 6, 7, 8, 9]

        assert bst.delete(7)
        assert 7 not in bst
        assert bst.inorder() == [3, 4, 5, 6, 8, 9]

        assert bst.delete(5)
        assert 5 not in bst
        assert bst.inorder() == [3, 4, 6, 8, 9]

        assert bst.delete(8)
        assert 8 not in bst
        assert bst.inorder() == [3, 4, 6, 9]

        assert not bst.delete(999)
        assert len(bst) == 4

    def test_randomized_inorder_matches_sorted_set(self):
        rng = random.Random(42)
        for _ in range(10):
            data = [rng.randint(-500, 500) for _ in range(100)]
            bst = BST(data)
            expected = sorted(set(data))
            assert bst.inorder() == expected
            assert list(bst) == expected
            assert len(bst) == len(expected)
            assert bst.find_min() == expected[0]
            assert bst.find_max() == expected[-1]
            for val in expected:
                assert val in bst
            assert 99999 not in bst

    def test_randomized_deletions(self):
        rng = random.Random(123)
        data = list(range(100))
        rng.shuffle(data)
        bst = BST(data)
        active = set(data)

        to_delete = rng.sample(data, 50)
        for val in to_delete:
            assert bst.delete(val)
            assert not bst.delete(val)
            active.remove(val)
            assert val not in bst

        assert bst.inorder() == sorted(active)
        assert len(bst) == len(active)

    def test_deep_skewed_bst_no_recursion_error(self):
        bst = BST(range(5000))
        assert len(bst) == 5000
        assert bst.height() == 5000
        assert bst.find_min() == 0
        assert bst.find_max() == 4999
        assert 2500 in bst
        assert bst.delete(2500)
        assert 2500 not in bst
        assert len(bst) == 4999
        assert bst.inorder() == [i for i in range(5000) if i != 2500]


class TestHeaps:
    @pytest.mark.parametrize("heap_cls", [MinHeap, MaxHeap])
    def test_empty_heap_errors(self, heap_cls):
        heap = heap_cls()
        assert heap.is_empty()
        assert len(heap) == 0
        with pytest.raises(IndexError):
            heap.pop()
        with pytest.raises(IndexError):
            heap.peek()

    def test_min_heap_operations(self):
        h = MinHeap()
        values = [5, 3, 8, 1, 4]
        for v in values:
            h.push(v)
        assert not h.is_empty()
        assert len(h) == 5
        assert h.peek() == 1
        popped = [h.pop() for _ in range(5)]
        assert popped == [1, 3, 4, 5, 8]
        assert h.is_empty()

    def test_max_heap_operations(self):
        h = MaxHeap()
        values = [5, 3, 8, 1, 4]
        for v in values:
            h.push(v)
        assert not h.is_empty()
        assert len(h) == 5
        assert h.peek() == 8
        popped = [h.pop() for _ in range(5)]
        assert popped == [8, 5, 4, 3, 1]
        assert h.is_empty()

    def test_heapify_classmethod(self):
        data = [9, 3, 7, 1, 6, 2, 8]
        min_h = MinHeap.heapify(data)
        assert [min_h.pop() for _ in range(len(data))] == sorted(data)

        max_h = MaxHeap.heapify(data)
        assert [max_h.pop() for _ in range(len(data))] == sorted(data, reverse=True)

    def test_key_function(self):
        words = ["banana", "apple", "fig", "kiwi", "pear"]
        min_h = MinHeap(words, key=len)
        assert len(min_h.peek()) == 3
        popped_min = [min_h.pop() for _ in range(len(words))]
        assert [len(w) for w in popped_min] == sorted([len(w) for w in words])

        max_h = MaxHeap(words, key=len)
        assert len(max_h.peek()) == 6
        popped_max = [max_h.pop() for _ in range(len(words))]
        assert [len(w) for w in popped_max] == sorted([len(w) for w in words], reverse=True)

    def test_randomized_comparison_against_heapq(self):
        rng = random.Random(777)
        for _ in range(10):
            data = [rng.randint(-1000, 1000) for _ in range(200)]
            ref = list(data)
            heapq.heapify(ref)
            ref_sorted = [heapq.heappop(ref) for _ in range(len(data))]

            min_h = MinHeap.heapify(data)
            assert [min_h.pop() for _ in range(len(data))] == ref_sorted

            max_h = MaxHeap.heapify(data)
            assert [max_h.pop() for _ in range(len(data))] == sorted(data, reverse=True)

    def test_large_heap_performance(self):
        data = list(range(5000))
        random.Random(99).shuffle(data)
        min_h = MinHeap.heapify(data)
        assert len(min_h) == 5000
        assert min_h.peek() == 0
        for expected in range(5000):
            assert min_h.pop() == expected


class TestTrie:
    def test_empty_trie(self):
        t = Trie()
        assert len(t) == 0
        assert not t.search("a")
        assert not t.starts_with("a")
        assert "a" not in t
        assert not t.search("")
        assert not t.starts_with("")
        assert "" not in t

    def test_empty_string(self):
        t = Trie()
        t.insert("")
        assert len(t) == 1
        assert t.search("")
        assert "" in t
        assert t.starts_with("")
        assert not t.search("a")
        assert not t.starts_with("a")

    def test_overlapping_prefixes(self):
        words = ["app", "apple", "application", "apt", "bat", "batch", "bath"]
        t = Trie(words)
        assert len(t) == 7

        for word in words:
            assert t.search(word)
            assert word in t

        assert t.starts_with("ap")
        assert t.starts_with("app")
        assert t.starts_with("appl")
        assert t.starts_with("application")
        assert t.starts_with("apt")
        assert t.starts_with("ba")
        assert t.starts_with("bat")
        assert t.starts_with("batch")
        assert t.starts_with("bath")

        assert not t.starts_with("baz")
        assert not t.starts_with("c")
        assert not t.search("ap")
        assert not t.search("appl")
        assert "appl" not in t
        assert 123 not in t

    def test_duplicate_inserts(self):
        t = Trie(["hello", "hello", "world", "world"])
        assert len(t) == 2
        t.insert("hello")
        assert len(t) == 2


def test_top_level_exports():
    expected_names = [
        "BinaryTreeNode",
        "BinaryTree",
        "BST",
        "MinHeap",
        "MaxHeap",
        "Trie",
    ]
    for name in expected_names:
        assert name in raghu.__all__
        assert hasattr(raghu, name)
    assert hasattr(raghu, "__version__")
