import random
from collections import OrderedDict
from typing import Any, List

import pytest

import raghu
from raghu import HashMap, LRUCache


class CollisionKey:
    def __init__(self, val: int) -> None:
        self.val = val

    def __hash__(self) -> int:
        return 42

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CollisionKey):
            return self.val == other.val
        return False

    def __repr__(self) -> str:
        return f"CollisionKey({self.val})"


class ReferenceLRU:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: OrderedDict = OrderedDict()

    def get(self, key: Any, default: Any = None) -> Any:
        if key not in self.data:
            return default
        self.data.move_to_end(key, last=False)
        return self.data[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self.data:
            self.data[key] = value
            self.data.move_to_end(key, last=False)
        else:
            self.data[key] = value
            self.data.move_to_end(key, last=False)
            if len(self.data) > self.capacity:
                self.data.popitem(last=True)

    def keys(self) -> List[Any]:
        return list(self.data.keys())


class TestHashMap:
    def test_basic_crud_and_operators(self):
        hm = HashMap()
        assert len(hm) == 0
        hm.put("a", 10)
        hm["b"] = 20
        assert len(hm) == 2
        assert hm.get("a") == 10
        assert hm["b"] == 20
        assert "a" in hm
        assert hm.contains("b")
        assert "c" not in hm

        hm["a"] = 100
        assert hm["a"] == 100
        assert len(hm) == 2

        assert hm.get("missing", default="fallback") == "fallback"
        with pytest.raises(KeyError):
            hm.get("missing")
        with pytest.raises(KeyError):
            _ = hm["missing"]

        assert hm.remove("a") == 100
        assert "a" not in hm
        assert len(hm) == 1
        with pytest.raises(KeyError):
            hm.remove("a")

        del hm["b"]
        assert len(hm) == 0
        with pytest.raises(KeyError):
            del hm["b"]

    def test_keys_values_items_iter_clear(self):
        pairs = [(1, "one"), (2, "two"), (3, "three")]
        hm = HashMap(pairs)
        assert len(hm) == 3
        assert set(hm.keys()) == {1, 2, 3}
        assert set(hm.values()) == {"one", "two", "three"}
        assert set(hm.items()) == {(1, "one"), (2, "two"), (3, "three")}
        assert set(iter(hm)) == {1, 2, 3}

        hm.clear()
        assert len(hm) == 0
        assert hm.keys() == []
        assert hm.values() == []
        assert hm.items() == []

    def test_heavy_collisions_constant_hash(self):
        hm = HashMap()
        keys = [CollisionKey(i) for i in range(100)]
        for i, k in enumerate(keys):
            hm[k] = i * 10
        assert len(hm) == 100

        for i, k in enumerate(keys):
            assert hm[k] == i * 10
            assert k in hm

        for i in range(0, 100, 2):
            hm[keys[i]] = i * 100
        assert len(hm) == 100
        for i in range(0, 100, 2):
            assert hm[keys[i]] == i * 100

        for i in range(0, 50):
            del hm[keys[i]]
        assert len(hm) == 50
        for i in range(0, 50):
            assert keys[i] not in hm
        for i in range(50, 100):
            assert keys[i] in hm

    def test_forced_resizes(self):
        hm = HashMap()
        n = 600
        for i in range(n):
            hm[i] = i * 2
        assert len(hm) == n
        for i in range(n):
            assert hm[i] == i * 2

    def test_randomized_comparison_against_dict(self):
        rng = random.Random(42)
        hm = HashMap()
        reference = {}
        keys_pool = list(range(100))

        for _ in range(1000):
            op = rng.choice(["put", "get", "remove", "contains"])
            k = rng.choice(keys_pool)
            if op == "put":
                val = rng.randint(0, 10000)
                hm[k] = val
                reference[k] = val
            elif op == "get":
                if k in reference:
                    assert hm[k] == reference[k]
                    assert hm.get(k) == reference.get(k)
                else:
                    assert hm.get(k, None) is None
                    with pytest.raises(KeyError):
                        _ = hm[k]
            elif op == "remove":
                if k in reference:
                    assert hm.remove(k) == reference.pop(k)
                else:
                    with pytest.raises(KeyError):
                        hm.remove(k)
            elif op == "contains":
                assert (k in hm) == (k in reference)

            assert len(hm) == len(reference)

        assert sorted(hm.keys()) == sorted(reference.keys())
        assert sorted(hm.items()) == sorted(reference.items())


class TestLRUCache:
    def test_invalid_capacity(self):
        with pytest.raises(ValueError):
            LRUCache(0)
        with pytest.raises(ValueError):
            LRUCache(-1)

    def test_capacity_one(self):
        cache = LRUCache(1)
        assert len(cache) == 0
        cache.put("a", 1)
        assert len(cache) == 1
        assert cache.get("a") == 1
        assert cache.keys() == ["a"]

        cache.put("b", 2)
        assert len(cache) == 1
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.keys() == ["b"]

        cache.put("b", 20)
        assert len(cache) == 1
        assert cache.get("b") == 20
        assert cache.keys() == ["b"]

    def test_eviction_order(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.keys() == ["c", "b", "a"]

        cache.put("d", 4)
        assert cache.keys() == ["d", "c", "b"]
        assert cache.get("a") is None
        assert "a" not in cache

    def test_update_refreshes_recency(self):
        cache = LRUCache(3)
        cache.put(1, "one")
        cache.put(2, "two")
        cache.put(3, "three")
        assert cache.keys() == [3, 2, 1]

        cache.put(1, "ONE")
        assert cache.keys() == [1, 3, 2]

        cache.put(4, "four")
        assert cache.keys() == [4, 1, 3]
        assert 2 not in cache
        assert cache.get(2) is None
        assert cache.get(1) == "ONE"

    def test_get_refreshes_recency(self):
        cache = LRUCache(3)
        cache.put("x", 10)
        cache.put("y", 20)
        cache.put("z", 30)
        assert cache.keys() == ["z", "y", "x"]

        assert cache.get("x") == 10
        assert cache.keys() == ["x", "z", "y"]

        cache.put("w", 40)
        assert cache.keys() == ["w", "x", "z"]
        assert "y" not in cache

    def test_contains_does_not_refresh_recency(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.keys() == ["c", "b", "a"]

        assert "a" in cache
        assert cache.keys() == ["c", "b", "a"]

        cache.put("d", 4)
        assert cache.keys() == ["d", "c", "b"]
        assert "a" not in cache

    def test_clear_and_len(self):
        cache = LRUCache(3)
        cache.put("k1", 100)
        cache.put("k2", 200)
        assert len(cache) == 2
        cache.clear()
        assert len(cache) == 0
        assert cache.keys() == []
        assert cache.values() == []
        assert cache.items() == []
        assert cache.get("k1") is None

    def test_randomized_comparison_against_ordered_dict(self):
        rng = random.Random(999)
        cap = 8
        cache = LRUCache(cap)
        reference = ReferenceLRU(cap)
        keys_pool = list(range(20))

        for _ in range(1000):
            op = rng.choice(["put", "get", "contains", "len", "keys"])
            k = rng.choice(keys_pool)
            if op == "put":
                v = rng.randint(0, 1000)
                cache.put(k, v)
                reference.put(k, v)
            elif op == "get":
                assert cache.get(k) == reference.get(k)
            elif op == "contains":
                assert (k in cache) == (k in reference.data)
            elif op == "len":
                assert len(cache) == len(reference.data)
            elif op == "keys":
                assert cache.keys() == reference.keys()

            assert cache.keys() == reference.keys()
            assert len(cache) == len(reference.data)


def test_top_level_exports():
    expected_names = [
        "HashMap",
        "LRUCache",
    ]
    for name in expected_names:
        assert name in raghu.__all__
        assert hasattr(raghu, name)
    assert hasattr(raghu, "__version__")
