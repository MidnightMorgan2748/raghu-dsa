# Changelog

All notable changes to `raghu` are documented in this file.

## [0.5.0]

- Packaging and release readiness.
- Validated full strict type checking with `mypy --strict`.
- Formatted and linted with `ruff`.
- Added multi-version GitHub Actions CI matrix across Python 3.8 through 3.13.
- Added comprehensive top-level export verification tests.

## [0.4.0]

- Added `HashMap`: separate chaining hash table with dynamic resizing and load factor management.
- Added `LRUCache`: O(1) least-recently-used cache implemented with a plain dict and doubly linked list.

## [0.3.0]

- Added `Graph`: directed and undirected graph supporting weighted and unweighted edges.
- Added graph algorithms: `bfs`, `dfs`, `has_cycle`, `topological_sort`, `dijkstra`, `shortest_path`.
- Added `UnionFind`: disjoint-set structure with path compression and union by rank.

## [0.2.0]

- Added `BinaryTree`: binary tree with iterative traversals (`inorder`, `preorder`, `postorder`, `level_order`).
- Added `BST`: iterative binary search tree with `insert`, `search`, `delete`, `find_min`, `find_max`.
- Added `MinHeap` and `MaxHeap`: array-backed binary heaps with $O(n)$ `heapify`.
- Added `Trie`: prefix tree for efficient string insertion, search, and prefix matching.

## [0.1.0]

- Initial release.
- Added linear data structures: `Stack`, `Queue`, `Deque`, `SinglyLinkedList`, `DoublyLinkedList`.
- Added searching algorithms: `linear_search`, `binary_search`.
- Added sorting algorithms: `bubble_sort`, `selection_sort`, `insertion_sort`, `merge_sort`, `quick_sort`, `heap_sort`.
