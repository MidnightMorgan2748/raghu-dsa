"""Graph algorithms and data structures: Graph, UnionFind, BFS, DFS, Dijkstra."""

import heapq
from collections import deque as _deque
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
)

T = TypeVar("T")

__all__ = [
    "Graph",
    "UnionFind",
    "bfs",
    "dfs",
    "dijkstra",
    "has_cycle",
    "shortest_path",
    "topological_sort",
]


class _ComponentCount(int):
    def __call__(self) -> int:
        return int(self)


def _parse_neighbor(adj_list: Dict[Any, Any], item: Any) -> Tuple[Any, float]:
    if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], (int, float)):
        if item in adj_list:
            return item, 1.0
        return item[0], float(item[1])
    return item, 1.0


def _get_neighbors(adj_list: Dict[Any, Any], u: Any) -> List[Any]:
    neighbors = adj_list.get(u, [])
    result: List[Any] = []
    for item in neighbors:
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], (int, float)):
            if item in adj_list:
                result.append(item)
            else:
                result.append(item[0])
        else:
            result.append(item)
    return result


def bfs(adj_list: Dict[Any, Any], start: Any) -> List[Any]:
    """Perform breadth-first search from ``start`` returning visit order.

    Accepts unweighted ``Dict[V, Iterable[V]]`` or weighted ``Dict[V, Iterable[Tuple[V, float]]]``.

    Args:
        adj_list: Adjacency list representation of the graph.
        start: Starting vertex.

    Returns:
        List of vertices in BFS visit order.

    Time: O(V + E). Space: O(V).
    """
    if start not in adj_list:
        return []
    visited: Set[Any] = {start}
    queue: _deque[Any] = _deque([start])
    order: List[Any] = []
    while queue:
        curr = queue.popleft()
        order.append(curr)
        for nxt in _get_neighbors(adj_list, curr):
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
    return order


def dfs(adj_list: Dict[Any, Any], start: Any) -> List[Any]:
    """Perform iterative depth-first search from ``start`` returning visit order.

    Accepts unweighted ``Dict[V, Iterable[V]]`` or weighted ``Dict[V, Iterable[Tuple[V, float]]]``.

    Args:
        adj_list: Adjacency list representation of the graph.
        start: Starting vertex.

    Returns:
        List of vertices in DFS visit order.

    Time: O(V + E). Space: O(V).
    """
    if start not in adj_list:
        return []
    visited: Set[Any] = set()
    order: List[Any] = []
    stack: List[Any] = [start]
    while stack:
        curr = stack.pop()
        if curr not in visited:
            visited.add(curr)
            order.append(curr)
            neighbors = _get_neighbors(adj_list, curr)
            for nxt in reversed(neighbors):
                if nxt not in visited:
                    stack.append(nxt)
    return order


def _has_cycle_directed(adj_list: Dict[Any, Any]) -> bool:
    all_vertices: Set[Any] = set(adj_list.keys())
    for u in adj_list:
        for v in _get_neighbors(adj_list, u):
            all_vertices.add(v)
    color: Dict[Any, int] = {}
    for node in all_vertices:
        if color.get(node, 0) != 0:
            continue
        color[node] = 1
        stack: List[Tuple[Any, Iterator[Any]]] = [
            (node, iter(_get_neighbors(adj_list, node)))
        ]
        while stack:
            curr, it = stack[-1]
            try:
                nxt = next(it)
                nxt_color = color.get(nxt, 0)
                if nxt_color == 1:
                    return True
                if nxt_color == 0:
                    color[nxt] = 1
                    stack.append((nxt, iter(_get_neighbors(adj_list, nxt))))
            except StopIteration:
                color[curr] = 2
                stack.pop()
    return False


def _has_cycle_undirected(adj_list: Dict[Any, Any]) -> bool:
    all_vertices: Set[Any] = set(adj_list.keys())
    for u in adj_list:
        for v in _get_neighbors(adj_list, u):
            all_vertices.add(v)
    visited: Set[Any] = set()
    for start in all_vertices:
        if start in visited:
            continue
        visited.add(start)
        queue: _deque[Tuple[Any, Any]] = _deque([(start, None)])
        while queue:
            curr, parent = queue.popleft()
            for nxt in _get_neighbors(adj_list, curr):
                if nxt == curr:
                    return True
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, curr))
                elif nxt != parent:
                    return True
    return False


def has_cycle(adj_list: Dict[Any, Any], directed: bool = False) -> bool:
    """Return True if the graph contains at least one cycle.

    Directed cycle detection uses three-color (white/gray/black) DFS iteratively.
    Undirected cycle detection uses parent tracking and handles self-loops iteratively.

    Args:
        adj_list: Adjacency list representation of the graph.
        directed: Whether the graph is directed.

    Returns:
        True if the graph contains a cycle, False otherwise.

    Time: O(V + E). Space: O(V).
    """
    if directed:
        return _has_cycle_directed(adj_list)
    return _has_cycle_undirected(adj_list)


def topological_sort(adj_list: Dict[Any, Any]) -> List[Any]:
    """Compute a topological ordering of vertices using Kahn's algorithm.

    Args:
        adj_list: Adjacency list of a directed acyclic graph.

    Returns:
        List of vertices in topological order.

    Raises:
        ValueError: if the graph contains a cycle.

    Time: O(V + E). Space: O(V).
    """
    all_vertices: Set[Any] = set(adj_list.keys())
    for u in adj_list:
        for v in _get_neighbors(adj_list, u):
            all_vertices.add(v)
    in_degree: Dict[Any, int] = {v: 0 for v in all_vertices}
    for u in adj_list:
        for v in _get_neighbors(adj_list, u):
            in_degree[v] += 1
    queue: _deque[Any] = _deque([v for v in all_vertices if in_degree[v] == 0])
    result: List[Any] = []
    while queue:
        curr = queue.popleft()
        result.append(curr)
        for nxt in _get_neighbors(adj_list, curr):
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)
    if len(result) != len(all_vertices):
        raise ValueError("graph has at least one cycle")
    return result


def dijkstra(
    adj_list: Dict[Any, Any],
    source: Any,
) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
    """Compute shortest path distances and predecessors from ``source`` via Dijkstra's algorithm.

    Accepts unweighted ``Dict[V, Iterable[V]]`` (treated as weight 1.0) or
    weighted ``Dict[V, Iterable[Tuple[V, float]]]``.

    Args:
        adj_list: Adjacency list representation of the graph.
        source: Source vertex.

    Returns:
        Tuple of (distances_dict, predecessors_dict).

    Raises:
        ValueError: if any edge weight is negative.

    Time: O((V + E) log V). Space: O(V).
    """
    all_vertices: Set[Any] = set(adj_list.keys())
    for u in adj_list:
        for item in adj_list[u]:
            v, _ = _parse_neighbor(adj_list, item)
            all_vertices.add(v)
    all_vertices.add(source)

    distances: Dict[Any, float] = {v: float("inf") for v in all_vertices}
    predecessors: Dict[Any, Optional[Any]] = {v: None for v in all_vertices}
    distances[source] = 0.0

    heap: List[Tuple[float, Any]] = [(0.0, source)]
    visited: Set[Any] = set()

    while heap:
        curr_dist, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        for item in adj_list.get(u, []):
            v, weight = _parse_neighbor(adj_list, item)
            if weight < 0:
                raise ValueError(f"Negative edge weight encountered: {weight}")
            new_dist = curr_dist + weight
            if new_dist < distances.get(v, float("inf")):
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(heap, (new_dist, v))

    return distances, predecessors


def shortest_path(
    adj_list: Dict[Any, Any],
    source: Any,
    target: Any,
) -> List[Any]:
    """Compute the shortest path from ``source`` to ``target`` as a list of vertices.

    Args:
        adj_list: Adjacency list representation of the graph.
        source: Source vertex.
        target: Target vertex.

    Returns:
        List of vertices forming the path from source to target, or empty list if unreachable.

    Time: O((V + E) log V). Space: O(V).
    """
    if source == target:
        all_vertices: Set[Any] = set(adj_list.keys())
        for u in adj_list:
            for item in adj_list[u]:
                v, _ = _parse_neighbor(adj_list, item)
                all_vertices.add(v)
        if source in all_vertices or not all_vertices:
            return [source]
    distances, predecessors = dijkstra(adj_list, source)
    if distances.get(target, float("inf")) == float("inf"):
        return []
    path: List[Any] = []
    curr: Optional[Any] = target
    while curr is not None:
        path.append(curr)
        curr = predecessors.get(curr)
    path.reverse()
    if path and path[0] == source:
        return path
    return []


class Graph:
    """Graph structure supporting directed, undirected, weighted, and unweighted graphs.

    Space: O(V + E).
    """

    def __init__(self, directed: bool = False) -> None:
        """Initialize a new graph.

        Args:
            directed: Whether edges are directed.

        Space: O(1).
        """
        self.directed = directed
        self._adj: Dict[Any, Dict[Any, Optional[float]]] = {}

    def add_vertex(self, v: Any) -> None:
        """Add vertex ``v`` to the graph if not already present.

        Args:
            v: Hashable vertex.

        Time: O(1). Space: O(1).
        """
        if v not in self._adj:
            self._adj[v] = {}

    def add_edge(self, u: Any, v: Any, weight: Optional[float] = None) -> None:
        """Add an edge between ``u`` and ``v`` with optional ``weight``.

        Automatically adds missing vertices.

        Args:
            u: Source vertex.
            v: Destination vertex.
            weight: Optional numeric weight.

        Time: O(1). Space: O(1).
        """
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u][v] = weight
        if not self.directed:
            self._adj[v][u] = weight

    def remove_edge(self, u: Any, v: Any) -> bool:
        """Remove the edge between ``u`` and ``v`` if present.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Returns:
            True if an edge was removed, False otherwise.

        Time: O(1). Space: O(1).
        """
        if u in self._adj and v in self._adj[u]:
            del self._adj[u][v]
            if not self.directed and v in self._adj and u in self._adj[v]:
                del self._adj[v][u]
            return True
        return False

    def remove_vertex(self, v: Any) -> bool:
        """Remove vertex ``v`` and all associated edges from the graph.

        Args:
            v: Vertex to remove.

        Returns:
            True if the vertex was removed, False if it was not found.

        Time: O(V). Space: O(1).
        """
        if v not in self._adj:
            return False
        del self._adj[v]
        for u in self._adj:
            if v in self._adj[u]:
                del self._adj[u][v]
        return True

    def has_vertex(self, v: Any) -> bool:
        """Return True if vertex ``v`` is in the graph.

        Args:
            v: Vertex to check.

        Time: O(1). Space: O(1).
        """
        return v in self._adj

    def has_edge(self, u: Any, v: Any) -> bool:
        """Return True if an edge exists from ``u`` to ``v``.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Time: O(1). Space: O(1).
        """
        return u in self._adj and v in self._adj[u]

    def neighbors(self, v: Any) -> List[Any]:
        """Return a list of neighbor vertices for ``v``.

        Args:
            v: Vertex to inspect.

        Returns:
            List of neighbor vertices.

        Raises:
            KeyError: if ``v`` is not in the graph.

        Time: O(deg(v)). Space: O(deg(v)).
        """
        if v not in self._adj:
            raise KeyError(f"Vertex {v!r} not in graph")
        return list(self._adj[v].keys())

    def vertices(self) -> List[Any]:
        """Return a list of all vertices in the graph.

        Time: O(V). Space: O(V).
        """
        return list(self._adj.keys())

    def edges(self) -> List[Tuple[Any, ...]]:
        """Return a list of all edges as tuples.

        Returns (u, v) for unweighted edges or (u, v, weight) for weighted edges.

        Time: O(V + E). Space: O(E).
        """
        result: List[Tuple[Any, ...]] = []
        seen: Set[Any] = set()
        for u in self._adj:
            for v, w in self._adj[u].items():
                if not self.directed:
                    edge_id = frozenset([u, v]) if u != v else (u, u)
                    if edge_id in seen:
                        continue
                    seen.add(edge_id)
                if w is not None:
                    result.append((u, v, w))
                else:
                    result.append((u, v))
        return result

    def to_adjacency_list(self, weighted: Optional[bool] = None) -> Dict[Any, Any]:
        """Convert graph to an adjacency list.

        Args:
            weighted: Optional boolean flag. If True, returns Dict[V, List[Tuple[V, float]]].
                If False, returns Dict[V, List[V]]. If None, returns weighted format
                if any edge has a weight, otherwise unweighted format.

        Returns:
            Adjacency list dictionary.

        Time: O(V + E). Space: O(V + E).
        """
        has_any_weight = any(
            w is not None for u in self._adj for w in self._adj[u].values()
        )
        use_weighted = weighted if weighted is not None else has_any_weight
        if use_weighted:
            return {
                u: [
                    (v, float(w) if w is not None else 1.0)
                    for v, w in self._adj[u].items()
                ]
                for u in self._adj
            }
        return {u: list(self._adj[u].keys()) for u in self._adj}

    def bfs(self, start: Any) -> List[Any]:
        """Perform breadth-first search from ``start`` returning visit order.

        Args:
            start: Starting vertex.

        Time: O(V + E). Space: O(V).
        """
        return bfs(self.to_adjacency_list(weighted=False), start)

    def dfs(self, start: Any) -> List[Any]:
        """Perform iterative depth-first search from ``start`` returning visit order.

        Args:
            start: Starting vertex.

        Time: O(V + E). Space: O(V).
        """
        return dfs(self.to_adjacency_list(weighted=False), start)

    def has_cycle(self) -> bool:
        """Return True if the graph contains a cycle.

        Time: O(V + E). Space: O(V).
        """
        return has_cycle(self.to_adjacency_list(weighted=False), directed=self.directed)

    def topological_sort(self) -> List[Any]:
        """Return a topological ordering of vertices via Kahn's algorithm.

        Raises:
            ValueError: if the graph contains a cycle.

        Time: O(V + E). Space: O(V).
        """
        return topological_sort(self.to_adjacency_list(weighted=False))

    def dijkstra(
        self,
        source: Any,
    ) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
        """Compute shortest path distances and predecessors from ``source``.

        Time: O((V + E) log V). Space: O(V).
        """
        return dijkstra(self.to_adjacency_list(weighted=True), source)

    def shortest_path(self, source: Any, target: Any) -> List[Any]:
        """Compute the shortest path from ``source`` to ``target``.

        Time: O((V + E) log V). Space: O(V).
        """
        return shortest_path(self.to_adjacency_list(weighted=True), source, target)

    def __len__(self) -> int:
        return len(self._adj)

    def __contains__(self, v: Any) -> bool:
        return self.has_vertex(v)

    def __repr__(self) -> str:
        kind = "directed" if self.directed else "undirected"
        return f"Graph({kind}, vertices={len(self._adj)}, edges={len(self.edges())})"


class UnionFind(Generic[T]):
    """Disjoint-set data structure with union-by-rank and iterative path compression.

    Space: O(n).
    """

    def __init__(self, elements: Optional[Iterable[T]] = None) -> None:
        """Initialize a union-find data structure.

        Args:
            elements: Optional initial elements to add as singleton components.

        Space: O(n).
        """
        self._parent: Dict[T, T] = {}
        self._rank: Dict[T, int] = {}
        self._num_components: int = 0
        if elements is not None:
            for elem in elements:
                self.add(elem)

    def add(self, x: T) -> bool:
        """Add an element as a new singleton component if not already present.

        Args:
            x: Element to add.

        Returns:
            True if element was added, False if already present.

        Time: O(1). Space: O(1).
        """
        if x in self._parent:
            return False
        self._parent[x] = x
        self._rank[x] = 0
        self._num_components += 1
        return True

    def find(self, x: T) -> T:
        """Find the component representative for ``x`` with iterative path compression.

        Automatically adds unseen elements.

        Args:
            x: Element to find.

        Returns:
            Representative of the component containing ``x``.

        Time: O(alpha(n)) amortized. Space: O(1).
        """
        if x not in self._parent:
            self.add(x)
            return x
        root = x
        while root != self._parent[root]:
            root = self._parent[root]
        curr = x
        while curr != root:
            nxt = self._parent[curr]
            self._parent[curr] = root
            curr = nxt
        return root

    def union(self, u: T, v: T) -> bool:
        """Merge the components containing ``u`` and ``v`` using union by rank.

        Automatically adds unseen elements.

        Args:
            u: First element.
            v: Second element.

        Returns:
            True if two disjoint components were merged, False if already joined.

        Time: O(alpha(n)) amortized. Space: O(1).
        """
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u == root_v:
            return False
        if self._rank[root_u] < self._rank[root_v]:
            self._parent[root_u] = root_v
        elif self._rank[root_u] > self._rank[root_v]:
            self._parent[root_v] = root_u
        else:
            self._parent[root_v] = root_u
            self._rank[root_u] += 1
        self._num_components -= 1
        return True

    def connected(self, u: T, v: T) -> bool:
        """Return True if ``u`` and ``v`` belong to the same component.

        Args:
            u: First element.
            v: Second element.

        Returns:
            True if in the same component, False otherwise.

        Time: O(alpha(n)) amortized. Space: O(1).
        """
        return self.find(u) == self.find(v)

    @property
    def component_count(self) -> _ComponentCount:
        """Return the number of disjoint components.

        Can be called as a method ``component_count()`` or accessed as an attribute.

        Time: O(1). Space: O(1).
        """
        return _ComponentCount(self._num_components)

    def __len__(self) -> int:
        return len(self._parent)

    def __contains__(self, x: Any) -> bool:
        return x in self._parent

    def __repr__(self) -> str:
        return f"UnionFind(elements={len(self._parent)}, components={self._num_components})"
