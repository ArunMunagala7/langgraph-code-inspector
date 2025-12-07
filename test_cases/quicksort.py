# Test Case: QuickSort Algorithm
# Expected Quality: A-
# Expected Bugs: 0


from typing import List

def quicksort(arr: List[int]) -> List[int]:
    """
    Sort array using quicksort algorithm.
    
    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(log n) due to recursion
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)


def quicksort_inplace(arr: List[int], low: int = 0, high: int = None) -> None:
    """In-place quicksort with O(1) extra space."""
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_idx = partition(arr, low, high)
        quicksort_inplace(arr, low, pivot_idx - 1)
        quicksort_inplace(arr, pivot_idx + 1, high)


def partition(arr: List[int], low: int, high: int) -> int:
    """Partition array around pivot."""
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
