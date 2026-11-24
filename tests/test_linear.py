import pytest

import raghu
from raghu import Deque, DoublyLinkedList, Queue, SinglyLinkedList, Stack


class TestStack:
    def test_push_pop_lifo(self):
        s = Stack()
        for i in range(3):
            s.push(i)
        assert [s.pop(), s.pop(), s.pop()] == [2, 1, 0]

    def test_peek_does_not_remove(self):
        s = Stack([1, 2])
        assert s.peek() == 2
        assert s.size() == 2

    def test_is_empty_and_size(self):
        s = Stack()
        assert s.is_empty() and s.size() == 0 and len(s) == 0
        s.push("a")
        assert not s.is_empty() and s.size() == 1

    def test_empty_errors(self):
        s = Stack()
        with pytest.raises(IndexError):
            s.pop()
        with pytest.raises(IndexError):
            s.peek()

    def test_iter_top_first(self):
        assert list(Stack([1, 2, 3])) == [3, 2, 1]


class TestQueue:
    def test_fifo(self):
        q = Queue()
        for i in range(3):
            q.enqueue(i)
        assert [q.dequeue(), q.dequeue(), q.dequeue()] == [0, 1, 2]

    def test_front_does_not_remove(self):
        q = Queue([5, 6])
        assert q.front() == 5
        assert q.size() == 2

    def test_is_empty(self):
        q = Queue()
        assert q.is_empty()
        q.enqueue(1)
        assert not q.is_empty()

    def test_empty_errors(self):
        q = Queue()
        with pytest.raises(IndexError):
            q.dequeue()
        with pytest.raises(IndexError):
            q.front()


class TestDeque:
    def test_both_ends(self):
        d = Deque()
        d.append_right(2)
        d.append_right(3)
        d.append_left(1)
        assert list(d) == [1, 2, 3]
        assert d.pop_left() == 1
        assert d.pop_right() == 3
        assert d.size() == 1

    def test_peek(self):
        d = Deque([1, 2, 3])
        assert d.peek_left() == 1
        assert d.peek_right() == 3
        assert len(d) == 3

    def test_empty_errors(self):
        d = Deque()
        assert d.is_empty()
        for method in (d.pop_left, d.pop_right, d.peek_left, d.peek_right):
            with pytest.raises(IndexError):
                method()


class TestSinglyLinkedList:
    def test_insert_head_and_tail(self):
        ll = SinglyLinkedList()
        ll.insert_tail(2)
        ll.insert_head(1)
        ll.insert_tail(3)
        assert ll.to_list() == [1, 2, 3]
        assert len(ll) == 3

    def test_delete_head_middle_tail(self):
        ll = SinglyLinkedList([1, 2, 3, 4])
        assert ll.delete(1)
        assert ll.delete(3)
        assert ll.delete(4)
        assert ll.to_list() == [2]
        ll.insert_tail(9)
        assert ll.to_list() == [2, 9]

    def test_delete_missing_and_only_element(self):
        ll = SinglyLinkedList([1])
        assert not ll.delete(7)
        assert ll.delete(1)
        assert ll.to_list() == [] and len(ll) == 0
        ll.insert_tail(5)
        ll.insert_head(4)
        assert ll.to_list() == [4, 5]

    def test_delete_removes_first_occurrence_only(self):
        ll = SinglyLinkedList([1, 2, 1])
        ll.delete(1)
        assert ll.to_list() == [2, 1]

    def test_search(self):
        ll = SinglyLinkedList([1, 2, 3])
        assert ll.search(2)
        assert not ll.search(9)
        assert 3 in ll

    def test_reverse(self):
        ll = SinglyLinkedList([1, 2, 3])
        ll.reverse()
        assert ll.to_list() == [3, 2, 1]
        ll.insert_tail(0)
        assert ll.to_list() == [3, 2, 1, 0]

    def test_reverse_empty_and_single(self):
        ll = SinglyLinkedList()
        ll.reverse()
        assert ll.to_list() == []
        ll.insert_head(1)
        ll.reverse()
        assert ll.to_list() == [1]


class TestDoublyLinkedList:
    def test_insert_head_and_tail(self):
        dl = DoublyLinkedList()
        dl.insert_tail(2)
        dl.insert_head(1)
        dl.insert_tail(3)
        assert dl.traverse_forward() == [1, 2, 3]
        assert dl.traverse_backward() == [3, 2, 1]

    @pytest.mark.parametrize("index,expected", [
        (0, [9, 1, 2, 3, 4]),
        (1, [1, 9, 2, 3, 4]),
        (2, [1, 2, 9, 3, 4]),
        (3, [1, 2, 3, 9, 4]),
        (4, [1, 2, 3, 4, 9]),
    ])
    def test_insert_at_index(self, index, expected):
        dl = DoublyLinkedList([1, 2, 3, 4])
        dl.insert(index, 9)
        assert dl.traverse_forward() == expected
        assert dl.traverse_backward() == expected[::-1]
        assert len(dl) == 5

    def test_insert_out_of_range(self):
        dl = DoublyLinkedList([1])
        with pytest.raises(IndexError):
            dl.insert(5, 0)
        with pytest.raises(IndexError):
            dl.insert(-1, 0)

    def test_insert_into_empty(self):
        dl = DoublyLinkedList()
        dl.insert(0, 1)
        assert dl.to_list() == [1]

    def test_delete_keeps_links_consistent(self):
        dl = DoublyLinkedList([1, 2, 3, 4])
        assert dl.delete(1)
        assert dl.delete(4)
        assert dl.delete(3)
        assert dl.traverse_forward() == [2]
        assert dl.traverse_backward() == [2]
        assert dl.delete(2)
        assert dl.to_list() == [] and dl.traverse_backward() == []
        assert not dl.delete(2)
        dl.insert_tail(7)
        dl.insert_head(6)
        assert dl.traverse_backward() == [7, 6]

    def test_search_and_contains(self):
        dl = DoublyLinkedList([1, 2, 3])
        assert dl.search(3) and 2 in dl
        assert not dl.search(0)


def test_top_level_exports():
    for name in ("Stack", "Queue", "Deque", "SinglyLinkedList", "DoublyLinkedList"):
        assert name in raghu.__all__
        assert hasattr(raghu, name)
