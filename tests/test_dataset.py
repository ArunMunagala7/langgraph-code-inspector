"""
Comprehensive Test Dataset for Code Analysis
Contains diverse code snippets with varying complexity, quality, and characteristics
"""

TEST_CASES = {
    "perfect_code": {
        "name": "Perfect Code - Binary Search",
        "language": "python",
        "expected_quality": "A+",
        "expected_bugs": 0,
        "code": """
def binary_search(arr: list[int], target: int) -> int:
    \"\"\"
    Perform binary search on a sorted array.
    
    Args:
        arr: Sorted list of integers
        target: Value to search for
        
    Returns:
        Index of target if found, -1 otherwise
        
    Time Complexity: O(log n)
    Space Complexity: O(1)
    \"\"\"
    if not arr:
        return -1
    
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Prevents overflow
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def test_binary_search():
    \"\"\"Test cases for binary search.\"\"\"
    assert binary_search([1, 2, 3, 4, 5], 3) == 2
    assert binary_search([1, 2, 3, 4, 5], 6) == -1
    assert binary_search([], 1) == -1
    assert binary_search([1], 1) == 0
    print("All tests passed!")
"""
    },
    
    "buggy_code": {
        "name": "Buggy Code - Multiple Issues",
        "language": "python",
        "expected_quality": "D",
        "expected_bugs": 5,
        "code": """
def calculate_average(numbers):
    # Bug 1: No input validation
    # Bug 2: Division by zero if empty list
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    avg = total / len(numbers)  # ZeroDivisionError risk
    return avg

def find_max(lst):
    # Bug 3: No check for empty list
    max = lst[0]  # IndexError if empty
    for num in lst:
        if num > max:
            max = num
    return max

# Bug 4: Hardcoded password
password = "admin123"

def login(user, pwd):
    # Bug 5: Insecure comparison, no hashing
    if pwd == password:
        return True
    return False
"""
    },
    
    "complex_algorithm": {
        "name": "Complex Algorithm - Dijkstra's Shortest Path",
        "language": "python",
        "expected_quality": "B+",
        "expected_bugs": 0,
        "code": """
import heapq
from typing import Dict, List, Tuple

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Dict[int, int]:
    \"\"\"
    Find shortest paths from start node to all other nodes.
    
    Args:
        graph: Adjacency list {node: [(neighbor, weight), ...]}
        start: Starting node
        
    Returns:
        Dictionary of shortest distances {node: distance}
    \"\"\"
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        if current_dist > distances[current_node]:
            continue
        
        for neighbor, weight in graph.get(current_node, []):
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances
"""
    },
    
    "inefficient_code": {
        "name": "Inefficient Code - Poor Performance",
        "language": "python",
        "expected_quality": "C",
        "expected_bugs": 2,
        "code": """
def is_prime(n):
    # Inefficient: O(n) when O(√n) is possible
    if n < 2:
        return False
    for i in range(2, n):  # Should only go to sqrt(n)
        if n % i == 0:
            return False
    return True

def find_duplicates(arr):
    # Inefficient: O(n²) when O(n) is possible with set
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates

def fibonacci(n):
    # Inefficient: Exponential time, no memoization
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    },
    
    "unreadable_code": {
        "name": "Unreadable Code - Poor Style",
        "language": "python",
        "expected_quality": "D-",
        "expected_bugs": 3,
        "code": """
def f(x,y,z):
    a=x+y
    b=a*z
    if a>10:c=a*2
    else:c=a/2
    d=[i for i in range(100) if i%2==0 and i%3==0 and i%5==0]
    return b+c+sum(d)

def g(l):
    r=[]
    for i in l:
        if type(i)==int:
            r.append(i*2)
        elif type(i)==str:
            r.append(i.upper())
    return r

x=f(5,10,2)
y=g([1,2,"hello",3,"world"])
"""
    },
    
    "edge_cases_missing": {
        "name": "Missing Edge Cases",
        "language": "python",
        "expected_quality": "C+",
        "expected_bugs": 4,
        "code": """
def reverse_string(s):
    # Missing: None check, empty string check
    return s[::-1]

def get_first_element(arr):
    # Missing: empty array check
    return arr[0]

def divide(a, b):
    # Missing: division by zero check
    return a / b

def parse_json(json_string):
    import json
    # Missing: error handling for invalid JSON
    return json.loads(json_string)

def access_dict(d, key):
    # Missing: key existence check
    return d[key]
"""
    },
    
    "good_practices": {
        "name": "Good Practices - Clean Code",
        "language": "python",
        "expected_quality": "A",
        "expected_bugs": 0,
        "code": """
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"

@dataclass
class Task:
    id: int
    title: str
    description: str
    status: Status
    
    def mark_completed(self) -> None:
        \"\"\"Mark task as completed.\"\"\"
        self.status = Status.COMPLETED
    
    def is_active(self) -> bool:
        \"\"\"Check if task is active.\"\"\"
        return self.status == Status.ACTIVE

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        \"\"\"Add a new task.\"\"\"
        if not isinstance(task, Task):
            raise TypeError("Expected Task object")
        self.tasks.append(task)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        \"\"\"Get task by ID.\"\"\"
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_completed_tasks(self) -> List[Task]:
        \"\"\"Get all completed tasks.\"\"\"
        return [t for t in self.tasks if t.status == Status.COMPLETED]
"""
    },
    
    "security_issues": {
        "name": "Security Vulnerabilities",
        "language": "python",
        "expected_quality": "F",
        "expected_bugs": 6,
        "code": """
import os

# Security Issue 1: Hardcoded credentials
DB_PASSWORD = "password123"
API_KEY = "sk_live_abc123xyz"

def execute_command(user_input):
    # Security Issue 2: Command injection vulnerability
    os.system(f"echo {user_input}")

def run_sql_query(user_id):
    import sqlite3
    # Security Issue 3: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def save_file(filename, content):
    # Security Issue 4: Path traversal vulnerability
    with open(filename, 'w') as f:
        f.write(content)

def eval_expression(expr):
    # Security Issue 5: Code injection via eval
    return eval(expr)

# Security Issue 6: Insecure random for security purposes
import random
def generate_token():
    return random.randint(1000, 9999)
"""
    },
    
    "nested_complexity": {
        "name": "High Cyclomatic Complexity",
        "language": "python",
        "expected_quality": "C-",
        "expected_bugs": 2,
        "code": """
def process_data(data, mode, validate, transform, filter_nulls, sort_result):
    result = []
    
    if data is not None:
        if len(data) > 0:
            if mode == "strict":
                if validate:
                    for item in data:
                        if item is not None:
                            if isinstance(item, dict):
                                if "value" in item:
                                    if item["value"] > 0:
                                        if transform:
                                            item["value"] = item["value"] * 2
                                        if filter_nulls:
                                            if item.get("status") is not None:
                                                result.append(item)
                                        else:
                                            result.append(item)
            elif mode == "relaxed":
                for item in data:
                    if item:
                        result.append(item)
        
        if sort_result:
            result.sort(key=lambda x: x.get("value", 0))
    
    return result
"""
    },
    
    "javascript_async": {
        "name": "JavaScript Async/Await Pattern",
        "language": "javascript",
        "expected_quality": "B+",
        "expected_bugs": 1,
        "code": """
// Async data fetching with error handling
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch user:', error);
        return null;
    }
}

// Bug: No error handling for Promise.all
async function fetchMultipleUsers(userIds) {
    const promises = userIds.map(id => fetchUserData(id));
    const results = await Promise.all(promises);  // Could fail if any promise rejects
    return results.filter(user => user !== null);
}

// Good: Proper error handling with Promise.allSettled
async function fetchMultipleUsersSafe(userIds) {
    const promises = userIds.map(id => fetchUserData(id));
    const results = await Promise.allSettled(promises);
    
    return results
        .filter(result => result.status === 'fulfilled')
        .map(result => result.value)
        .filter(user => user !== null);
}
"""
    },
    
    "recursive_algorithm": {
        "name": "Recursive Tree Traversal",
        "language": "python",
        "expected_quality": "A-",
        "expected_bugs": 0,
        "code": """
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    \"\"\"
    Perform inorder traversal (left -> root -> right).
    
    Time: O(n), Space: O(h) where h is height
    \"\"\"
    if root is None:
        return []
    
    result = []
    result.extend(inorder_traversal(root.left))
    result.append(root.val)
    result.extend(inorder_traversal(root.right))
    
    return result

def find_path(root: Optional[TreeNode], target: int) -> Optional[List[int]]:
    \"\"\"Find path from root to target value.\"\"\"
    if root is None:
        return None
    
    if root.val == target:
        return [root.val]
    
    # Search in left subtree
    left_path = find_path(root.left, target)
    if left_path is not None:
        return [root.val] + left_path
    
    # Search in right subtree
    right_path = find_path(root.right, target)
    if right_path is not None:
        return [root.val] + right_path
    
    return None
"""
    },
    
    "memory_leak": {
        "name": "Potential Memory Issues",
        "language": "python",
        "expected_quality": "D+",
        "expected_bugs": 3,
        "code": """
class Cache:
    def __init__(self):
        # Bug 1: Unbounded cache growth - memory leak
        self.data = {}
    
    def set(self, key, value):
        self.data[key] = value
    
    def get(self, key):
        return self.data.get(key)

# Bug 2: Circular reference
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []
    
    def add_child(self, child):
        child.parent = self  # Circular reference
        self.children.append(child)

# Bug 3: Not closing file handles
def read_files(filenames):
    contents = []
    for fname in filenames:
        f = open(fname, 'r')  # Not closed!
        contents.append(f.read())
    return contents
"""
    },
    
    "quicksort": {
        "name": "QuickSort Algorithm",
        "language": "python",
        "expected_quality": "A-",
        "expected_bugs": 0,
        "code": """
from typing import List

def quicksort(arr: List[int]) -> List[int]:
    \"\"\"
    Sort array using quicksort algorithm.
    
    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(log n) due to recursion
    \"\"\"
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)


def quicksort_inplace(arr: List[int], low: int = 0, high: int = None) -> None:
    \"\"\"In-place quicksort with O(1) extra space.\"\"\"
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_idx = partition(arr, low, high)
        quicksort_inplace(arr, low, pivot_idx - 1)
        quicksort_inplace(arr, pivot_idx + 1, high)


def partition(arr: List[int], low: int, high: int) -> int:
    \"\"\"Partition array around pivot.\"\"\"
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
"""
    },
    
    "merge_sort": {
        "name": "Merge Sort Algorithm",
        "language": "python",
        "expected_quality": "A",
        "expected_bugs": 0,
        "code": """
from typing import List

def merge_sort(arr: List[int]) -> List[int]:
    \"\"\"
    Sort array using merge sort algorithm.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    \"\"\"
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    \"\"\"Merge two sorted arrays.\"\"\"
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def merge_sort_inplace(arr: List[int], temp: List[int], left: int, right: int) -> None:
    \"\"\"In-place merge sort using temporary array.\"\"\"
    if left < right:
        mid = (left + right) // 2
        merge_sort_inplace(arr, temp, left, mid)
        merge_sort_inplace(arr, temp, mid + 1, right)
        merge_inplace(arr, temp, left, mid, right)


def merge_inplace(arr: List[int], temp: List[int], left: int, mid: int, right: int) -> None:
    \"\"\"Merge two sorted subarrays in-place.\"\"\"
    i = left
    j = mid + 1
    k = left
    
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
        k += 1
    
    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1
    
    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1
    
    for i in range(left, right + 1):
        arr[i] = temp[i]
"""
    },
    
    "bst_operations": {
        "name": "Binary Search Tree Operations",
        "language": "python",
        "expected_quality": "A-",
        "expected_bugs": 0,
        "code": """
from typing import Optional

class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BST:
    def __init__(self):
        self.root: Optional[TreeNode] = None
    
    def insert(self, val: int) -> None:
        \"\"\"Insert value into BST.\"\"\"
        if self.root is None:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node: TreeNode, val: int) -> TreeNode:
        \"\"\"Helper for recursive insertion.\"\"\"
        if node is None:
            return TreeNode(val)
        
        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        
        return node
    
    def search(self, val: int) -> bool:
        \"\"\"Search for value in BST.\"\"\"
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node: Optional[TreeNode], val: int) -> bool:
        \"\"\"Helper for recursive search.\"\"\"
        if node is None:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def delete(self, val: int) -> None:
        \"\"\"Delete value from BST.\"\"\"
        self.root = self._delete_recursive(self.root, val)
    
    def _delete_recursive(self, node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        \"\"\"Helper for recursive deletion.\"\"\"
        if node is None:
            return None
        
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children
            min_node = self._find_min(node.right)
            node.val = min_node.val
            node.right = self._delete_recursive(node.right, min_node.val)
        
        return node
    
    def _find_min(self, node: TreeNode) -> TreeNode:
        \"\"\"Find minimum value node in subtree.\"\"\"
        current = node
        while current.left is not None:
            current = current.left
        return current
"""
    },
    
    "linked_list": {
        "name": "Linked List Implementation",
        "language": "python",
        "expected_quality": "B+",
        "expected_bugs": 0,
        "code": """
from typing import Optional

class Node:
    def __init__(self, data):
        self.data = data
        self.next: Optional[Node] = None


class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.size = 0
    
    def append(self, data) -> None:
        \"\"\"Add element to end of list.\"\"\"
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def prepend(self, data) -> None:
        \"\"\"Add element to beginning of list.\"\"\"
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def delete(self, data) -> bool:
        \"\"\"Delete first occurrence of data.\"\"\"
        if self.head is None:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def reverse(self) -> None:
        \"\"\"Reverse the linked list in-place.\"\"\"
        prev = None
        current = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def find_middle(self) -> Optional[Node]:
        \"\"\"Find middle node using slow-fast pointer.\"\"\"
        if self.head is None:
            return None
        
        slow = fast = self.head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow
    
    def has_cycle(self) -> bool:
        \"\"\"Detect cycle using Floyd's algorithm.\"\"\"
        if self.head is None:
            return False
        
        slow = fast = self.head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                return True
        
        return False
"""
    },
    
    "hash_table": {
        "name": "Hash Table with Chaining",
        "language": "python",
        "expected_quality": "B+",
        "expected_bugs": 0,
        "code": """
from typing import List, Optional, Tuple

class HashTable:
    def __init__(self, size: int = 10):
        \"\"\"
        Initialize hash table with separate chaining.
        
        Time Complexity: O(1) average for insert/search/delete
        Space Complexity: O(n)
        \"\"\"
        self.size = size
        self.table: List[List[Tuple[str, any]]] = [[] for _ in range(size)]
        self.count = 0
    
    def _hash(self, key: str) -> int:
        \"\"\"Hash function using built-in hash.\"\"\"
        return hash(key) % self.size
    
    def insert(self, key: str, value: any) -> None:
        \"\"\"Insert key-value pair.\"\"\"
        index = self._hash(key)
        
        # Update if key exists
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        
        # Insert new key-value pair
        self.table[index].append((key, value))
        self.count += 1
        
        # Rehash if load factor > 0.7
        if self.count / self.size > 0.7:
            self._rehash()
    
    def get(self, key: str) -> Optional[any]:
        \"\"\"Get value for key.\"\"\"
        index = self._hash(key)
        
        for k, v in self.table[index]:
            if k == key:
                return v
        
        return None
    
    def delete(self, key: str) -> bool:
        \"\"\"Delete key-value pair.\"\"\"
        index = self._hash(key)
        
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.count -= 1
                return True
        
        return False
    
    def _rehash(self) -> None:
        \"\"\"Resize and rehash all entries.\"\"\"
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)
"""
    },
    
    "heap_operations": {
        "name": "Min Heap Implementation",
        "language": "python",
        "expected_quality": "A-",
        "expected_bugs": 0,
        "code": """
from typing import List

class MinHeap:
    def __init__(self):
        \"\"\"
        Initialize min heap.
        
        Time Complexity: O(log n) for insert/extract_min
        Space Complexity: O(n)
        \"\"\"
        self.heap: List[int] = []
    
    def parent(self, i: int) -> int:
        return (i - 1) // 2
    
    def left_child(self, i: int) -> int:
        return 2 * i + 1
    
    def right_child(self, i: int) -> int:
        return 2 * i + 2
    
    def swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def insert(self, value: int) -> None:
        \"\"\"Insert value into heap.\"\"\"
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
    
    def _heapify_up(self, i: int) -> None:
        \"\"\"Restore heap property upward.\"\"\"
        while i > 0 and self.heap[i] < self.heap[self.parent(i)]:
            self.swap(i, self.parent(i))
            i = self.parent(i)
    
    def extract_min(self) -> int:
        \"\"\"Remove and return minimum element.\"\"\"
        if not self.heap:
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        
        return min_val
    
    def _heapify_down(self, i: int) -> None:
        \"\"\"Restore heap property downward.\"\"\"
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[min_index]:
            min_index = left
        
        if right < len(self.heap) and self.heap[right] < self.heap[min_index]:
            min_index = right
        
        if min_index != i:
            self.swap(i, min_index)
            self._heapify_down(min_index)
    
    def peek(self) -> int:
        \"\"\"Return minimum without removing.\"\"\"
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def size(self) -> int:
        return len(self.heap)
"""
    },
    
    "graph_bfs_dfs": {
        "name": "Graph BFS and DFS",
        "language": "python",
        "expected_quality": "A",
        "expected_bugs": 0,
        "code": """
from typing import Dict, List, Set
from collections import deque

class Graph:
    def __init__(self):
        \"\"\"Initialize graph as adjacency list.\"\"\"
        self.graph: Dict[int, List[int]] = {}
    
    def add_edge(self, u: int, v: int) -> None:
        \"\"\"Add edge from u to v.\"\"\"
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        
        self.graph[u].append(v)
    
    def bfs(self, start: int) -> List[int]:
        \"\"\"
        Breadth-first search traversal.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        \"\"\"
        if start not in self.graph:
            return []
        
        visited: Set[int] = set()
        queue = deque([start])
        result = []
        
        visited.add(start)
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start: int) -> List[int]:
        \"\"\"
        Depth-first search traversal (iterative).
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        \"\"\"
        if start not in self.graph:
            return []
        
        visited: Set[int] = set()
        stack = [start]
        result = []
        
        while stack:
            node = stack.pop()
            
            if node not in visited:
                visited.add(node)
                result.append(node)
                
                # Add neighbors in reverse order for correct traversal
                for neighbor in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def dfs_recursive(self, start: int, visited: Set[int] = None) -> List[int]:
        \"\"\"Depth-first search (recursive).\"\"\"
        if visited is None:
            visited = set()
        
        if start not in self.graph or start in visited:
            return []
        
        visited.add(start)
        result = [start]
        
        for neighbor in self.graph[start]:
            result.extend(self.dfs_recursive(neighbor, visited))
        
        return result
    
    def has_path(self, start: int, end: int) -> bool:
        \"\"\"Check if path exists between two nodes.\"\"\"
        if start not in self.graph:
            return False
        
        visited: Set[int] = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            node = queue.popleft()
            
            if node == end:
                return True
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False
"""
    },
    
    "dynamic_programming": {
        "name": "Dynamic Programming Examples",
        "language": "python",
        "expected_quality": "A-",
        "expected_bugs": 0,
        "code": """
from typing import List

def fibonacci_dp(n: int) -> int:
    \"\"\"
    Calculate nth Fibonacci number using DP.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    \"\"\"
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]


def fibonacci_optimized(n: int) -> int:
    \"\"\"
    Fibonacci with O(1) space.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    \"\"\"
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr


def longest_common_subsequence(s1: str, s2: str) -> int:
    \"\"\"
    Find length of longest common subsequence.
    
    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    \"\"\"
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]


def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    \"\"\"
    0/1 Knapsack problem.
    
    Time Complexity: O(n * capacity)
    Space Complexity: O(n * capacity)
    \"\"\"
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    values[i-1] + dp[i-1][w - weights[i-1]],
                    dp[i-1][w]
                )
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]


def coin_change(coins: List[int], amount: int) -> int:
    \"\"\"
    Minimum coins needed to make amount.
    
    Time Complexity: O(amount * len(coins))
    Space Complexity: O(amount)
    \"\"\"
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
"""
    },
    
    "trie_implementation": {
        "name": "Trie (Prefix Tree)",
        "language": "python",
        "expected_quality": "A-",
        "expected_bugs": 0,
        "code": """
from typing import Dict, List

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False


class Trie:
    \"\"\"
    Trie data structure for efficient string operations.
    
    Time Complexity: O(m) for insert/search/delete where m is word length
    Space Complexity: O(n * m) where n is number of words
    \"\"\"
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        \"\"\"Insert word into trie.\"\"\"
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        \"\"\"Search for exact word in trie.\"\"\"
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        \"\"\"Check if any word starts with prefix.\"\"\"
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> TrieNode:
        \"\"\"Find node corresponding to prefix.\"\"\"
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def find_words_with_prefix(self, prefix: str) -> List[str]:
        \"\"\"Find all words starting with prefix.\"\"\"
        node = self._find_node(prefix)
        
        if node is None:
            return []
        
        words = []
        self._collect_words(node, prefix, words)
        return words
    
    def _collect_words(self, node: TrieNode, current: str, words: List[str]) -> None:
        \"\"\"Recursively collect all words from node.\"\"\"
        if node.is_end_of_word:
            words.append(current)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current + char, words)
    
    def delete(self, word: str) -> bool:
        \"\"\"Delete word from trie.\"\"\"
        return self._delete_recursive(self.root, word, 0)
    
    def _delete_recursive(self, node: TrieNode, word: str, index: int) -> bool:
        \"\"\"Helper for recursive deletion.\"\"\"
        if index == len(word):
            if not node.is_end_of_word:
                return False
            
            node.is_end_of_word = False
            return len(node.children) == 0
        
        char = word[index]
        if char not in node.children:
            return False
        
        child_node = node.children[char]
        should_delete = self._delete_recursive(child_node, word, index + 1)
        
        if should_delete:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end_of_word
        
        return False
"""
    }
}


def generate_test_report():
    """Generate a test report showing all test cases."""
    print("=" * 80)
    print("CODE ANALYSIS TEST DATASET")
    print("=" * 80)
    print(f"\nTotal Test Cases: {len(TEST_CASES)}\n")
    
    for key, test in TEST_CASES.items():
        print(f"\n{'='*80}")
        print(f"Test Case: {test['name']}")
        print(f"Language: {test['language']}")
        print(f"Expected Quality: {test['expected_quality']}")
        print(f"Expected Bugs: {test['expected_bugs']}")
        print(f"Code Length: {len(test['code'])} characters")
        print(f"Lines: {len(test['code'].splitlines())}")
        print(f"{'='*80}")


def export_to_files():
    """Export each test case to a separate file."""
    import os
    
    test_dir = "test_cases"
    os.makedirs(test_dir, exist_ok=True)
    
    for key, test in TEST_CASES.items():
        ext = '.js' if test['language'] == 'javascript' else '.py'
        filename = f"{test_dir}/{key}{ext}"
        
        with open(filename, 'w') as f:
            f.write(f"# Test Case: {test['name']}\n")
            f.write(f"# Expected Quality: {test['expected_quality']}\n")
            f.write(f"# Expected Bugs: {test['expected_bugs']}\n\n")
            f.write(test['code'])
        
        print(f"Created: {filename}")


if __name__ == "__main__":
    generate_test_report()
    print("\n" + "=" * 80)
    print("Exporting test cases to files...")
    print("=" * 80 + "\n")
    export_to_files()
