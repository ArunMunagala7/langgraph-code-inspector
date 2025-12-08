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
