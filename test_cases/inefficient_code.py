# Test Case: Inefficient Code - Poor Performance
# Expected Quality: C
# Expected Bugs: 2


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
