# raghu

Clean, type-safe OOP data structures and standalone algorithms in pure Python. Zero runtime dependencies.

`raghu` provides reliable, well-tested implementations of fundamental computer science data structures and algorithms. Built for Python 3.8+ with standard library only.

---

## Installation

```bash
pip install raghu
```

---

## Quick-Start Examples

### Linear Data Structures

```python
import raghu

stack = raghu.Stack([1, 2, 3])
stack.push(4)
top_item = stack.pop()

queue = raghu.Queue()
queue.enqueue("task_a")
queue.enqueue("task_b")
first_task = queue.dequeue()

deque = raghu.Deque([10, 20])
deque.append_left(5)
deque.append_right(30)
left_item = deque.pop_left()

sll = raghu.SinglyLinkedList([1, 2, 3])
sll.reverse()

dll = raghu.DoublyLinkedList([10, 30])
dll.insert(1, 20)
forward_values = dll.traverse_forward()
```

### Searching and Sorting

```python
import raghu

numbers = [9, 3, 7, 1, 5, 2, 8]

index = raghu.binary_search(sorted(numbers), 7)

sorted_asc = raghu.merge_sort(numbers)
sorted_desc = raghu.quick_sort(numbers, key=lambda x: -x)
sorted_heap = raghu.heap_sort(numbers)
```

### Trees and Heaps

```python
import raghu

bst = raghu.BST([5, 3, 8, 1, 4, 7, 9])
bst.insert(6)
bst.delete(3)
smallest = bst.find_min()
largest = bst.find_max()
inorder_elements = bst.inorder()

min_heap = raghu.MinHeap.heapify([5, 1, 8, 3, 2])
min_val = min_heap.pop()

trie = raghu.Trie(["apple", "application", "aptitude"])
is_present = trie.search("apple")
has_prefix = trie.starts_with("app")
```

### Graphs and Disjoint Sets

```python
import raghu

g = raghu.Graph(directed=True)
g.add_edge("A", "B", weight=2.0)
g.add_edge("B", "C", weight=3.0)
g.add_edge("A", "C", weight=6.0)

bfs_order = g.bfs("A")
distances, predecessors = g.dijkstra("A")
path = g.shortest_path("A", "C")

dag = raghu.Graph(directed=True)
dag.add_edge("task1", "task2")
dag.add_edge("task2", "task3")
topo_order = dag.topological_sort()

uf = raghu.UnionFind([1, 2, 3, 4, 5])
uf.union(1, 2)
uf.union(2, 3)
are_connected = uf.connected(1, 3)
```

### Custom Containers

```python
import raghu

hmap = raghu.HashMap()
hmap["user_id"] = 101
hmap["role"] = "admin"
user = hmap.get("user_id")

lru = raghu.LRUCache(capacity=2)
lru.put("a", 1)
lru.put("b", 2)
val_a = lru.get("a")
lru.put("c", 3)
assert "b" not in lru
```

---

## Complexity Reference

| Module | Entity | Kind | Time Complexity (Average) | Time Complexity (Worst) | Space Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `linear` | `Stack` | Class | Push/Pop/Peek: $O(1)$ | Push/Pop/Peek: $O(1)$ | $O(n)$ |
| `linear` | `Queue` | Class | Enqueue/Dequeue/Front: $O(1)$ | Enqueue/Dequeue/Front: $O(1)$ | $O(n)$ |
| `linear` | `Deque` | Class | Append/Pop Left/Right: $O(1)$ | Append/Pop Left/Right: $O(1)$ | $O(n)$ |
| `linear` | `SinglyLinkedList` | Class | Insert Head/Tail: $O(1)$, Delete/Search: $O(n)$ | Insert Head/Tail: $O(1)$, Delete/Search: $O(n)$ | $O(n)$ |
| `linear` | `DoublyLinkedList` | Class | Insert Head/Tail: $O(1)$, Index Insert/Delete: $O(n)$ | Insert Head/Tail: $O(1)$, Index Insert/Delete: $O(n)$ | $O(n)$ |
| `searching_sorting` | `linear_search` | Function | $O(n)$ | $O(n)$ | $O(1)$ |
| `searching_sorting` | `binary_search` | Function | $O(\log n)$ | $O(\log n)$ | $O(1)$ iterative, $O(\log n)$ recursive |
| `searching_sorting` | `bubble_sort` | Function | $O(n^2)$ | $O(n^2)$ ($O(n)$ best) | $O(n)$ |
| `searching_sorting` | `selection_sort` | Function | $O(n^2)$ | $O(n^2)$ | $O(n)$ |
| `searching_sorting` | `insertion_sort` | Function | $O(n^2)$ | $O(n^2)$ ($O(n)$ best) | $O(n)$ |
| `searching_sorting` | `merge_sort` | Function | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| `searching_sorting` | `quick_sort` | Function | $O(n \log n)$ | $O(n^2)$ | $O(n)$ copy + $O(\log n)$ stack |
| `searching_sorting` | `heap_sort` | Function | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| `trees` | `BinaryTreeNode` | Class | $O(1)$ | $O(1)$ | $O(1)$ |
| `trees` | `BinaryTree` | Class | Traversals/Height/Size: $O(n)$ | Traversals/Height/Size: $O(n)$ | $O(n)$ |
| `trees` | `BST` | Class | Insert/Search/Delete: $O(\log n)$ | Insert/Search/Delete: $O(n)$ | $O(n)$ |
| `trees` | `MinHeap` | Class | Push/Pop: $O(\log n)$, Heapify: $O(n)$, Peek: $O(1)$ | Push/Pop: $O(\log n)$, Heapify: $O(n)$, Peek: $O(1)$ | $O(n)$ |
| `trees` | `MaxHeap` | Class | Push/Pop: $O(\log n)$, Heapify: $O(n)$, Peek: $O(1)$ | Push/Pop: $O(\log n)$, Heapify: $O(n)$, Peek: $O(1)$ | $O(n)$ |
| `trees` | `Trie` | Class | Insert/Search/Prefix: $O(m)$ | Insert/Search/Prefix: $O(m)$ | $O(N)$ characters |
| `graphs` | `Graph` | Class | Add/Has Vertex/Edge: $O(1)$ | Add/Has Vertex/Edge: $O(1)$ | $O(V + E)$ |
| `graphs` | `UnionFind` | Class | Find/Union/Connected: $O(\alpha(n))$ | Find/Union/Connected: $O(\alpha(n))$ | $O(n)$ |
| `graphs` | `bfs` | Function | $O(V + E)$ | $O(V + E)$ | $O(V)$ |
| `graphs` | `dfs` | Function | $O(V + E)$ | $O(V + E)$ | $O(V)$ |
| `graphs` | `has_cycle` | Function | $O(V + E)$ | $O(V + E)$ | $O(V)$ |
| `graphs` | `topological_sort` | Function | $O(V + E)$ | $O(V + E)$ | $O(V)$ |
| `graphs` | `dijkstra` | Function | $O((V + E) \log V)$ | $O((V + E) \log V)$ | $O(V)$ |
| `graphs` | `shortest_path` | Function | $O((V + E) \log V)$ | $O((V + E) \log V)$ | $O(V)$ |
| `containers` | `HashMap` | Class | Put/Get/Remove: $O(1)$ | Put/Get/Remove: $O(n)$ | $O(n)$ |
| `containers` | `LRUCache` | Class | Get/Put: $O(1)$ | Get/Put: $O(1)$ | $O(\text{capacity})$ |

---

## Contributing

Contributions are welcome. Please ensure that all contributions conform to project guidelines:
- Python 3.8+ compatible, standard library only at runtime.
- Full type annotations conforming to `mypy --strict`.
- Formatted and linted via `ruff`.
- All tests passing under `pytest`.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
