"""
Sample code snippets for testing the code inspector system.
"""
import json


SAMPLES = {
    "python_sum_array": {
        "language": "python",
        "code": """def sum_array(arr):
    total = 0
    for x in arr:
        total += x
    return total"""
    },
    
    "python_fibonacci": {
        "language": "python",
        "code": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)"""
    },
    
    "python_binary_search": {
        "language": "python",
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
    
    "javascript_factorial": {
        "language": "javascript",
        "code": """function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    }
    return n * factorial(n - 1);
}"""
    },
    
    "python_bubble_sort": {
        "language": "python",
        "code": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr"""
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
