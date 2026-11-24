import random
from collections import deque
from typing import Dict, List, Set, Tuple

import pytest

import raghu
from raghu import (
    Graph,
    UnionFind,
    bfs,
    dfs,
    dijkstra,
    has_cycle,
    shortest_path,
    topological_sort,
)


class TestGraph:
    def test_vertex_and_edge_crud(self):
        g = Graph(directed=False)
        assert len(g) == 0
        g.add_vertex("A")
        assert "A" in g
        assert g.has_vertex("A")
        assert not g.has_vertex("B")
        assert g.vertices() == ["A"]

        g.add_edge("A", "B", weight=3.5)
        assert len(g) == 2
        assert g.has_vertex("B")
        assert g.has_edge("A", "B")
        assert g.has_edge("B", "A")
        assert "B" in g.neighbors("A")
        assert "A" in g.neighbors("B")

        edges = g.edges()
        assert len(edges) == 1
        assert edges[0] in [("A", "B", 3.5), ("B", "A", 3.5)]

        assert g.remove_edge("A", "B")
        assert not g.has_edge("A", "B")
        assert not g.has_edge("B", "A")
        assert len(g.edges()) == 0

        assert g.remove_vertex("A")
        assert not g.has_vertex("A")
        assert not g.remove_vertex("A")
        assert len(g) == 1

    def test_directed_graph_edges(self):
        g = Graph(directed=True)
        g.add_edge("X", "Y")
        assert g.has_edge("X", "Y")
        assert not g.has_edge("Y", "X")
        assert g.edges() == [("X", "Y")]
        assert g.remove_edge("X", "Y")
        assert not g.has_edge("X", "Y")

    def test_neighbors_missing_vertex_raises(self):
        g = Graph()
        with pytest.raises(KeyError):
            g.neighbors("missing")

    def test_to_adjacency_list(self):
        g = Graph(directed=True)
        g.add_edge(1, 2)
        assert g.to_adjacency_list() == {1: [2], 2: []}
        assert g.to_adjacency_list(weighted=False) == {1: [2], 2: []}
        assert g.to_adjacency_list(weighted=True) == {1: [(2, 1.0)], 2: []}

        gw = Graph(directed=True)
        gw.add_edge(1, 2, 4.5)
        assert gw.to_adjacency_list() == {1: [(2, 4.5)], 2: []}
        assert gw.to_adjacency_list(weighted=False) == {1: [2], 2: []}

    def test_oop_delegation_methods(self):
        g = Graph(directed=True)
        g.add_edge(1, 2, 2.0)
        g.add_edge(2, 3, 3.0)
        assert g.bfs(1) == [1, 2, 3]
        assert g.dfs(1) == [1, 2, 3]
        assert not g.has_cycle()
        assert g.topological_sort() == [1, 2, 3]
        dist, pred = g.dijkstra(1)
        assert dist[3] == 5.0
        assert pred[3] == 2
        assert g.shortest_path(1, 3) == [1, 2, 3]


class TestBFSDFS:
    def test_bfs_dfs_known_graph(self):
        adj = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F"],
            "D": [],
            "E": ["F"],
            "F": [],
        }
        assert bfs(adj, "A") == ["A", "B", "C", "D", "E", "F"]
        assert dfs(adj, "A") == ["A", "B", "D", "E", "F", "C"]

    def test_bfs_dfs_disconnected_and_missing(self):
        adj = {1: [2], 2: [], 3: [4], 4: []}
        assert bfs(adj, 1) == [1, 2]
        assert dfs(adj, 1) == [1, 2]
        assert bfs(adj, 3) == [3, 4]
        assert dfs(adj, 3) == [3, 4]
        assert bfs(adj, 99) == []
        assert dfs(adj, 99) == []

    def test_bfs_dfs_weighted_adj_list(self):
        adj = {"A": [("B", 1.5), ("C", 2.0)], "B": [], "C": []}
        assert bfs(adj, "A") == ["A", "B", "C"]
        assert dfs(adj, "A") == ["A", "B", "C"]


class TestCycleDetection:
    def test_self_loops(self):
        adj = {1: [1]}
        assert has_cycle(adj, directed=True)
        assert has_cycle(adj, directed=False)

    def test_classic_diamond_undirected_vs_directed(self):
        directed_adj = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        assert not has_cycle(directed_adj, directed=True)

        undirected_adj = {
            "A": ["B", "C"],
            "B": ["A", "D"],
            "C": ["A", "D"],
            "D": ["B", "C"],
        }
        assert has_cycle(undirected_adj, directed=False)

    def test_two_node_back_and_forth(self):
        directed_cycle = {1: [2], 2: [1]}
        assert has_cycle(directed_cycle, directed=True)

        undirected_edge = {1: [2], 2: [1]}
        assert not has_cycle(undirected_edge, directed=False)

    def test_disconnected_cycle(self):
        adj = {
            1: [2],
            2: [],
            3: [4],
            4: [5],
            5: [3],
        }
        assert has_cycle(adj, directed=True)

        undirected_adj = {
            1: [2],
            2: [1],
            3: [4, 5],
            4: [3, 5],
            5: [3, 4],
        }
        assert has_cycle(undirected_adj, directed=False)


class TestTopologicalSort:
    def test_topological_sort_validity(self):
        adj = {
            "cook": ["eat"],
            "wash": ["cook"],
            "shop": ["cook", "wash"],
            "eat": ["sleep"],
            "sleep": [],
        }
        order = topological_sort(adj)
        assert len(order) == 5
        for u in adj:
            for v in adj[u]:
                assert order.index(u) < order.index(v)

    def test_random_dag_topological_order(self):
        rng = random.Random(42)
        n = 50
        adj: Dict[int, List[int]] = {i: [] for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.15:
                    adj[i].append(j)

        order = topological_sort(adj)
        assert len(order) == n
        pos = {v: idx for idx, v in enumerate(order)}
        for u in adj:
            for v in adj[u]:
                assert pos[u] < pos[v]

    def test_cycle_raises_value_error(self):
        adj = {1: [2], 2: [3], 3: [1]}
        with pytest.raises(ValueError):
            topological_sort(adj)


class TestDijkstraAndShortestPath:
    def test_negative_weight_raises(self):
        adj = {1: [(2, -0.5)], 2: []}
        with pytest.raises(ValueError):
            dijkstra(adj, 1)

    def test_unweighted_treated_as_weight_one(self):
        adj = {1: [2], 2: [3], 3: []}
        dist, pred = dijkstra(adj, 1)
        assert dist[1] == 0.0
        assert dist[2] == 1.0
        assert dist[3] == 2.0
        assert pred[3] == 2
        assert pred[2] == 1
        assert pred[1] is None
        assert shortest_path(adj, 1, 3) == [1, 2, 3]

    def test_shortest_path_unreachable_and_self(self):
        adj = {1: [2], 2: [], 3: [4], 4: []}
        assert shortest_path(adj, 1, 3) == []
        assert shortest_path(adj, 1, 1) == [1]

    def test_dijkstra_against_bellman_ford_random(self):
        def bellman_ford(
            verts: List[int],
            edges_list: List[Tuple[int, int, float]],
            src: int,
        ) -> Dict[int, float]:
            d = {v: float("inf") for v in verts}
            d[src] = 0.0
            for _ in range(len(verts) - 1):
                updated = False
                for u, v, w in edges_list:
                    if d[u] != float("inf") and d[u] + w < d[v]:
                        d[v] = d[u] + w
                        updated = True
                if not updated:
                    break
            return d

        rng = random.Random(12345)
        for _ in range(5):
            n = 25
            vertices_list = list(range(n))
            adj: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(n)}
            all_edges: List[Tuple[int, int, float]] = []

            for i in range(n):
                for j in range(n):
                    if i != j and rng.random() < 0.2:
                        w = round(rng.uniform(0.5, 20.0), 2)
                        adj[i].append((j, w))
                        all_edges.append((i, j, w))

            source = 0
            bf_dist = bellman_ford(vertices_list, all_edges, source)
            dijkstra_dist, _ = dijkstra(adj, source)

            for v in vertices_list:
                assert abs(dijkstra_dist[v] - bf_dist[v]) < 1e-6


class TestUnionFind:
    def test_basic_union_and_find(self):
        uf = UnionFind([1, 2, 3, 4, 5])
        assert len(uf) == 5
        assert uf.component_count == 5
        assert uf.component_count() == 5

        assert uf.union(1, 2)
        assert not uf.union(1, 2)
        assert uf.connected(1, 2)
        assert uf.component_count() == 4

        assert uf.union(3, 4)
        assert uf.union(4, 5)
        assert uf.connected(3, 5)
        assert not uf.connected(1, 5)
        assert uf.component_count() == 2

        assert uf.union(2, 5)
        assert uf.connected(1, 3)
        assert uf.component_count() == 1

    def test_auto_add_unseen_elements(self):
        uf = UnionFind()
        assert len(uf) == 0
        assert uf.union("x", "y")
        assert len(uf) == 2
        assert uf.connected("x", "y")
        assert "x" in uf
        assert "z" not in uf
        assert uf.find("z") == "z"
        assert "z" in uf
        assert len(uf) == 3

    def test_arbitrary_hashable_elements(self):
        uf = UnionFind([(1, 2), "hello", 42])
        assert len(uf) == 3
        assert uf.union((1, 2), "hello")
        assert uf.connected((1, 2), "hello")
        assert not uf.connected((1, 2), 42)

    def test_union_find_against_naive_labeling(self):
        def naive_components(
            nodes: List[int],
            edges_list: List[Tuple[int, int]],
        ) -> Tuple[Dict[int, int], int]:
            graph: Dict[int, List[int]] = {x: [] for x in nodes}
            for u, v in edges_list:
                graph[u].append(v)
                graph[v].append(u)
            visited: Set[int] = set()
            labels: Dict[int, int] = {}
            count = 0
            for node in nodes:
                if node not in visited:
                    queue: deque = deque([node])
                    visited.add(node)
                    while queue:
                        curr = queue.popleft()
                        labels[curr] = count
                        for nxt in graph[curr]:
                            if nxt not in visited:
                                visited.add(nxt)
                                queue.append(nxt)
                    count += 1
            return labels, count

        rng = random.Random(888)
        elements = list(range(100))
        edges: List[Tuple[int, int]] = []
        uf = UnionFind(elements)

        for _ in range(80):
            u, v = rng.sample(elements, 2)
            edges.append((u, v))
            uf.union(u, v)

        expected_labels, expected_count = naive_components(elements, edges)
        assert uf.component_count() == expected_count

        for i in range(len(elements)):
            for j in range(i + 1, min(i + 15, len(elements))):
                expected_connected = expected_labels[elements[i]] == expected_labels[elements[j]]
                assert uf.connected(elements[i], elements[j]) == expected_connected


class TestDeepGraphRecursionSafety:
    def test_10000_node_path_graph(self):
        n = 10000
        g = Graph(directed=True)
        for i in range(n - 1):
            g.add_edge(i, i + 1)

        assert len(g) == n
        assert not g.has_cycle()

        topo = g.topological_sort()
        assert len(topo) == n

        dfs_order = g.dfs(0)
        assert len(dfs_order) == n

        bfs_order = g.bfs(0)
        assert len(bfs_order) == n

        path = g.shortest_path(0, n - 1)
        assert len(path) == n
        assert path[0] == 0
        assert path[-1] == n - 1

        uf = UnionFind()
        for i in range(n - 1):
            uf.union(i, i + 1)
        assert len(uf) == n
        assert uf.connected(0, n - 1)
        assert uf.component_count() == 1


def test_top_level_exports():
    expected_names = [
        "Graph",
        "UnionFind",
        "bfs",
        "dfs",
        "has_cycle",
        "topological_sort",
        "dijkstra",
        "shortest_path",
    ]
    for name in expected_names:
        assert name in raghu.__all__
        assert hasattr(raghu, name)
    assert hasattr(raghu, "__version__")
