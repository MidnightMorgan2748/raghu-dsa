import random

import pytest

import raghu
from raghu import (
    binary_search,
    bubble_sort,
    heap_sort,
    insertion_sort,
    linear_search,
    merge_sort,
    quick_sort,
    selection_sort,
)

ALL_SORTS = [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort]
STABLE_SORTS = [bubble_sort, insertion_sort, merge_sort]


def random_lists():
    rng = random.Random(1234)
    yield []
    yield [1]
    yield [2, 1]
    yield list(range(50))
    yield list(range(50, 0, -1))
    yield [7] * 30
    for n in (3, 10, 57, 200):
        yield [rng.randint(-20, 20) for _ in range(n)]


class TestLinearSearch:
    def test_found_first_occurrence(self):
        assert linear_search([4, 5, 6, 5], 5) == 1

    def test_missing_and_empty(self):
        assert linear_search([1, 2], 3) == -1
        assert linear_search([], 1) == -1

    def test_works_on_strings_and_tuples(self):
        assert linear_search("hello", "l") == 2
        assert linear_search((1, 2, 3), 3) == 2


@pytest.mark.parametrize("recursive", [False, True])
class TestBinarySearch:
    def test_finds_every_element(self, recursive):
        arr = list(range(0, 100, 3))
        for i, v in enumerate(arr):
            assert binary_search(arr, v, recursive=recursive) == i

    def test_missing_values(self, recursive):
        arr = [1, 3, 5, 7]
        for target in (0, 2, 4, 8):
            assert binary_search(arr, target, recursive=recursive) == -1

    def test_empty_and_single(self, recursive):
        assert binary_search([], 1, recursive=recursive) == -1
        assert binary_search([1], 1, recursive=recursive) == 0
        assert binary_search([1], 2, recursive=recursive) == -1

    def test_duplicates_return_valid_index(self, recursive):
        arr = [1, 2, 2, 2, 3]
        assert arr[binary_search(arr, 2, recursive=recursive)] == 2

    def test_strings(self, recursive):
        arr = ["a", "c", "e"]
        assert binary_search(arr, "c", recursive=recursive) == 1


@pytest.mark.parametrize("sort", ALL_SORTS)
class TestSorts:
    def test_matches_builtin(self, sort):
        for data in random_lists():
            assert sort(data) == sorted(data)

    def test_does_not_mutate_input(self, sort):
        data = [3, 1, 2]
        result = sort(data)
        assert data == [3, 1, 2]
        assert result is not data

    def test_key_function(self, sort):
        words = ["pear", "fig", "banana", "kiwi", "apple"]
        result = sort(words, key=len)
        assert [len(w) for w in result] == sorted(len(w) for w in words)

    def test_strings_and_floats(self, sort):
        assert sort(["b", "a", "c"]) == ["a", "b", "c"]
        assert sort([2.5, -1.0, 0.0]) == [-1.0, 0.0, 2.5]

    def test_accepts_tuple_input(self, sort):
        assert sort((3, 2, 1)) == [1, 2, 3]


@pytest.mark.parametrize("sort", STABLE_SORTS)
def test_stability(sort):
    rng = random.Random(99)
    pairs = [(rng.randint(0, 5), i) for i in range(100)]
    assert sort(pairs, key=lambda p: p[0]) == sorted(pairs, key=lambda p: p[0])


def test_quick_sort_many_duplicates_and_sorted_input():
    assert quick_sort([5] * 5000) == [5] * 5000
    data = list(range(5000))
    assert quick_sort(data) == data
    assert quick_sort(data[::-1]) == data


def test_top_level_exports():
    names = [
        "linear_search", "binary_search", "bubble_sort", "selection_sort",
        "insertion_sort", "merge_sort", "quick_sort", "heap_sort",
    ]
    for name in names:
        assert name in raghu.__all__
        assert hasattr(raghu, name)
