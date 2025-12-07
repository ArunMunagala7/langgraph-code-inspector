# Test Case: Perfect Code - Binary Search
# Expected Quality: A+
# Expected Bugs: 0


def binary_search(arr: list[int], target: int) -> int:
    """
    Perform binary search on a sorted array.
    
    Args:
        arr: Sorted list of integers
        target: Value to search for
        
    Returns:
        Index of target if found, -1 otherwise
        
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
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
    """Test cases for binary search."""
    assert binary_search([1, 2, 3, 4, 5], 3) == 2
    assert binary_search([1, 2, 3, 4, 5], 6) == -1
    assert binary_search([], 1) == -1
    assert binary_search([1], 1) == 0
    print("All tests passed!")
