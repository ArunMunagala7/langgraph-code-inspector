# Test Case: Merge Sort Algorithm
# Expected Quality: A
# Expected Bugs: 0


from typing import List

def merge_sort(arr: List[int]) -> List[int]:
    """
    Sort array using merge sort algorithm.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted arrays."""
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
    """In-place merge sort using temporary array."""
    if left < right:
        mid = (left + right) // 2
        merge_sort_inplace(arr, temp, left, mid)
        merge_sort_inplace(arr, temp, mid + 1, right)
        merge_inplace(arr, temp, left, mid, right)


def merge_inplace(arr: List[int], temp: List[int], left: int, mid: int, right: int) -> None:
    """Merge two sorted subarrays in-place."""
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
