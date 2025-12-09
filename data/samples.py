"""
Sample code snippets for testing the code inspector system.
"""
import json


SAMPLES = {
    # Easy - Basic iteration
    "python_sum_array": {
        "language": "python",
        "difficulty": "Easy",
        "code": """def sum_array(arr):
    total = 0
    for x in arr:
        total += x
    return total"""
    },
    
    # Easy - Simple validation
    "python_is_palindrome": {
        "language": "python",
        "difficulty": "Easy",
        "code": """def is_palindrome(s):
    s = s.lower().replace(' ', '')
    return s == s[::-1]"""
    },
    
    # Easy - Basic recursion
    "python_fibonacci": {
        "language": "python",
        "difficulty": "Easy",
        "code": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)"""
    },
    
    # Medium - Search algorithm
    "python_binary_search": {
        "language": "python",
        "difficulty": "Medium",
        "code": """def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1"""
    },
    
    # Medium - Two pointers
    "python_two_sum": {
        "language": "python",
        "difficulty": "Medium",
        "code": """def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None"""
    },
    
    # Medium - Class with data structure
    "python_stack": {
        "language": "python",
        "difficulty": "Medium",
        "code": """class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0"""
    },
    
    # Medium - Nested loops
    "python_bubble_sort": {
        "language": "python",
        "difficulty": "Medium",
        "code": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr"""
    },
    
    # Hard - Complex class with multiple methods
    "python_lru_cache": {
        "language": "python",
        "difficulty": "Hard",
        "code": """class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)"""
    },
    
    # Hard - Dynamic programming
    "python_longest_common_subsequence": {
        "language": "python",
        "difficulty": "Hard",
        "code": """def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]"""
    },
    
    # Easy - JavaScript
    "javascript_factorial": {
        "language": "javascript",
        "difficulty": "Easy",
        "code": """function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    }
    return n * factorial(n - 1);
}"""
    },
    
    # Medium - Linked List (Python)
    "python_reverse_linked_list": {
        "language": "python",
        "difficulty": "Medium",
        "code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    return prev"""
    },
    
    # Medium - Graph DFS (Python)
    "python_graph_dfs": {
        "language": "python",
        "difficulty": "Medium",
        "code": """def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    result = [start]
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))
    
    return result"""
    },
    
    # Medium - Matrix traversal (Python)
    "python_spiral_matrix": {
        "language": "python",
        "difficulty": "Medium",
        "code": """def spiral_order(matrix):
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1
        
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
        
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    
    return result"""
    },
    
    # Hard - Backtracking (Python)
    "python_n_queens": {
        "language": "python",
        "difficulty": "Hard",
        "code": """def solve_n_queens(n):
    def is_safe(board, row, col):
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        
        # Check diagonal
        for i in range(row):
            if abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def backtrack(row, board):
        if row == n:
            solutions.append(board[:])
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1, board)
                board[row] = -1
    
    solutions = []
    backtrack(0, [-1] * n)
    return solutions"""
    },
    
    # Hard - Trie data structure (Python)
    "python_trie": {
        "language": "python",
        "difficulty": "Hard",
        "code": """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True"""
    },
    
    # Medium - C++ Binary Tree
    "cpp_inorder_traversal": {
        "language": "cpp",
        "difficulty": "Medium",
        "code": """struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

vector<int> inorderTraversal(TreeNode* root) {
    vector<int> result;
    stack<TreeNode*> stk;
    TreeNode* curr = root;
    
    while (curr != nullptr || !stk.empty()) {
        while (curr != nullptr) {
            stk.push(curr);
            curr = curr->left;
        }
        curr = stk.top();
        stk.pop();
        result.push_back(curr->val);
        curr = curr->right;
    }
    
    return result;
}"""
    },
    
    # Medium - C++ Sliding Window
    "cpp_longest_substring": {
        "language": "cpp",
        "difficulty": "Medium",
        "code": """int lengthOfLongestSubstring(string s) {
    unordered_map<char, int> charIndex;
    int maxLen = 0;
    int start = 0;
    
    for (int end = 0; end < s.length(); end++) {
        if (charIndex.find(s[end]) != charIndex.end()) {
            start = max(start, charIndex[s[end]] + 1);
        }
        charIndex[s[end]] = end;
        maxLen = max(maxLen, end - start + 1);
    }
    
    return maxLen;
}"""
    },
    
    # Hard - C++ Dynamic Programming
    "cpp_edit_distance": {
        "language": "cpp",
        "difficulty": "Hard",
        "code": """int minDistance(string word1, string word2) {
    int m = word1.length();
    int n = word2.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));
    
    for (int i = 0; i <= m; i++) {
        dp[i][0] = i;
    }
    for (int j = 0; j <= n; j++) {
        dp[0][j] = j;
    }
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1[i-1] == word2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = 1 + min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});
            }
        }
    }
    
    return dp[m][n];
}"""
    },
    
    # Hard - C++ Dijkstra's Algorithm
    "cpp_dijkstra": {
        "language": "cpp",
        "difficulty": "Hard",
        "code": """vector<int> dijkstra(vector<vector<pair<int, int>>>& graph, int start) {
    int n = graph.size();
    vector<int> dist(n, INT_MAX);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    
    dist[start] = 0;
    pq.push({0, start});
    
    while (!pq.empty()) {
        int u = pq.top().second;
        int d = pq.top().first;
        pq.pop();
        
        if (d > dist[u]) continue;
        
        for (auto& edge : graph[u]) {
            int v = edge.first;
            int weight = edge.second;
            
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    
    return dist;
}"""
    },
    
    # Medium - Merge Intervals (Python)
    "python_merge_intervals": {
        "language": "python",
        "difficulty": "Medium",
        "code": """def merge_intervals(intervals):
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            merged[-1] = [last[0], max(last[1], current[1])]
        else:
            merged.append(current)
    
    return merged"""
    }
}


def get_sample(name: str) -> dict:
    """Get a sample code snippet by name."""
    return SAMPLES.get(name)


def list_samples() -> list:
    """List all available sample names."""
    return list(SAMPLES.keys())


if __name__ == "__main__":
    # Save samples to JSON file
    with open("data/samples.json", "w") as f:
        json.dump(SAMPLES, f, indent=2)
    print("✓ Saved samples to data/samples.json")
